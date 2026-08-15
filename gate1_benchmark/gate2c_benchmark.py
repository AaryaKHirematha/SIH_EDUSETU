import time
import json
import re
import psutil
import torch
import gc
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

# Define Kannada morphology joiner
def kannada_morph_join(word, suffix):
    suffix = suffix.strip()
    if suffix in ['ಅನ್ನು', 'ವನ್ನು', 'ಯನ್ನು']:
        if word.endswith('ಿ') or word.endswith('ೆ'): return word + 'ಯನ್ನು'
        elif word.endswith('ಮ್'): return word[:-2] + 'ಮನ್ನು'
        else: return word + 'ವನ್ನು'
    if suffix in ['ರ', 'ದ']:
        if word.endswith('ಿ') or word.endswith('ೆ'): return word + 'ಯ'
        else: return word + 'ದ'
    if suffix in ['ಗೆ', 'ಕ್ಕೆ', 'ಯಿಗೆ']:
        if word.endswith('ಿ') or word.endswith('ೆ'): return word + 'ಗೆ'
        else: return word + 'ಕ್ಕೆ'
    if suffix in ['ಇಂದ', 'ದಿಂದ', 'ಯಿಂದ']:
        if word.endswith('ಿ') or word.endswith('ೆ'): return word + 'ಯಿಂದ'
        else: return word + 'ದಿಂದ'
    if suffix in ['ಲ್ಲಿ', 'ದಲ್ಲಿ', 'ಯಲ್ಲಿ']:
        if word.endswith('ಿ') or word.endswith('ೆ'): return word + 'ಯಲ್ಲಿ'
        else: return word + 'ದಲ್ಲಿ'
    return word + ' ' + suffix

known_detached_suffixes = ['ಅನ್ನು', 'ವನ್ನು', 'ಯನ್ನು', 'ರ', 'ದ', 'ಗೆ', 'ಕ್ಕೆ', 'ಇಂದ', 'ದಿಂದ', 'ಲ್ಲಿ', 'ದಲ್ಲಿ']

# RAM/VRAM tracking
def get_ram_mb():
    return psutil.virtual_memory().used / (1024 * 1024)

def get_vram_mb():
    if torch.cuda.is_available():
        torch.cuda.synchronize()
        return torch.cuda.memory_allocated() / (1024 * 1024)
    return 0

hardware = {
    "vram_before_load": get_vram_mb(),
    "ram_before_load": get_ram_mb(),
    "vram_after_load": 0,
    "ram_after_load": 0,
    "peak_vram_inference": 0,
    "load_time": 0,
    "total_benchmark_time": 0
}

# Load Model
start_load = time.time()
model_name = "ai4bharat/indictrans2-en-indic-dist-200M"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token=True)
ip = IndicProcessor(inference=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16, token=True).cuda()
model.eval()
hardware["load_time"] = time.time() - start_load
hardware["vram_after_load"] = get_vram_mb()
hardware["ram_after_load"] = get_ram_mb()

# Core Translation function
def translate_raw(text, tgt_lang_code):
    raw_tgt_lang = "hin_Deva" if tgt_lang_code == "hi" else "kan_Knda"
    batch = ip.preprocess_batch([text], src_lang="eng_Latn", tgt_lang=raw_tgt_lang)
    inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt", max_length=256).to("cuda")
    
    t0 = time.time()
    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=5, num_return_sequences=1, max_length=256)
    latency = time.time() - t0
    
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    out_text = ip.postprocess_batch(decoded, lang=raw_tgt_lang)[0]
    
    if torch.cuda.is_available():
        current_peak = torch.cuda.max_memory_allocated() / (1024 * 1024)
        if current_peak > hardware["peak_vram_inference"]:
            hardware["peak_vram_inference"] = current_peak
            
    return out_text, latency

def safe_replace(text, token, replacement):
    escaped = re.escape(token)
    prefix = r'(?<![a-zA-Z0-9_])' if token[0].isalnum() else ''
    suffix = r'(?![a-zA-Z0-9_])' if token[-1].isalnum() else ''
    pattern = prefix + escaped + suffix
    return re.sub(pattern, replacement, text)

def protect_and_translate(text, tgt_lang_code, config, formulas_and_identifiers, term_tokens):
    # Prepare glossaries
    sorted_formulas = sorted(formulas_and_identifiers, key=len, reverse=True)
    mapping = {}
    counter = 99901
    protected_text = text
    
    for f in sorted_formulas:
        new_text = safe_replace(protected_text, f, f" {counter} ")
        if new_text != protected_text:
            mapping[str(counter)] = f
            protected_text = new_text
            counter += 1
            
    # sort terminology by english length
    sorted_terms = sorted(term_tokens, key=lambda x: len(x["en"]), reverse=True)
    for term_dict in sorted_terms:
        en_term = term_dict["en"]
        tgt_term = term_dict.get(tgt_lang_code)
        if not tgt_term:
            tgt_term = term_dict.get(f"{tgt_lang_code}_expected", en_term) # Fallback to EN if missing
            
        pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
        if pattern.search(protected_text):
            mapping[str(counter)] = tgt_term
            protected_text = pattern.sub(f" {counter} ", protected_text)
            counter += 1

    protected_text = re.sub(r'\s+', ' ', protected_text).strip()
    
    # Translate
    translated_text, latency = translate_raw(protected_text, tgt_lang_code)
    
    # Restore
    restored_text = translated_text
    morph_flags = []
    
    for ph_num, tgt_word in mapping.items():
        if config == "C" and tgt_lang_code == "kn":
            # Find attached suffixes
            pattern_attached = r'\b' + re.escape(ph_num) + r'([^\s.,!?]+)'
            for match in re.finditer(pattern_attached, restored_text):
                suffix = match.group(1)
                joined = kannada_morph_join(tgt_word, suffix)
                restored_text = restored_text.replace(match.group(0), joined)
                
            # Find detached suffixes
            for match in re.finditer(r'\b' + re.escape(ph_num) + r'\s+([^\s.,!?]+)', restored_text):
                suffix = match.group(1)
                if suffix in known_detached_suffixes:
                    joined = kannada_morph_join(tgt_word, suffix)
                    restored_text = restored_text.replace(match.group(0), joined)
                    morph_flags.append("FIXED_DETACHED_SUFFIX")
            
            # Replace remaining plain placeholders
            restored_text = re.sub(r'\b' + re.escape(ph_num) + r'\b', tgt_word, restored_text)
        else:
            # Config B or Hindi (simple restore)
            pattern_attached = r'\b' + re.escape(ph_num) + r'([^\s.,!?]+)?'
            def repl(m):
                suf = m.group(1) or ""
                return tgt_word + (" " + suf if suf else "")
            restored_text = re.sub(pattern_attached, repl, restored_text)
            
    restored_text = re.sub(r'\s+([.,!?])', r'\1', restored_text)
    
    return restored_text, latency, len(mapping), morph_flags

def run_bench():
    # Load dataset
    with open("gate2_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    benchmark_results = []
    t_start = time.time()
    
    # Sanity Check
    print("Running Sanity Check...")
    item0 = dataset[0]
    formulas_and_tech = item0.get("formula_tokens", []) + item0.get("technical_tokens", [])
    terms = item0.get("terminology_tokens", [])
    
    for lang in ["hi", "kn"]:
        for config in ["A", "B", "C"]:
            if config == "A":
                res, _ = translate_raw(item0["source_en"], lang)
            else:
                res, _, _, _ = protect_and_translate(item0["source_en"], lang, config, formulas_and_tech, terms)
            if not res:
                print(f"Sanity Check Failed for {lang} Config {config}: Empty Output")
                return
    print("Sanity Check Passed. Proceeding with 720 inferences.")

    # Main Loop
    first_latency = {"hi": {}, "kn": {}}
    
    for idx, item in enumerate(dataset):
        formulas_and_tech = item.get("formula_tokens", []) + item.get("technical_tokens", [])
        terms = item.get("terminology_tokens", [])
        source = item["source_en"]
        
        for lang in ["hi", "kn"]:
            # Config A
            a_out, a_lat = translate_raw(source, lang)
            
            # Config B
            b_out, b_lat, b_protected_count, _ = protect_and_translate(source, lang, "B", formulas_and_tech, terms)
            
            # Config C
            c_out, c_lat, c_protected_count, c_morph = protect_and_translate(source, lang, "C", formulas_and_tech, terms)
            
            # Capture cold latency
            if idx == 0:
                hardware["cold_latency_a"] = a_lat
                
            benchmark_results.append({
                "id": item["id"],
                "source_en": source,
                "domain": item["domain"],
                "target_language": lang,
                
                "out_A": a_out,
                "lat_A": a_lat,
                
                "out_B": b_out,
                "lat_B": b_lat,
                "protected_count_B": b_protected_count,
                
                "out_C": c_out,
                "lat_C": c_lat,
                "morph_flags_C": c_morph,
                
                "formula_tokens": item.get("formula_tokens", []),
                "technical_tokens": item.get("technical_tokens", []),
                "terminology_tokens": terms
            })
            
        # Cleanup every 10 items
        if idx % 10 == 0:
            gc.collect()
            torch.cuda.empty_cache()
            
    hardware["total_benchmark_time"] = time.time() - t_start
    
    # Save results
    with open("gate2_benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, ensure_ascii=False, indent=2)
        
    with open("gate2_hardware_report.json", "w", encoding="utf-8") as f:
        json.dump(hardware, f, ensure_ascii=False, indent=2)
        
    print("Benchmark Execution Complete.")

if __name__ == "__main__":
    run_bench()

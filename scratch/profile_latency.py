import time
import os
import sys

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gate1_benchmark')))

# Import
print("Loading module...")
t0 = time.time()
from gate2c_benchmark import translate_raw, protect_and_translate, ip, tokenizer, model, safe_replace, kannada_morph_join, known_detached_suffixes
print(f"Module load time (Cold Start + Model Load): {time.time() - t0:.2f}s")

def profile_translation(text, lang, config, formulas_and_ids, term_tokens):
    import re
    metrics = {}
    
    t_start = time.perf_counter()
    
    # --- PREPROCESSING / PROTECTION ---
    t_protect_start = time.perf_counter()
    
    sorted_formulas = sorted(formulas_and_ids, key=len, reverse=True)
    mapping = {}
    counter = 99901
    protected_text = text
    
    for f in sorted_formulas:
        new_text = safe_replace(protected_text, f, f" {counter} ")
        if new_text != protected_text:
            mapping[str(counter)] = f
            protected_text = new_text
            counter += 1
            
    sorted_terms = sorted(term_tokens, key=lambda x: len(x["en"]), reverse=True)
    for term_dict in sorted_terms:
        en_term = term_dict["en"]
        tgt_term = term_dict.get(lang)
        if not tgt_term:
            tgt_term = term_dict.get(f"{lang}_expected", en_term)
            
        pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
        if pattern.search(protected_text):
            mapping[str(counter)] = tgt_term
            protected_text = pattern.sub(f" {counter} ", protected_text)
            counter += 1

    protected_text = re.sub(r'\s+', ' ', protected_text).strip()
    metrics['protection_time'] = time.perf_counter() - t_protect_start
    
    # --- MODEL PREPROCESSING ---
    t_model_prep_start = time.perf_counter()
    raw_tgt_lang = "hin_Deva" if lang == "hi" else "kan_Knda"
    batch = ip.preprocess_batch([protected_text], src_lang="eng_Latn", tgt_lang=raw_tgt_lang)
    inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt", max_length=256).to("cuda")
    metrics['model_preprocessing_time'] = time.perf_counter() - t_model_prep_start
    
    # --- MODEL INFERENCE ---
    t_infer_start = time.perf_counter()
    import torch
    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=5, num_return_sequences=1, max_length=256)
    metrics['model_inference_time'] = time.perf_counter() - t_infer_start
    
    # --- MODEL POSTPROCESSING ---
    t_model_post_start = time.perf_counter()
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    out_text = ip.postprocess_batch(decoded, lang=raw_tgt_lang)[0]
    metrics['model_postprocessing_time'] = time.perf_counter() - t_model_post_start
    
    # --- RESTORATION & MORPHOLOGY ---
    t_restore_start = time.perf_counter()
    restored_text = out_text
    
    for ph_num, tgt_word in mapping.items():
        if config == "C" and lang == "kn":
            pattern_attached = r'\b' + re.escape(ph_num) + r'([^\s.,!?]+)'
            for match in re.finditer(pattern_attached, restored_text):
                suffix = match.group(1)
                joined = kannada_morph_join(tgt_word, suffix)
                restored_text = restored_text.replace(match.group(0), joined)
                
            for match in re.finditer(r'\b' + re.escape(ph_num) + r'\s+([^\s.,!?]+)', restored_text):
                suffix = match.group(1)
                if suffix in known_detached_suffixes:
                    joined = kannada_morph_join(tgt_word, suffix)
                    restored_text = restored_text.replace(match.group(0), joined)
            
            restored_text = re.sub(r'\b' + re.escape(ph_num) + r'\b', tgt_word, restored_text)
        else:
            pattern_attached = r'\b' + re.escape(ph_num) + r'([^\s.,!?]+)?'
            def repl(m):
                suf = m.group(1) or ""
                return tgt_word + (" " + suf if suf else "")
            restored_text = re.sub(pattern_attached, repl, restored_text)
            
    restored_text = re.sub(r'\s+([.,!?])', r'\1', restored_text)
    metrics['restoration_time'] = time.perf_counter() - t_restore_start
    
    metrics['total_time'] = time.perf_counter() - t_start
    
    return restored_text, metrics

def run():
    text = "The famous equation E = mc² describes the relationship between energy and mass."
    lang = "kn"
    config = "C"
    formulas_and_ids = ["E = mc²", "a", "b"]
    term_tokens = [{"en": "equation", "hi": "समीकरण", "kn": "ಸಮೀಕರಣ"}, {"en": "energy", "hi": "ऊर्जा", "kn": "ಶಕ್ತಿ"}, {"en": "mass", "hi": "द्रव्यमान", "kn": "ದ್ರವ್ಯರಾಶಿ"}]
    
    print("\n--- WARMING UP ---")
    _, _ = profile_translation(text, lang, config, formulas_and_ids, term_tokens)
    
    print("\n--- MEASURING ---")
    ITER = 10
    total_metrics = {'protection_time': 0, 'model_preprocessing_time': 0, 'model_inference_time': 0, 'model_postprocessing_time': 0, 'restoration_time': 0, 'total_time': 0}
    
    for i in range(ITER):
        _, m = profile_translation(text, lang, config, formulas_and_ids, term_tokens)
        for k in total_metrics:
            total_metrics[k] += m[k]
            
    print(f"Averaged over {ITER} runs:")
    for k, v in total_metrics.items():
        print(f"{k}: {(v/ITER)*1000:.2f} ms")

if __name__ == "__main__":
    run()

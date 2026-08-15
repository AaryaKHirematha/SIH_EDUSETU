import time
import torch
import json
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

sentences = [
    "Solve the quadratic equation using the quadratic formula.",
    "The coefficient of x in the equation is 5.",
    "The derivative of the function is positive.",
    "The mass of the object is exactly 5 kg.",
    "The force acting on the object is constant.",
    "The value of the matrix is calculated using the algorithm.",
    "The chemical formula of water is H₂O.",
    "The equation E = mc² describes the relationship between energy and mass."
]

glossary = {
    "quadratic equation": "ವರ್ಗ ಸಮೀಕರಣ",
    "quadratic formula": "ವರ್ಗ ಸೂತ್ರ",
    "quadratic": "ವರ್ಗ",
    "coefficient": "ಗುಣಾಂಕ",
    "equation": "ಸಮೀಕರಣ",
    "derivative": "ವ್ಯುತ್ಪನ್ನ",
    "function": "ಕಾರ್ಯ",
    "mass": "ದ್ರವ್ಯರಾಶಿ",
    "force": "ಬಲ",
    "matrix": "ಮಾತೃಕೆ",
    "algorithm": "ಅಲ್ಗಾರಿದಮ್",
    "chemical formula": "ರಾಸಾಯನಿಕ ಸೂತ್ರ",
    "energy": "ಶಕ್ತಿ",
    "relationship": "ಸಂಬಂಧ"
}

formulas_and_identifiers = ["E = mc²", "H₂O", "CO₂", "9.8 m/s²", "F = ma", "x"]

model_name = "ai4bharat/indictrans2-en-indic-dist-200M"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token=True)
ip = IndicProcessor(inference=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16, token=True).cuda()
model.eval()

def translate_raw(text):
    batch = ip.preprocess_batch([text], src_lang="eng_Latn", tgt_lang="kan_Knda")
    inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt", max_length=256).to("cuda")
    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=5, num_return_sequences=1, max_length=256)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return ip.postprocess_batch(decoded, lang="kan_Knda")[0]

def get_mappings(text, strategy):
    sorted_terms = sorted(glossary.keys(), key=len, reverse=True)
    sorted_formulas = sorted(formulas_and_identifiers, key=len, reverse=True)
    mapping = {}
    counter = 99901
    protected_text = text
    
    for f in sorted_formulas:
        if f in protected_text:
            ph = str(counter) if strategy == "A" or strategy == "C" else f'"{counter}"'
            mapping[str(counter)] = f
            protected_text = protected_text.replace(f, f" {ph} ")
            counter += 1
            
    for term in sorted_terms:
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        if pattern.search(protected_text):
            ph = str(counter) if strategy == "A" or strategy == "C" else f'"{counter}"'
            mapping[str(counter)] = glossary[term]
            protected_text = pattern.sub(f" {ph} ", protected_text)
            counter += 1
            
    protected_text = re.sub(r'\s+', ' ', protected_text).strip()
    return protected_text, mapping

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

def run_strategy(text, strategy):
    protected_text, mapping = get_mappings(text, strategy)
    translated_text = translate_raw(protected_text)
    
    restored_text = translated_text
    morphology_log = []
    
    for ph_num, tgt_word in mapping.items():
        if strategy == "C":
            # Find attached suffixes: e.g. 99901ರ or 99901ನ್ನು
            pattern_attached = r'\b' + re.escape(ph_num) + r'([^\s.,!?]+)'
            for match in re.finditer(pattern_attached, restored_text):
                suffix = match.group(1)
                joined = kannada_morph_join(tgt_word, suffix)
                restored_text = restored_text.replace(match.group(0), joined)
                morphology_log.append(f"Attached: {suffix} -> {joined}")
                
            # Find detached suffixes: e.g. 99901 ಅನ್ನು
            for match in re.finditer(r'\b' + re.escape(ph_num) + r'\s+([^\s.,!?]+)', restored_text):
                suffix = match.group(1)
                if suffix in known_detached_suffixes:
                    joined = kannada_morph_join(tgt_word, suffix)
                    restored_text = restored_text.replace(match.group(0), joined)
                    morphology_log.append(f"Detached: {suffix} -> {joined}")
            
            # Replace remaining plain placeholders
            restored_text = re.sub(r'\b' + re.escape(ph_num) + r'\b', tgt_word, restored_text)
            
        elif strategy == "B":
            # For B, placeholder is "99901". Suffixes might attach outside quotes
            pattern_attached = r'"' + re.escape(ph_num) + r'"([^\s.,!?]+)?'
            def repl(m):
                suf = m.group(1) or ""
                return tgt_word + (" " + suf if suf else "")
            restored_text = re.sub(pattern_attached, repl, restored_text)
            
            # Detached suffixes
            restored_text = re.sub(r'"' + re.escape(ph_num) + r'"', tgt_word, restored_text)
            
        elif strategy == "A":
            # Simple replacement without morph logic
            pattern_attached = r'\b' + re.escape(ph_num) + r'([^\s.,!?]+)?'
            def repl(m):
                suf = m.group(1) or ""
                return tgt_word + (" " + suf if suf else "")
            restored_text = re.sub(pattern_attached, repl, restored_text)

    restored_text = re.sub(r'\s+([.,!?])', r'\1', restored_text)
    
    return {
        "protected_input": protected_text,
        "translated_output": translated_text,
        "final_output": restored_text,
        "morph_log": morphology_log if strategy == "C" else []
    }

results = []
for i, text in enumerate(sentences):
    raw_kannada = translate_raw(text)
    res_A = run_strategy(text, "A")
    res_B = run_strategy(text, "B")
    res_C = run_strategy(text, "C")
    
    results.append({
        "id": i+1,
        "en": text,
        "raw_kannada": raw_kannada,
        "strategy_A": res_A,
        "strategy_B": res_B,
        "strategy_C": res_C
    })

print(json.dumps(results, ensure_ascii=False, indent=2))

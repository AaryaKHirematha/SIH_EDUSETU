import time
import psutil
import torch
import gc
import json
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

glossary = {
    "quadratic equation": {"hi": "द्विघात समीकरण", "kn": "ವರ್ಗ ಸಮೀಕರಣ"},
    "quadratic formula": {"hi": "द्विघात सूत्र", "kn": "ವರ್ಗ ಸೂತ್ರ"},
    "quadratic": {"hi": "द्विघात", "kn": "ವರ್ಗ"},
    "polynomial": {"hi": "बहुपद", "kn": "ಬಹುಪದ"},
    "algebraic expression": {"hi": "बीजगणितीय व्यंजक", "kn": "ಬೀಜಗಣಿತದ ಅಭಿವ್ಯಕ್ತಿ"},
    "derivative": {"hi": "अवकलज", "kn": "ವ್ಯುತ್ಪನ್ನ"},
    "integration": {"hi": "समाकलन", "kn": "ಅನುಕಲನ"},
    "coefficient": {"hi": "गुणांक", "kn": "ಗುಣಾಂಕ"},
    "coefficients": {"hi": "गुणांकों", "kn": "ಗುಣಾಂಕಗಳು"},
    "variables": {"hi": "चरों", "kn": "ಚರಗಳು"},
    "variable": {"hi": "चर", "kn": "ಚರ"},
    "matrix multiplication": {"hi": "मैट्रिक्स गुणन", "kn": "ಮಾತೃಕೆ ಗುಣಾಕಾರ"},
    "matrix": {"hi": "आव्यूह", "kn": "ಮಾತೃಕೆ"},
    "equation": {"hi": "समीकरण", "kn": "ಸಮೀಕರಣ"},
    "function": {"hi": "फलन", "kn": "ಕಾರ್ಯ"},
    "linear equation": {"hi": "रैखिक समीकरण", "kn": "ರೇಖಾತ್ಮಕ ಸಮೀಕರಣ"},
    "mass": {"hi": "द्रव्यमान", "kn": "ದ್ರವ್ಯರಾಶಿ"},
    "force": {"hi": "बल", "kn": "ಬಲ"},
    "acceleration": {"hi": "त्वरण", "kn": "ವೇಗವರ್ಧನೆ"},
    "velocity": {"hi": "वेग", "kn": "ವೇಗ"},
    "momentum": {"hi": "संवेग", "kn": "ಆವೇಗ"},
    "gravity": {"hi": "गुरुत्वाकर्षण", "kn": "ಗುರುತ್ವಾಕರ್ಷಣೆ"},
    "molecule": {"hi": "अणु", "kn": "ಅಣು"},
    "atom": {"hi": "परमाणु", "kn": "ಪರಮಾಣು"},
    "chemical formula": {"hi": "रासायनिक सूत्र", "kn": "ರಾಸಾಯನಿಕ ಸೂತ್ರ"},
    "algorithm": {"hi": "एल्गोरिदम", "kn": "ಅಲ್ಗಾರಿದಮ್"},
    "framework": {"hi": "फ्रेमवर्क", "kn": "ಚೌಕಟ್ಟು"},
    "database": {"hi": "डेटाबेस", "kn": "ದತ್ತಸಂಚಯ"}
}

formulas_and_identifiers = [
    "E = mc²",
    "F = ma",
    "H₂O",
    "CO₂",
    "9.8 m/s²",
    "Python",
    "NumPy",
    "HTML",
    "CSS",
    "TensorFlow"
]

sentences = [
    "The quadratic equation can be solved using the quadratic formula.",
    "The mass of the object is exactly 5 kg.",
    "Force is equal to mass times acceleration.",
    "A polynomial is an algebraic expression consisting of variables and coefficients.",
    "The derivative of a function represents its rate of change.",
    "Integration is used to calculate area under a curve.",
    "The famous equation is E = mc².",
    "Gravity on Earth is approximately 9.8 m/s².",
    "The chemical formula for water is H₂O.",
    "Python and NumPy are used for matrix multiplication."
]

def get_ram_mb():
    return psutil.virtual_memory().used / (1024 * 1024)

def get_vram_mb():
    if torch.cuda.is_available():
        torch.cuda.synchronize()
        return torch.cuda.memory_allocated() / (1024 * 1024)
    return 0

model_name = "ai4bharat/indictrans2-en-indic-dist-200M"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token=True)
ip = IndicProcessor(inference=True)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16, token=True).cuda()
model.eval()

def translate_raw(text, src_lang, tgt_lang):
    batch = ip.preprocess_batch([text], src_lang=src_lang, tgt_lang=tgt_lang)
    inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt", max_length=256).to("cuda")
    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=5, num_return_sequences=1, max_length=256)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return ip.postprocess_batch(decoded, lang=tgt_lang)[0]

def protect_and_translate(text, tgt_lang_code):
    # Sort terms by length to match multi-word terms first
    sorted_terms = sorted(glossary.keys(), key=len, reverse=True)
    sorted_formulas = sorted(formulas_and_identifiers, key=len, reverse=True)
    
    mapping = {}
    counter = 99901
    
    protected_text = text
    
    # Protect formulas first
    for f in sorted_formulas:
        if f in protected_text:
            placeholder = str(counter)
            mapping[placeholder] = f
            protected_text = protected_text.replace(f, f" {placeholder} ")
            counter += 1
            
    # Protect glossary terms
    # We use word boundaries \b to avoid partial matches, ignoring case
    for term in sorted_terms:
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        if pattern.search(protected_text):
            placeholder = str(counter)
            # Find all instances and replace
            tgt_term = glossary[term][tgt_lang_code]
            mapping[placeholder] = tgt_term
            protected_text = pattern.sub(f" {placeholder} ", protected_text)
            counter += 1
            
    # Clean up multiple spaces
    protected_text = re.sub(r'\s+', ' ', protected_text).strip()
    
    # Translate
    raw_tgt_lang = "hin_Deva" if tgt_lang_code == "hi" else "kan_Knda"
    translated_text = translate_raw(protected_text, "eng_Latn", raw_tgt_lang)
    
    # Restore placeholders
    restored_text = translated_text
    for placeholder, tgt_word in mapping.items():
        # Placeholders might be attached to punctuation in translation
        # Replace the numeric placeholder with the target word
        restored_text = re.sub(r'\b' + re.escape(placeholder) + r'\b', tgt_word, restored_text)
        
    # Clean up spaces around punctuation (optional but good for fluency)
    restored_text = re.sub(r'\s+([.,!?])', r'\1', restored_text)
    
    return translated_text, restored_text, mapping

results = []
metrics = {
    "peak_vram": 0,
    "peak_ram": 0,
}

for i, text in enumerate(sentences):
    # Hindi Raw
    hi_raw = translate_raw(text, "eng_Latn", "hin_Deva")
    # Hindi Protected
    hi_translated_protected, hi_protected, hi_mapping = protect_and_translate(text, "hi")
    
    # Kannada Raw
    kn_raw = translate_raw(text, "eng_Latn", "kan_Knda")
    # Kannada Protected
    kn_translated_protected, kn_protected, kn_mapping = protect_and_translate(text, "kn")
    
    results.append({
        "id": i + 1,
        "en": text,
        "hi_raw": hi_raw,
        "hi_protected": hi_protected,
        "hi_mapping": hi_mapping,
        "hi_translated_protected": hi_translated_protected,
        "kn_raw": kn_raw,
        "kn_protected": kn_protected,
        "kn_mapping": kn_mapping,
        "kn_translated_protected": kn_translated_protected
    })

if torch.cuda.is_available():
    metrics["peak_vram"] = torch.cuda.max_memory_allocated() / (1024 * 1024)
metrics["peak_ram"] = get_ram_mb()

print(json.dumps({"metrics": metrics, "results": results}, ensure_ascii=False, indent=2))

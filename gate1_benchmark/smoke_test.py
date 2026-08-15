import os
import time
import shutil
import psutil
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor
import gc

def get_dir_size(path="."):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def get_disk_free():
    return shutil.disk_usage("/mnt/d/SIH").free / (1024**3)

def measure_vram():
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated(0) / (1024**2)
        reserved = torch.cuda.memory_reserved(0) / (1024**2)
        return allocated, reserved
    return 0, 0

def get_ram():
    return psutil.virtual_memory().used / (1024**3)

def translate(sentences, src_lang, tgt_lang, model, tokenizer, ip):
    # Preprocess
    batch = ip.preprocess_batch(sentences, src_lang=src_lang, tgt_lang=tgt_lang)
    
    # Tokenize
    inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        return_attention_mask=True,
    ).to(model.device)
    
    # Generate
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=5,
            num_return_sequences=1,
        )
    
    # Decode
    with tokenizer.as_target_tokenizer():
        generated_tokens = tokenizer.batch_decode(
            generated_tokens.detach().cpu().tolist(),
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )
    
    # Postprocess
    translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)
    return translations

def run_smoke_test():
    print("="*50)
    print("INDIC TRANS 2 200M SMOKE TEST")
    print("="*50)
    
    model_id = "ai4bharat/indictrans2-en-indic-dist-200M"
    print(f"Model ID: {model_id}")
    
    # Measure initial state
    disk_before = get_disk_free()
    ram_before = get_ram()
    vram_alloc_before, vram_res_before = measure_vram()
    
    print(f"Disk Free Before: {disk_before:.2f} GB")
    print(f"RAM Before: {ram_before:.2f} GB")
    print(f"VRAM Allocated Before: {vram_alloc_before:.2f} MB")
    
    print("\n--- Downloading/Loading Model ---")
    torch.cuda.empty_cache()
    
    start_load = time.time()
    
    ip = IndicProcessor(inference=True)
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    
    try:
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_id, 
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="cuda"
        )
    except Exception as e:
        print(f"FATAL: Model load failed: {e}")
        return
        
    load_time = time.time() - start_load
    
    disk_after = get_disk_free()
    ram_after = get_ram()
    vram_alloc_after, vram_res_after = measure_vram()
    
    print(f"Load Time: {load_time:.2f} seconds")
    print(f"Model Device: {model.device}")
    print(f"Model dtype: {model.dtype}")
    print(f"Disk Free After: {disk_after:.2f} GB (Used roughly: {disk_before - disk_after:.2f} GB)")
    print(f"RAM After: {ram_after:.2f} GB")
    print(f"VRAM Allocated After: {vram_alloc_after:.2f} MB")
    
    # Test Data
    test_sentences = [
        "Education is the key to unlocking the world, a passport to freedom.",
        "Newton's second law of motion states that force equals mass times acceleration (F = ma).",
        "The quadratic formula is used to solve equations of the form ax^2 + bx + c = 0.",
        "The mitochondria is known as the powerhouse of the cell, generating ATP.",
        "A machine learning algorithm can be trained using a large dataset to recognize patterns."
    ]
    
    tech_sentences = [
        "import numpy as np; arr = np.zeros(10)",
        "The formula for Einstein's mass-energy equivalence is E = mc².",
        "During photosynthesis, plants convert CO₂ and H₂O into glucose and oxygen.",
        "Acceleration due to gravity is approximately 9.8 m/s².",
        "The concentration increased by 45.5% over a period of 10 days."
    ]
    
    src_lang = "eng_Latn"
    
    print("\n--- Kannada (kan_Knda) Translation Test ---")
    tgt_lang_kn = "kan_Knda"
    
    start_kn = time.time()
    kan_translations = translate(test_sentences, src_lang, tgt_lang_kn, model, tokenizer, ip)
    latency_kn = time.time() - start_kn
    print(f"Kannada Latency: {latency_kn:.2f} seconds")
    
    for i, (src, tgt) in enumerate(zip(test_sentences, kan_translations)):
        print(f"\n[EN {i+1}]: {src}")
        print(f"[KN {i+1}]: {tgt}")
        
    print("\n--- Hindi (hin_Deva) Translation Test ---")
    tgt_lang_hi = "hin_Deva"
    
    start_hi = time.time()
    hin_translations = translate(test_sentences, src_lang, tgt_lang_hi, model, tokenizer, ip)
    latency_hi = time.time() - start_hi
    print(f"Hindi Latency: {latency_hi:.2f} seconds")
    
    for i, (src, tgt) in enumerate(zip(test_sentences, hin_translations)):
        print(f"\n[EN {i+1}]: {src}")
        print(f"[HI {i+1}]: {tgt}")
        
    print("\n--- Technical Content Test (Kannada & Hindi) ---")
    
    tech_kn = translate(tech_sentences, src_lang, tgt_lang_kn, model, tokenizer, ip)
    tech_hi = translate(tech_sentences, src_lang, tgt_lang_hi, model, tokenizer, ip)
    
    for i, (src, kn, hi) in enumerate(zip(tech_sentences, tech_kn, tech_hi)):
        print(f"\n[EN Tech {i+1}]: {src}")
        print(f"[KN Tech {i+1}]: {kn}")
        print(f"[HI Tech {i+1}]: {hi}")
        
    peak_vram = torch.cuda.max_memory_allocated(0) / (1024**2)
    print(f"\nPeak VRAM during inference: {peak_vram:.2f} MB")
    
    print("\nSMOKE TEST SCRIPT COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    run_smoke_test()

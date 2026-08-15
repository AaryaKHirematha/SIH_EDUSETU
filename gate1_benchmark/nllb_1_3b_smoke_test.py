import os
import time
import shutil
import psutil
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import gc
import statistics

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

def translate(sentences, src_lang, tgt_lang, model, tokenizer):
    tokenizer.src_lang = src_lang
    inputs = tokenizer(sentences, return_tensors="pt", padding=True, truncation=True, max_length=512).to(model.device)
    tgt_lang_id = tokenizer.lang_code_to_id[tgt_lang]
    
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tgt_lang_id,
            max_length=512,
            num_beams=5
        )
        
    translations = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return translations

def run_smoke_test():
    print("="*50)
    print("NLLB-200 1.3B SMOKE TEST")
    print("="*50)
    
    model_id = "facebook/nllb-200-1.3B"
    print(f"Model ID: {model_id}")
    
    disk_before = get_disk_free()
    ram_before = get_ram()
    vram_alloc_before, vram_res_before = measure_vram()
    
    print(f"Disk Free Before: {disk_before:.2f} GB")
    print(f"RAM Before: {ram_before:.2f} GB")
    print(f"VRAM Allocated Before: {vram_alloc_before:.2f} MB")
    
    print("\n--- Downloading/Loading Model ---")
    torch.cuda.empty_cache()
    
    start_load = time.time()
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    try:
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_id, 
            torch_dtype=torch.float16
        ).to("cuda")
    except Exception as e:
        print(f"FATAL: Model load failed: {e}")
        return
        
    load_time = time.time() - start_load
    
    disk_after = get_disk_free()
    ram_after = get_ram()
    vram_alloc_after, vram_res_after = measure_vram()
    
    print(f"Load Time (includes download): {load_time:.2f} seconds")
    print(f"Model Device: {model.device}")
    print(f"Model dtype: {model.dtype}")
    print(f"Disk Free After: {disk_after:.2f} GB (Used roughly: {disk_before - disk_after:.2f} GB)")
    print(f"RAM After: {ram_after:.2f} GB")
    print(f"VRAM Allocated After: {vram_alloc_after:.2f} MB")
    
    src_lang = "eng_Latn"
    
    def test_translation(name, sents, tgt_lang):
        print(f"\n--- {name} ({tgt_lang}) ---")
        translations = translate(sents, src_lang, tgt_lang, model, tokenizer)
        for i, (src, tgt) in enumerate(zip(sents, translations)):
            print(f"\n[EN {i+1}]: {src}")
            print(f"[{tgt_lang[:3].upper()} {i+1}]: {tgt}")

    # 7. CONTROLLED TERMINOLOGY TEST
    controlled_sents = [
        "Force is equal to mass times acceleration.",
        "The quadratic equation can be solved using the quadratic formula.",
        "The chemical formula for water is H₂O and for carbon dioxide is CO₂.",
        "The famous equation is E = mc².",
        "Gravity on Earth is approximately 9.8 m/s².",
        "We use Python and NumPy for matrix multiplication."
    ]
    test_translation("Controlled Terminology", controlled_sents, "kan_Knda")
    test_translation("Controlled Terminology", controlled_sents, "hin_Deva")

    # 8. CONTEXT SENSITIVITY TEST (MASS)
    mass_sents = [
        "Mass is a measure of the amount of matter in an object.",
        "Force is equal to mass times acceleration.",
        "The mass of the object is exactly 5 kg."
    ]
    test_translation("Mass Context", mass_sents, "kan_Knda")
    test_translation("Mass Context", mass_sents, "hin_Deva")

    # 9. QUADRATIC TEST
    quad_sents = [
        "The quadratic equation has two roots.",
        "The quadratic formula is used to solve the equation.",
        "The graph of a quadratic function is a parabola.",
        "The quadratic term is x²."
    ]
    test_translation("Quadratic Context", quad_sents, "kan_Knda")
    test_translation("Quadratic Context", quad_sents, "hin_Deva")

    # 10. TECHNICAL CONTENT (Extra requested elements not already covered)
    tech_sents = [
        "TensorFlow is great.",
        "HTML and CSS are used for web.",
        "DNA and RNA are nucleic acids.",
        "The efficiency increased by 25%."
    ]
    test_translation("Technical/Extra Content", tech_sents, "kan_Knda")
    test_translation("Technical/Extra Content", tech_sents, "hin_Deva")

    # 12. PERFORMANCE
    print("\n--- Latency Test ---")
    latency_sents = ["Education is the passport to the future."]
    
    # First inference
    start = time.time()
    translate(latency_sents, src_lang, "kan_Knda", model, tokenizer)
    first_kan = time.time() - start
    
    start = time.time()
    translate(latency_sents, src_lang, "hin_Deva", model, tokenizer)
    first_hin = time.time() - start
    
    print(f"First Inference Kannada: {first_kan:.2f}s")
    print(f"First Inference Hindi: {first_hin:.2f}s")
    
    # Warmup
    for _ in range(2):
        translate(latency_sents, src_lang, "kan_Knda", model, tokenizer)
        translate(latency_sents, src_lang, "hin_Deva", model, tokenizer)
        
    # Measured runs
    kan_latencies = []
    hin_latencies = []
    
    for _ in range(3):
        start = time.time()
        translate(latency_sents, src_lang, "kan_Knda", model, tokenizer)
        kan_latencies.append(time.time() - start)
        
        start = time.time()
        translate(latency_sents, src_lang, "hin_Deva", model, tokenizer)
        hin_latencies.append(time.time() - start)
        
    print(f"\nKannada Warm Latency - Mean: {statistics.mean(kan_latencies):.2f}s, Min: {min(kan_latencies):.2f}s, Max: {max(kan_latencies):.2f}s")
    print(f"Hindi Warm Latency   - Mean: {statistics.mean(hin_latencies):.2f}s, Min: {min(hin_latencies):.2f}s, Max: {max(hin_latencies):.2f}s")
    
    peak_vram = torch.cuda.max_memory_allocated(0) / (1024**2)
    print(f"\nPeak VRAM during inference: {peak_vram:.2f} MB")
    
    print("\nSMOKE TEST SCRIPT COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    run_smoke_test()

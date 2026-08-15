import os
import time
import shutil
import psutil
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
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
    print("NLLB-200 DISTILLED 600M SMOKE TEST")
    print("="*50)
    
    model_id = "facebook/nllb-200-distilled-600M"
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
    
    print(f"Load Time: {load_time:.2f} seconds")
    print(f"Model Device: {model.device}")
    print(f"Model dtype: {model.dtype}")
    print(f"Disk Free After: {disk_after:.2f} GB (Used roughly: {disk_before - disk_after:.2f} GB)")
    print(f"RAM After: {ram_after:.2f} GB")
    print(f"VRAM Allocated After: {vram_alloc_after:.2f} MB")
    
    # Test Data
    test_sentences = [
        "Force is equal to mass times acceleration.",
        "The quadratic equation can be solved using the quadratic formula.",
        "Cells contain DNA which carries genetic information.",
        "A molecule of water is formed by two hydrogen atoms and one oxygen atom.",
        "An algorithm is a step-by-step procedure for solving a problem or performing a computation."
    ]
    
    tech_sentences = [
        "We use Python and NumPy for matrix multiplication.",
        "TensorFlow is an open-source machine learning framework.",
        "The web page is styled using HTML and CSS.",
        "The process of transcription produces RNA from DNA.",
        "The chemical formula for water is H₂O and for carbon dioxide is CO₂.",
        "The famous equation is E = mc².",
        "According to Newton's second law, F = ma.",
        "Gravity on Earth is approximately 9.8 m/s².",
        "The efficiency of the new engine increased by 25%.",
        "The mass of the object is exactly 5 kg."
    ]
    
    length_sentences = [
        "Education is the passport to the future.",
        "Education is the passport to the future, for tomorrow belongs to those who prepare for it today. Learning is a continuous process that enriches our lives and helps us adapt to an ever-changing world.",
        "Education is the passport to the future, for tomorrow belongs to those who prepare for it today. Learning is a continuous process that enriches our lives and helps us adapt to an ever-changing world. It is not merely about acquiring facts, but about developing critical thinking and problem-solving skills. Through education, individuals are empowered to make informed decisions and contribute meaningfully to society. Furthermore, a strong educational foundation fosters innovation and drives economic progress on a global scale. Therefore, investing in quality education is essential for the sustainable development of any nation."
    ]
    
    src_lang = "eng_Latn"
    
    def test_translation(name, sents, tgt_lang):
        print(f"\n--- {name} ({tgt_lang}) ---")
        start = time.time()
        translations = translate(sents, src_lang, tgt_lang, model, tokenizer)
        latency = time.time() - start
        print(f"Latency: {latency:.2f} seconds")
        for i, (src, tgt) in enumerate(zip(sents, translations)):
            print(f"\n[EN {i+1}]: {src}")
            print(f"[{tgt_lang[:3].upper()} {i+1}]: {tgt}")
        return latency

    latency_kn = test_translation("Kannada Basic Test", test_sentences, "kan_Knda")
    latency_hi = test_translation("Hindi Basic Test", test_sentences, "hin_Deva")
    
    test_translation("Kannada Technical Test", tech_sentences, "kan_Knda")
    test_translation("Hindi Technical Test", tech_sentences, "hin_Deva")
    
    test_translation("Kannada Length Test", length_sentences, "kan_Knda")
    test_translation("Hindi Length Test", length_sentences, "hin_Deva")
    
    peak_vram = torch.cuda.max_memory_allocated(0) / (1024**2)
    print(f"\nPeak VRAM during inference: {peak_vram:.2f} MB")
    
    print("\nSMOKE TEST SCRIPT COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    run_smoke_test()

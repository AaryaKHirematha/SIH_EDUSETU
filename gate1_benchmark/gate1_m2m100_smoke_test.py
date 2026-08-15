import time
import os
import psutil
import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from huggingface_hub import snapshot_download

MODEL_ID = "facebook/m2m100_418M"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

test_sentences = [
    "Force is equal to mass times acceleration.",
    "The mass of the object is exactly 5 kg.",
    "Acceleration is the rate of change of velocity.",
    "Newton's second law relates force, mass, and acceleration.",
    "The quadratic equation can be solved using the quadratic formula.",
    "A polynomial is an algebraic expression containing variables and coefficients.",
    "The derivative represents the rate of change of a function.",
    "Integration is the reverse process of differentiation.",
    "The chemical formula for water is H₂O.",
    "Carbon dioxide contains one carbon atom and two oxygen atoms.",
    "We use Python and NumPy for matrix multiplication.",
    "TensorFlow is an open-source machine learning framework.",
    "An algorithm is a step-by-step procedure for solving a problem.",
    "E = mc²",
    "F = ma",
    "H₂O",
    "CO₂",
    "9.8 m/s²"
]

medium_paragraph = "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy that, through cellular respiration, can later be released to fuel the organism's activities. Some of this chemical energy is stored in carbohydrate molecules, such as sugars and starches, which are synthesized from carbon dioxide and water – hence the name photosynthesis, from the Greek phōs, \"light\", and synthesis, \"putting together\"."

def get_vram_usage():
    if torch.cuda.is_available():
        return torch.cuda.memory_allocated() / (1024 ** 2)
    return 0

def get_peak_vram_usage():
    if torch.cuda.is_available():
        return torch.cuda.max_memory_allocated() / (1024 ** 2)
    return 0

def get_ram_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 2)

def main():
    print("=== M2M100 418M Smoke Test ===")
    print(f"Device: {DEVICE}")
    print(f"dtype: {DTYPE}")
    
    # 1. Measure Download Time
    print("\n--- Downloading Model ---")
    t0 = time.time()
    snapshot_download(repo_id=MODEL_ID)
    download_time = time.time() - t0
    print(f"Download time: {download_time:.2f} s")
    
    # 2. VRAM and RAM before loading
    vram_before = get_vram_usage()
    ram_before = get_ram_usage()
    print(f"\nVRAM before load: {vram_before:.2f} MB")
    print(f"RAM before load: {ram_before:.2f} MB")
    
    # 3. Measure Load Time
    print("\n--- Loading Model ---")
    t0 = time.time()
    tokenizer = M2M100Tokenizer.from_pretrained(MODEL_ID)
    model = M2M100ForConditionalGeneration.from_pretrained(MODEL_ID, torch_dtype=DTYPE)
    model.to(DEVICE)
    model.eval()
    load_time = time.time() - t0
    
    vram_after = get_vram_usage()
    ram_after = get_ram_usage()
    print(f"Load time: {load_time:.2f} s")
    print(f"VRAM after load: {vram_after:.2f} MB")
    print(f"RAM after load: {ram_after:.2f} MB")
    
    tokenizer.src_lang = "en"
    
    def translate(text, target_lang):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(DEVICE)
        t_start = time.time()
        with torch.no_grad():
            generated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=tokenizer.get_lang_id(target_lang),
                max_new_tokens=256
            )
        t_end = time.time()
        result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return result, (t_end - t_start)
    
    print("\n--- Inference Latency Test (English -> Hindi) ---")
    test_sent = "Force is equal to mass times acceleration."
    
    # Cold inference
    res, cold_latency = translate([test_sent], "hi")
    print(f"Cold inference latency: {cold_latency:.4f} s")
    
    # Warm inference 1
    res, w1 = translate([test_sent], "hi")
    print(f"Warm inference 1 latency: {w1:.4f} s")
    
    # Warm inference 2
    res, w2 = translate([test_sent], "hi")
    print(f"Warm inference 2 latency: {w2:.4f} s")
    
    # Warm inference 3
    res, w3 = translate([test_sent], "hi")
    print(f"Warm inference 3 latency: {w3:.4f} s")
    
    warm_latencies = [w1, w2, w3]
    mean_warm = sum(warm_latencies) / len(warm_latencies)
    median_warm = sorted(warm_latencies)[len(warm_latencies)//2]
    print(f"Mean warm latency: {mean_warm:.4f} s")
    print(f"Median warm latency: {median_warm:.4f} s")
    
    print("\n--- Full Sentence Tests (English -> Hindi) ---")
    for s in test_sentences:
        res, _ = translate([s], "hi")
        print(f"EN: {s}")
        print(f"HI: {res[0]}")
        print("-")
        
    print("\n--- Full Sentence Tests (English -> Kannada) ---")
    for s in test_sentences:
        res, _ = translate([s], "kn")
        print(f"EN: {s}")
        print(f"KN: {res[0]}")
        print("-")
        
    print("\n--- Medium Paragraph Test (English -> Hindi) ---")
    res, _ = translate([medium_paragraph], "hi")
    print(f"EN: {medium_paragraph}")
    print(f"HI: {res[0]}")
    print("-")
    
    print("\n--- Medium Paragraph Test (English -> Kannada) ---")
    res, _ = translate([medium_paragraph], "kn")
    print(f"EN: {medium_paragraph}")
    print(f"KN: {res[0]}")
    print("-")
    
    peak_vram = get_peak_vram_usage()
    print(f"\nPeak VRAM usage: {peak_vram:.2f} MB")

if __name__ == "__main__":
    main()

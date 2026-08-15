import time
import psutil
import torch
import gc
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

sentences = [
    "Force is equal to mass times acceleration.",
    "The mass of the object is exactly 5 kg.",
    "The velocity of an object changes when a force is applied.",
    "Momentum is equal to mass times velocity.",
    "The quadratic equation can be solved using the quadratic formula.",
    "A polynomial is an algebraic expression consisting of variables and coefficients.",
    "The derivative of a function represents its rate of change.",
    "Integration is used to calculate area under a curve.",
    "A matrix is a rectangular arrangement of numbers.",
    "The coefficient of x in the equation is 5.",
    "A molecule of water is formed by two hydrogen atoms and one oxygen atom.",
    "The chemical formula for water is H₂O and for carbon dioxide is CO₂.",
    "An atom consists of a nucleus surrounded by electrons.",
    "An algorithm is a step-by-step procedure for solving a problem.",
    "Python and NumPy are used for matrix multiplication.",
    "TensorFlow is an open-source machine learning framework.",
    "The web page is styled using HTML and CSS.",
    "A database stores and retrieves structured information.",
    "The famous equation is E = mc².",
    "Gravity on Earth is approximately 9.8 m/s².",
    "F = ma.",
    "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy that, through cellular respiration, can later be released to fuel the organism's activities. Some of this chemical energy is stored in carbohydrate molecules, such as sugars and starches, which are synthesized from carbon dioxide and water – hence the name photosynthesis, from the Greek phōs, \"light\", and synthesis, \"putting together\"."
]

def get_ram_mb():
    return psutil.virtual_memory().used / (1024 * 1024)

def get_vram_mb():
    if torch.cuda.is_available():
        torch.cuda.synchronize()
        return torch.cuda.memory_allocated() / (1024 * 1024)
    return 0

model_name = "ai4bharat/indictrans2-en-indic-dist-200M"

print("--- Initializing Tokenizer & Processor ---")
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token=True)
ip = IndicProcessor(inference=True)

ram_before_load = get_ram_mb()
vram_before_load = get_vram_mb()

t0 = time.time()
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16, token=True).cuda()
model.eval()
load_time = time.time() - t0

ram_after_load = get_ram_mb()
vram_after_load = get_vram_mb()

def translate_indic_single(text, src_lang, tgt_lang):
    batch = ip.preprocess_batch([text], src_lang=src_lang, tgt_lang=tgt_lang)
    inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt", max_length=256).to("cuda")
    
    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=5, num_return_sequences=1, max_length=256)
        
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return ip.postprocess_batch(decoded, lang=tgt_lang)[0]


results = []
metrics = {
    "load_time": load_time,
    "ram_before_load": ram_before_load,
    "ram_after_load": ram_after_load,
    "vram_before_load": vram_before_load,
    "vram_after_load": vram_after_load,
    "cold_latency": None,
    "warm_latencies": [],
    "peak_vram": 0,
    "peak_ram": 0,
}

# Warmup / Cold latency
print("--- Cold Inference ---")
ram_before_inf = get_ram_mb()
vram_before_inf = get_vram_mb()

t0 = time.time()
_ = translate_indic_single(sentences[0], "eng_Latn", "hin_Deva")
metrics["cold_latency"] = time.time() - t0

ram_after_inf = get_ram_mb()
vram_after_inf = get_vram_mb()
metrics["ram_after_inf"] = ram_after_inf
metrics["vram_after_inf"] = vram_after_inf

print("--- Testing Sentences ---")
for i, text in enumerate(sentences):
    # Hindi
    t0 = time.time()
    hi = translate_indic_single(text, "eng_Latn", "hin_Deva")
    hi_latency = time.time() - t0
    
    if i > 0:
        metrics["warm_latencies"].append(hi_latency)

    # Kannada
    t0 = time.time()
    kn = translate_indic_single(text, "eng_Latn", "kan_Knda")
    kn_latency = time.time() - t0
    
    metrics["warm_latencies"].append(kn_latency)

    results.append({
        "id": i + 1,
        "en": text,
        "hi": hi,
        "kn": kn
    })

if torch.cuda.is_available():
    metrics["peak_vram"] = torch.cuda.max_memory_allocated() / (1024 * 1024)
metrics["peak_ram"] = get_ram_mb()

print(json.dumps({"metrics": metrics, "results": results}, ensure_ascii=False, indent=2))

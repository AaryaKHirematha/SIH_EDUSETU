import json
import time
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit.processor import IndicProcessor

MODEL_PATH = str(Path.home() / ".cache/huggingface/hub/models--ai4bharat--indictrans2-en-indic-dist-200M/snapshots/173b94239f7c38886b2747b8d4a5db771a7e1232")

REFERENCE_FILE = "gate2_human_validated_references.json"
OUTPUT_FILE = "gate2_model_outputs_200M_GPU.json"

DEVICE = "cuda"
DTYPE = torch.float16

print("=" * 80)
print("EDUSETU — GATE 2 MODEL BENCHMARK")
print("=" * 80)

print("Model:", MODEL_PATH)
print("Device:", DEVICE)
print("CUDA:", torch.cuda.is_available())

with open(REFERENCE_FILE, encoding="utf-8") as f:
    references = json.load(f)

print("Reference items:", len(references))

print("\nLoading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    local_files_only=True,
)

print("Loading model...")
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    local_files_only=True,
    torch_dtype=DTYPE,
).to(DEVICE)

model.eval()
ip = IndicProcessor(inference=True)

print("Model loaded successfully.")

def translate(texts, target_lang):
    batch = ip.preprocess_batch(
        texts,
        src_lang="eng_Latn",
        tgt_lang=target_lang,
    )

    encoded = tokenizer(
        batch,
        padding=True,
        truncation=True,
        return_tensors="pt",
    ).to(DEVICE)

    with torch.no_grad():
        generated = model.generate(
            **encoded,
            num_beams=5,
            max_length=256,
            do_sample=False,
        )

    decoded = tokenizer.batch_decode(
        generated,
        skip_special_tokens=True,
    )

    return ip.postprocess_batch(
        decoded,
        lang=target_lang,
    )

outputs = []

total = len(references)

for i, item in enumerate(references, 1):
    source = item["source_en"]

    print(f"\n[{i}/{total}] {item['id']}")
    print("EN:", source)

    result = {
        "id": item["id"],
        "source_en": source,
    }

    for lang in ["hin_Deva", "kan_Knda"]:
        start = time.time()

        try:
            translation = translate([source], lang)[0]
            elapsed = time.time() - start

            result[lang] = translation
            result[f"{lang}_latency_s"] = round(elapsed, 4)

            print(f"{lang}: {translation}")
            print(f"Latency: {elapsed:.3f}s")

        except Exception as e:
            result[lang] = ""
            result[f"{lang}_latency_s"] = None
            result[f"{lang}_error"] = str(e)

            print(f"{lang}: ERROR")
            print(e)

    outputs.append(result)

    if DEVICE == "cuda":
        torch.cuda.empty_cache()

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(outputs, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 80)
print("GATE 2 TRANSLATION COMPLETE")
print("=" * 80)
print("Items:", len(outputs))
print("Hindi translations:", sum(bool(x.get("hin_Deva")) for x in outputs))
print("Kannada translations:", sum(bool(x.get("kan_Knda")) for x in outputs))
print("Output:", OUTPUT_FILE)

import requests

models_to_check = [
    "facebook/nllb-200-distilled-600M",
    "facebook/nllb-200-1.3B",
    "facebook/m2m100_418M",
    "facebook/mbart-large-50-many-to-many-mmt",
    "ai4bharat/indictrans-en-indic",
    "google/madlad400-3b-mt"
]

print(f"{'Model':<45} | {'Gated?':<7} | {'Downloads':<10} | {'Tags'}")
print("-" * 100)

for model in models_to_check:
    url = f"https://huggingface.co/api/models/{model}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        gated = data.get("gated", False)
        downloads = data.get("downloads", 0)
        tags = data.get("tags", [])
        pipeline = data.get("pipeline_tag", "")
        # Get safetensors size if available
        size = "Unknown"
        if "safetensors" in data:
            try:
                size = data["safetensors"]["total"] / (1024**3)
                size = f"{size:.2f} GB"
            except:
                pass
        
        # Checking gated via direct config access to be absolutely sure
        config_url = f"https://huggingface.co/{model}/resolve/main/config.json"
        config_r = requests.head(config_url)
        actually_gated = "YES" if config_r.status_code in (401, 403) else "NO"
        
        print(f"{model:<45} | {actually_gated:<7} | {downloads:<10} | {size}")
    else:
        print(f"{model:<45} | ERROR {r.status_code}")


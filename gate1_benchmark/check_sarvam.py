import requests

def check_model(model):
    url = f"https://huggingface.co/api/models/{model}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        gated = data.get("gated", False)
        downloads = data.get("downloads", 0)
        tags = data.get("tags", [])
        
        size = "Unknown"
        if "safetensors" in data:
            try:
                size = data["safetensors"]["total"] / (1024**3)
                size = f"{size:.2f} GB"
            except:
                pass
        
        config_url = f"https://huggingface.co/{model}/resolve/main/config.json"
        config_r = requests.head(config_url)
        actually_gated = "YES" if config_r.status_code in (401, 403) else "NO"
        
        print(f"{model:<35} | Gated: {actually_gated:<3} | Size: {size:<7} | Downloads: {downloads:<8}")
    else:
        print(f"{model} -> ERROR {r.status_code}")

check_model("sarvamai/sarvam-translate")
check_model("alirezamsh/small100")
check_model("Helsinki-NLP/opus-mt-en-dra")

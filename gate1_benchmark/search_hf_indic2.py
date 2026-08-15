import requests

def check_models(query):
    url = f"https://huggingface.co/api/models?search={query}&limit=20"
    r = requests.get(url)
    if r.status_code == 200:
        models = r.json()
        for m in models:
            model_id = m['modelId']
            print(f"{model_id}")

print("--- Helsinki-NLP ---")
check_models("Helsinki-NLP/opus-mt-en-")
print("--- cfilt ---")
check_models("cfilt")
print("--- anuvaad ---")
check_models("anuvaad")
print("--- AI4Bharat indictrans ---")
check_models("ai4bharat/indictrans")

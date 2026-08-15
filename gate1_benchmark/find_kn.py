import requests
url = 'https://huggingface.co/api/models?filter=translation,kn&sort=downloads&direction=-1'
r = requests.get(url)
models = r.json()
for m in models[:20]:
    print(f"{m['modelId']:<45} | {m.get('downloads', 0):<8}")

import requests
url = 'https://huggingface.co/api/models?author=ai4bharat'
r = requests.get(url)
models = [m['modelId'] for m in r.json()]
for m in models:
    if 'trans' in m.lower():
        print(m)

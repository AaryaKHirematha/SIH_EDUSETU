import requests

queries = ["indictrans", "kannada translation", "indic mt", "bhashini", "samanantar"]

seen = set()
for q in queries:
    url = f"https://huggingface.co/api/models?search={q}&sort=downloads&direction=-1&limit=20"
    r = requests.get(url)
    if r.status_code == 200:
        models = r.json()
        for m in models:
            model_id = m['modelId']
            if model_id not in seen:
                seen.add(model_id)
                # Check if it's an encoder-decoder or translation model
                pipeline = m.get('pipeline_tag', 'Unknown')
                downloads = m.get('downloads', 0)
                print(f"{model_id:<40} | {pipeline:<20} | Downloads: {downloads}")
    else:
        print(f"Error querying {q}: {r.status_code}")

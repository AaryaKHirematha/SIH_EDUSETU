import json
data = json.load(open('/mnt/d/SIH/gate1_benchmark/gate3b_results.json', encoding='utf-8'))
for x in data:
    if not x['C']['morphology_pass']:
        print(f"ID: {x['id']}")
        print(f"Output: {x['C']['output']}")
        print(f"Matches: {x['C']['detached_matches']}")

import json
import re

def analyze_failures():
    with open('/mnt/d/SIH/gate1_benchmark/gate3a_ai_review_results.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    morph_fails = [x for x in data if x['kannada']['C']['scores']['morphology'] == 'FAIL']
    
    print(f"Total morphology failures: {len(morph_fails)}")
    
    for case in morph_fails:
        out_text = case['kannada']['C']['output']
        detached = re.findall(r'\b([^\s.,!?]+)\s+(ಅನ್ನು|ವನ್ನು|ಯನ್ನು|ರ|ದ|ಗೆ|ಕ್ಕೆ|ಇಂದ|ದಿಂದ|ಲ್ಲಿ|ದಲ್ಲಿ)\b', out_text)
        print(f"ID: {case['id']}")
        print(f"Output: {out_text}")
        print(f"Detached: {detached}")
        print("-" * 50)

if __name__ == "__main__":
    analyze_failures()

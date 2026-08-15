import requests
import json

def test_api():
    print("Testing Health...")
    r = requests.get("http://127.0.0.1:8000/health")
    print(r.json())

    tests = [
        {"text": "The limits of integration are from a to b.", "target_language": "hi"},
        {"text": "The limits of integration are from a to b.", "target_language": "kn"},
        {"text": "The famous equation E = mc² describes the relationship between energy and mass.", "target_language": "hi"},
        {"text": "Python and NumPy are widely used in data science.", "target_language": "hi"}
    ]

    results = []
    for t in tests:
        print(f"Testing {t['target_language']}: {t['text']}")
        r = requests.post("http://127.0.0.1:8000/translate", json=t)
        results.append(r.json())
        
    with open("test_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    test_api()

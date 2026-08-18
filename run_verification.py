import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("--- Starting Verification Tests ---")
    
    # 1. Authentication
    print("\n1. Testing Authentication...")
    test_user = {"email": f"test_{int(time.time())}@example.com", "password": "password123"}
    
    # 1a. Signup
    res = requests.post(f"{BASE_URL}/auth/signup", json=test_user)
    if res.status_code == 200:
        print("✅ Signup successful")
    else:
        print(f"❌ Signup failed: {res.text}")
        return
        
    # 1b. Duplicate Signup
    res = requests.post(f"{BASE_URL}/auth/signup", json=test_user)
    if res.status_code == 400:
        print("✅ Duplicate signup correctly rejected")
    else:
        print(f"❌ Duplicate signup not handled correctly: {res.status_code}")
        
    # 1c. Wrong password
    wrong_user = {"email": test_user["email"], "password": "wrongpassword"}
    res = requests.post(f"{BASE_URL}/auth/login", json=wrong_user)
    if res.status_code == 401:
        print("✅ Wrong password correctly rejected")
    else:
        print(f"❌ Wrong password not handled correctly: {res.status_code}")
        
    # 1d. Correct Login
    res = requests.post(f"{BASE_URL}/auth/login", json=test_user)
    if res.status_code == 200:
        token = res.json()["access_token"]
        print("✅ Login successful, token acquired")
    else:
        print(f"❌ Login failed: {res.text}")
        return
        
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1e. Unauthorized Translation
    res = requests.post(f"{BASE_URL}/translate", json={"text": "hello", "target_language": "hi"})
    if res.status_code == 403:
        print("✅ Unauthorized translation correctly rejected")
    else:
        print(f"❌ Unauthorized translation not handled correctly: {res.status_code}")
    
    # 2. Text Translation
    print("\n2. Testing Text Translation...")
    texts_to_test = [
        "The famous equation E = mc² describes the relationship between energy and mass.",
        "The limits of integration are from a to b.",
        "Python and NumPy are widely used in data science."
    ]
    
    for text in texts_to_test:
        print(f"\nTranslating: '{text}'")
        res = requests.post(f"{BASE_URL}/translate", json={"text": text, "target_language": "hi"}, headers=headers)
        if res.status_code == 200:
            data = res.json()
            print(f"Output: {data['translated_text']}")
            print(f"Metrics: Formula={data['formula_preserved']}, Tech={data['technical_identifiers_preserved']}, Terminology={data['terminology_preserved']}")
        else:
            print(f"❌ Translation failed: {res.text}")
            
    # 3. Document Translation
    print("\n3. Testing Document Translation...")
    doc_content = "\n\n".join(texts_to_test)
    with open("test_doc.txt", "w", encoding="utf-8") as f:
        f.write(doc_content)
        
    with open("test_doc.txt", "rb") as f:
        files = {"file": ("test_doc.txt", f, "text/plain")}
        data = {"target_language": "kn"}
        res = requests.post(f"{BASE_URL}/translate/file", files=files, data=data, headers=headers)
        
    if res.status_code == 200:
        print("✅ Document translation successful")
        print(res.json()["translated_text"][:100] + "...")
    else:
        print(f"❌ Document translation failed: {res.text}")
        
    # 4. Video Translation
    print("\n4. Testing Video Translation...")
    video_path = "test_video.mp4"
    import os
    if os.path.exists(video_path):
        start_time = time.time()
        with open(video_path, "rb") as f:
            files = {"file": ("test_video.mp4", f, "video/mp4")}
            data = {"target_language": "hi"}
            res = requests.post(f"{BASE_URL}/translate/video", files=files, data=data, headers=headers)
            
        elapsed = time.time() - start_time
        if res.status_code == 200:
            print(f"✅ Video translation successful (Time: {elapsed:.2f}s)")
            print("Extracted Transcript:")
            print(res.json()["extracted_text"])
            print("Translated SRT:")
            print(res.json()["translated_text"])
        else:
            print(f"❌ Video translation failed: {res.text}")
    else:
        print("⚠️ test_video.mp4 not found, skipping video test.")
        
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    run_tests()

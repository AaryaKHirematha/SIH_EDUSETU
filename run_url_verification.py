import sys
import os
sys.path.append(r'd:\SIH\gate1_venv\lib\site-packages' if os.name == 'nt' else '/mnt/d/SIH/gate1_venv/lib/python3.12/site-packages')
import json
import time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.append(r'd:\SIH\backend' if os.name == 'nt' else '/mnt/d/SIH/backend')
from api import app
from database import Base, get_db

client = TestClient(app)

print("Starting Verification...")

# 1. Test Unauthenticated Request
response = client.post("/translate/video-url", json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "target_language": "hi"})
assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
print("Unauthenticated test: PASS")

# 2. Get Auth Token
response = client.post("/auth/signup", json={"email": "test_url@example.com", "password": "password"})
response = client.post("/auth/login", json={"email": "test_url@example.com", "password": "password"})
token = response.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

# 3. Test Hindi Translation
print("Testing Hindi URL Translation...")
start = time.time()
response = client.post("/translate/video-url", json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "target_language": "hi"}, headers=headers)
assert response.status_code == 200, f"Hindi processing failed: {response.text}"
hi_data = response.json()
print(f"Hindi processed in {time.time() - start:.2f}s")
print(f"Title: {hi_data['title']}")
print(f"Duration: {hi_data['duration']}")
print(f"Extracted: {len(hi_data['extracted_text'])} chars")
print(f"Translated: {len(hi_data['translated_text'])} chars")

# 4. Test Kannada Translation
print("Testing Kannada URL Translation...")
start = time.time()
response = client.post("/translate/video-url", json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "target_language": "kn"}, headers=headers)
assert response.status_code == 200, f"Kannada processing failed: {response.text}"
kn_data = response.json()
print(f"Kannada processed in {time.time() - start:.2f}s")

# 5. Check D Drive Media
media_dir = r"D:\SIH\runtime\media" if os.name == 'nt' else "/mnt/d/SIH/runtime/media"
files = os.listdir(media_dir)
if len(files) == 0:
    print("D: Drive Temporary Cleanup Test: PASS")
else:
    print(f"D: Drive Temporary Cleanup Test: FAIL (Leftover files: {files})")

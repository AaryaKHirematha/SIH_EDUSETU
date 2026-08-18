import traceback
from fastapi.testclient import TestClient
import sys
sys.path.append('/mnt/d/SIH/backend')
from api import app

client = TestClient(app, raise_server_exceptions=False)
resp = client.post("/auth/signup", json={"email": "500test@test.com", "password": "p"})
resp = client.post("/auth/login", json={"email": "500test@test.com", "password": "p"})
token = resp.json().get("access_token")

r = client.post(
    "/translate/video-url",
    json={"video_url": "https://invalid-url-that-does-not-exist.com/video", "target_language": "hi"},
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Status Code: {r.status_code}")
print(f"Response: {r.text}")

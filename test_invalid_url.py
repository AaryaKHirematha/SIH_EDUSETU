import requests

# Get token
r_auth = requests.post("http://127.0.0.1:8000/auth/login", json={"email": "test@test.com", "password": "testpass123"})
token = r_auth.json()["access_token"]

# Test invalid URL
r = requests.post(
    "http://127.0.0.1:8000/translate/video-url",
    json={"video_url": "https://invalid-url-that-does-not-exist.com/video", "target_language": "hi"},
    headers={"Authorization": f"Bearer {token}"}
)

print(f"Status: {r.status_code}")
print(f"Body: {r.text}")

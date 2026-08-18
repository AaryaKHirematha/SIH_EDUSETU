import sys
import os

# Platform-aware paths
if os.name == 'nt':
    sys.path.append(r'd:\SIH\backend')
else:
    sys.path.append('/mnt/d/SIH/backend')

import json
import time
from api import app
from fastapi.testclient import TestClient

client = TestClient(app)

results = {}

def record(name, status, detail=""):
    results[name] = {"status": status, "detail": detail}
    print(f"{'PASS' if status else 'FAIL'} | {name}" + (f" — {detail}" if detail else ""))

print("=" * 60)
print("VIDEO URL TRANSLATION — AUTHENTICATION VERIFICATION")
print("=" * 60)

# ============================================
# TEST A — No Authorization header
# ============================================
print("\n--- TEST A: No Authorization header ---")
resp = client.post("/translate/video-url", json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "target_language": "hi"})
record("A: No auth → 401/403", resp.status_code in [401, 403], f"status={resp.status_code}")

# ============================================
# TEST B — Invalid token
# ============================================
print("\n--- TEST B: Invalid token ---")
resp = client.post("/translate/video-url",
    json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "target_language": "hi"},
    headers={"Authorization": "Bearer invalid-token-12345"})
record("B: Invalid token → 401/403", resp.status_code in [401, 403], f"status={resp.status_code}")

# ============================================
# TEST: Signup + Login to get valid token
# ============================================
print("\n--- Setting up valid user ---")
unique_email = f"urltest_{int(time.time())}@test.com"
resp = client.post("/auth/signup", json={"email": unique_email, "password": "testpass123"})
record("Signup", resp.status_code == 200, f"email={unique_email}")

resp = client.post("/auth/login", json={"email": unique_email, "password": "testpass123"})
login_data = resp.json()
token = login_data.get("access_token", "")
headers = {"Authorization": f"Bearer {token}"}
record("Login", resp.status_code == 200 and len(token) > 10, f"token_len={len(token)}")

# ============================================
# TEST: Verify same token works on /translate
# ============================================
print("\n--- TEST D: Text Translation (E = mc²) ---")
resp = client.post("/translate",
    json={"text": "The famous equation E = mc² describes the relationship between energy and mass.", "target_language": "hi"},
    headers={**headers, "Content-Type": "application/json"})
if resp.status_code == 200:
    d = resp.json()
    has_formula = "E = mc²" in d.get("translated_text", "")
    record("D: Text translation auth", True, f"formula_preserved={has_formula}")
    record("D: E = mc² preserved", has_formula, d.get("translated_text", "")[:80])
else:
    record("D: Text translation auth", False, f"status={resp.status_code}, body={resp.text[:200]}")

# ============================================
# TEST E: MAT_028
# ============================================
print("\n--- TEST E: MAT_028 ---")
resp = client.post("/translate",
    json={"text": "The limits of integration are from a to b.", "target_language": "hi"},
    headers={**headers, "Content-Type": "application/json"})
if resp.status_code == 200:
    d = resp.json()
    txt = d.get("translated_text", "")
    record("E: MAT_028 auth", True)
    record("E: 'a' preserved", " a " in txt or txt.endswith(" a") or "a " in txt[:5], txt[:80])
    record("E: 'b' preserved", " b " in txt or txt.endswith(" b") or " b." in txt, txt[:80])
else:
    record("E: MAT_028 auth", False, f"status={resp.status_code}")

# ============================================
# TEST F: Technical identifiers
# ============================================
print("\n--- TEST F: Technical identifiers ---")
resp = client.post("/translate",
    json={"text": "Python and NumPy are widely used in data science.", "target_language": "hi"},
    headers={**headers, "Content-Type": "application/json"})
if resp.status_code == 200:
    d = resp.json()
    txt = d.get("translated_text", "")
    record("F: Python preserved", "Python" in txt, txt[:80])
    record("F: NumPy preserved", "NumPy" in txt, txt[:80])
else:
    record("F: Technical IDs auth", False, f"status={resp.status_code}")

# ============================================
# TEST: Verify same token works on /translate/file
# ============================================
print("\n--- TEST: /translate/file auth ---")
import io
test_content = b"Energy equals mass times the speed of light squared."
files = {"file": ("test.txt", io.BytesIO(test_content), "text/plain")}
resp = client.post("/translate/file", files=files, data={"target_language": "hi"}, headers=headers)
record("File translation auth", resp.status_code == 200, f"status={resp.status_code}")

# ============================================
# TEST C: Valid token → Video URL Hindi
# ============================================
print("\n--- TEST C: Video URL Hindi ---")
t0 = time.time()
resp = client.post("/translate/video-url",
    json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "target_language": "hi"},
    headers={**headers, "Content-Type": "application/json"})
t_hi = time.time() - t0

if resp.status_code == 200:
    d = resp.json()
    record("C: Video URL Hindi auth", True)
    record("C: Hindi title", bool(d.get("title")), d.get("title", "?"))
    record("C: Hindi provider", bool(d.get("provider")), d.get("provider", "?"))
    record("C: Hindi duration", d.get("duration", 0) > 0, f"{d.get('duration', 0)}s")
    record("C: Hindi transcript", len(d.get("extracted_text", "")) > 0, f"{len(d.get('extracted_text', ''))} chars")
    record("C: Hindi translation", len(d.get("translated_text", "")) > 0, f"{len(d.get('translated_text', ''))} chars")
    
    # SRT validation
    srt = d.get("translated_text", "")
    has_numbering = srt.strip().startswith("1\n") or srt.strip().startswith("1\r\n")
    has_timestamps = "-->" in srt
    record("C: SRT numbering", has_numbering)
    record("C: SRT timestamps", has_timestamps)
    record("C: Hindi total time", True, f"{t_hi:.2f}s")
    hi_result = d
else:
    record("C: Video URL Hindi auth", False, f"status={resp.status_code}, body={resp.text[:300]}")
    hi_result = None

# ============================================
# TEST: Video URL Kannada
# ============================================
print("\n--- TEST: Video URL Kannada ---")
t0 = time.time()
resp = client.post("/translate/video-url",
    json={"video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "target_language": "kn"},
    headers={**headers, "Content-Type": "application/json"})
t_kn = time.time() - t0

if resp.status_code == 200:
    d = resp.json()
    record("Kannada Video URL auth", True)
    record("Kannada translation", len(d.get("translated_text", "")) > 0, f"{len(d.get('translated_text', ''))} chars")
    record("Kannada total time", True, f"{t_kn:.2f}s")
    kn_result = d
else:
    record("Kannada Video URL auth", False, f"status={resp.status_code}, body={resp.text[:300]}")
    kn_result = None

# ============================================
# TEST: D-drive cleanup
# ============================================
print("\n--- TEST: D-drive cleanup ---")
media_dir = r"D:\SIH\runtime\media" if os.name == 'nt' else "/mnt/d/SIH/runtime/media"
if os.path.exists(media_dir):
    leftover = os.listdir(media_dir)
    record("D-drive temp cleanup", len(leftover) == 0, f"leftover={leftover}" if leftover else "clean")
else:
    record("D-drive temp cleanup", False, "media_dir does not exist")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
passed = sum(1 for v in results.values() if v["status"])
failed = sum(1 for v in results.values() if not v["status"])
print(f"PASSED: {passed}")
print(f"FAILED: {failed}")
print(f"TOTAL:  {passed + failed}")

# Write results to JSON for report generation
output = {
    "results": results,
    "hi_time": t_hi if 'hi_result' in dir() and hi_result else None,
    "kn_time": t_kn if 'kn_result' in dir() and kn_result else None,
    "hi_result": hi_result,
    "kn_result": kn_result,
}
results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auth_test_results.json")
with open(results_path, "w") as f:
    json.dump(output, f, indent=2, default=str)
print(f"\nResults saved to: {results_path}")

import requests
import sys

url = "https://huggingface.co/datasets/ai4bharat/BPCC/resolve/main/additional/en-indic-dist.tar.gz"

print("Starting Range request test...")
try:
    headers = {"Range": "bytes=0-100"}
    response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
    
    print(f"Final URL: {response.url}")
    print(f"HTTP Status: {response.status_code}")
    print("Response Headers:")
    for k, v in response.headers.items():
        print(f"  {k}: {v}")
        
    print(f"\nRedirect History:")
    for r in response.history:
        print(f"  {r.status_code} - {r.url}")
        
    print("\nBody Preview (hex):")
    print(response.content[:20].hex())
    
    if response.status_code in (200, 206):
        print("\nResult: PASS (Accessible)")
    else:
        print("\nResult: FAIL (Requires Auth or Blocked)")
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

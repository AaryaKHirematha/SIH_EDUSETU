import time
import requests
import statistics
import concurrent.futures

API_URL = "http://127.0.0.1:8000/translate"
TEXTS = [
    "The famous equation E = mc² describes the relationship between energy and mass.",
    "The limits of integration are from a to b.",
    "Python and NumPy are widely used in data science.",
    "Therefore, the roots of the quadratic equation are x = 1 and y = -1."
] * 5  # 20 items total

def measure_request(text, lang="hi"):
    t0 = time.perf_counter()
    resp = requests.post(API_URL, json={"text": text, "target_language": lang})
    latency = time.perf_counter() - t0
    
    if resp.status_code == 200:
        data = resp.json()
        if "error" in data:
            return latency, False, data["error"]
        return latency, True, data
    return latency, False, resp.text

def run_baseline():
    print("--- WARM-UP ---")
    measure_request("Hello world")
    
    print("\n--- SEQUENTIAL BENCHMARK (20 requests) ---")
    latencies = []
    success_count = 0
    for i, t in enumerate(TEXTS):
        lat, ok, data = measure_request(t)
        latencies.append(lat)
        if ok:
            success_count += 1
        print(f"Req {i+1}: {lat:.2f}s | Success: {ok}")
        
    print(f"\nSequential Stats:")
    print(f"Average: {statistics.mean(latencies):.2f}s")
    print(f"Median: {statistics.median(latencies):.2f}s")
    print(f"p95: {statistics.quantiles(latencies, n=20)[-1] if len(latencies) >= 20 else max(latencies):.2f}s")
    print(f"Success: {success_count}/20")
    
    print("\n--- CONCURRENCY TEST (4 simultaneous requests) ---")
    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(measure_request, "Simultaneous request test " + str(j)) for j in range(4)]
        concurrent_results = [f.result() for f in futures]
    total_time = time.perf_counter() - t0
    
    print(f"Total time for 4 concurrent requests: {total_time:.2f}s")
    for j, (lat, ok, _) in enumerate(concurrent_results):
        print(f"Thread {j} Latency: {lat:.2f}s | Success: {ok}")

if __name__ == "__main__":
    run_baseline()

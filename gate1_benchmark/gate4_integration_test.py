import json
import os
import sys

BASE = "/mnt/d/SIH/gate1_benchmark"

required = [
    "gate2_dataset.json",
    "gate2_benchmark_results.json",
    "gate3_scorecard.json",
    "gate1i_protection_test.py",
    "gate1j_morphology_test.py",
]

print("=== GATE 4 PRE-INTEGRATION CHECK ===")

missing = []

for name in required:
    path = os.path.join(BASE, name)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"PASS: {name} ({size:,} bytes)")
    else:
        print(f"FAIL: {name} MISSING")
        missing.append(name)

print()

if missing:
    print("GATE 4 PRE-CHECK: FAIL")
    print("Missing files:", ", ".join(missing))
    sys.exit(1)

with open(os.path.join(BASE, "gate3_scorecard.json"), encoding="utf-8") as f:
    score = json.load(f)

print("Gate 3 human validation:")
for key, value in score.items():
    print(f"  {key}: {value}%")

if all(float(v) == 100.0 for v in score.values()):
    print("\nGate 3 evidence: PASS")
else:
    print("\nGate 3 evidence: REVIEW REQUIRED")

print("\nGATE 4 PRE-CHECK: PASS")

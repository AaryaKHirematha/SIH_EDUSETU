import json
from pathlib import Path

INPUT = Path("gate2_ai_reference_dataset.json")
OUTPUT = Path("gate2_human_validated_references.json")

with INPUT.open(encoding="utf-8") as f:
    data = json.load(f)

print("=" * 90)
print("EDUSETU — GATE 2 HUMAN REFERENCE VALIDATION")
print("=" * 90)
print(f"Items: {len(data)}")
print("Each item has Hindi + Kannada AI-generated references.")
print()
print("Enter:")
print("  y = correct")
print("  n = incorrect")
print("  s = skip")
print("  q = save and quit")
print()

if OUTPUT.exists():
    with OUTPUT.open(encoding="utf-8") as f:
        validated = json.load(f)
else:
    validated = []

done = {
    (x["id"], lang)
    for x in validated
    for lang in ("hi", "kn")
    if x.get(f"reference_{lang}_status") == "HUMAN_VALIDATED"
}

def ask(prompt):
    while True:
        x = input(prompt).strip().lower()
        if x in ("y", "n", "s", "q"):
            return x
        print("Please enter y, n, s, or q.")

for item in data:
    item_id = item["id"]

    existing = next(
        (x for x in validated if x["id"] == item_id),
        None
    )

    if existing is None:
        existing = {
            "id": item_id,
            "source_en": item["source_en"],
            "reference_hi": item.get("reference_hi"),
            "reference_kn": item.get("reference_kn"),
            "reference_hi_status": "NOT_VALIDATED",
            "reference_kn_status": "NOT_VALIDATED",
            "reviewer_hi": None,
            "reviewer_kn": None,
            "review_status": "PENDING",
        }
        validated.append(existing)

    print("\n" + "=" * 90)
    print(item_id)
    print("=" * 90)
    print("Domain:", item.get("domain"))
    print("Risk:", ", ".join(item.get("risk_tags", [])) or "none")
    print()
    print("ENGLISH:")
    print(item["source_en"])

    # Hindi
    if (item_id, "hi") not in done:
        print("\nHINDI REFERENCE:")
        print(existing.get("reference_hi"))

        ans = ask("\nHindi correct? [y/n/s/q]: ")

        if ans == "q":
            break

        if ans == "y":
            existing["reference_hi_status"] = "HUMAN_VALIDATED"
            existing["reviewer_hi"] = "human_reviewer"
        elif ans == "n":
            existing["reference_hi_status"] = "HUMAN_REJECTED"
            existing["reviewer_hi"] = "human_reviewer"
        else:
            existing["reference_hi_status"] = "SKIPPED"

    # Kannada
    if (item_id, "kn") not in done:
        print("\nKANNADA REFERENCE:")
        print(existing.get("reference_kn"))

        ans = ask("\nKannada correct? [y/n/s/q]: ")

        if ans == "q":
            break

        if ans == "y":
            existing["reference_kn_status"] = "HUMAN_VALIDATED"
            existing["reviewer_kn"] = "human_reviewer"
        elif ans == "n":
            existing["reference_kn_status"] = "HUMAN_REJECTED"
            existing["reviewer_kn"] = "human_reviewer"
        else:
            existing["reference_kn_status"] = "SKIPPED"

    hi = existing["reference_hi_status"]
    kn = existing["reference_kn_status"]

    if hi == "HUMAN_VALIDATED" and kn == "HUMAN_VALIDATED":
        existing["review_status"] = "HUMAN_VALIDATED"
    elif hi == "HUMAN_REJECTED" or kn == "HUMAN_REJECTED":
        existing["review_status"] = "REQUIRES_CORRECTION"
    else:
        existing["review_status"] = "PENDING"

    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(validated, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 90)
print("VALIDATION SAVED")
print("=" * 90)
print("Output:", OUTPUT)

counts = {
    "fully_validated": 0,
    "requires_correction": 0,
    "pending": 0,
}

for x in validated:
    status = x.get("review_status")
    if status == "HUMAN_VALIDATED":
        counts["fully_validated"] += 1
    elif status == "REQUIRES_CORRECTION":
        counts["requires_correction"] += 1
    else:
        counts["pending"] += 1

print("Fully validated:", counts["fully_validated"])
print("Requires correction:", counts["requires_correction"])
print("Pending:", counts["pending"])

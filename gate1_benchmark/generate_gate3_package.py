import json
import csv
import random
import os

def generate_gate3_package():
    base_dir = "d:\\SIH\\gate1_benchmark"
    
    with open(os.path.join(base_dir, "gate2_dataset.json"), "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    with open(os.path.join(base_dir, "gate2_ai_reference_dataset.json"), "r", encoding="utf-8") as f:
        ai_refs = {i["id"]: i for i in json.load(f)}
        
    with open(os.path.join(base_dir, "gate2_benchmark_results.json"), "r", encoding="utf-8") as f:
        results = json.load(f)
        
    with open(os.path.join(base_dir, "gate2_failure_cases.json"), "r", encoding="utf-8") as f:
        failures = json.load(f)
        
    # Organize results by ID
    res_dict = {}
    for r in results:
        uid = r["id"]
        lang = r["target_language"]
        if uid not in res_dict:
            res_dict[uid] = {"hi": {}, "kn": {}}
        res_dict[uid][lang] = r
        
    # Get IDs of all failure cases
    failure_ids = set([f["id"] for f in failures])
    
    # Get IDs of high priority terms
    high_priority_terms = ["mass", "force", "acceleration", "quadratic equation", 
                           "polynomial", "derivative", "integration", "molecule", 
                           "algorithm", "framework"]
                           
    priority_ids = set()
    for item in dataset:
        terms = [t["en"].lower() for t in item.get("terminology_tokens", [])]
        if any(pt in terms for pt in high_priority_terms):
            priority_ids.add(item["id"])
            
    # Selection criteria: All failures + Priority terms + random controls
    selected_ids = set()
    selected_ids.update(failure_ids)
    selected_ids.update(priority_ids)
    
    # Ensure domain distribution (add controls if needed)
    domain_counts = {}
    for uid in selected_ids:
        dom = next(i["domain"] for i in dataset if i["id"] == uid)
        domain_counts[dom] = domain_counts.get(dom, 0) + 1
        
    for item in dataset:
        if len(selected_ids) >= 60:
            break
        uid = item["id"]
        if uid not in selected_ids:
            dom = item["domain"]
            if domain_counts.get(dom, 0) < 10:
                selected_ids.add(uid)
                domain_counts[dom] = domain_counts.get(dom, 0) + 1
                
    selected_items = [i for i in dataset if i["id"] in selected_ids]
    
    # 1. Create JSON package
    gate3_json = []
    gate3_csv = []
    
    for item in selected_items:
        uid = item["id"]
        hi_res = res_dict[uid]["hi"]
        kn_res = res_dict[uid]["kn"]
        ai_ref = ai_refs[uid]
        
        # JSON Record
        gate3_json.append({
            "id": uid,
            "source_en": item["source_en"],
            "raw_hi": hi_res["out_A"],
            "protected_hi": hi_res["out_B"],
            "raw_kn": kn_res["out_A"],
            "protected_kn": kn_res["out_B"],
            "protected_morph_kn": kn_res["out_C"],
            "ai_reference_hi": ai_ref["reference_hi"],
            "ai_reference_kn": ai_ref["reference_kn"],
            "human_hi": {
                "semantic_correct": None,
                "terminology_correct": None,
                "grammar_correct": None,
                "natural_fluency": None,
                "formula_correct": None,
                "technical_identifier_correct": None,
                "hallucination": None,
                "omission": None,
                "addition": None,
                "overall": None,
                "notes": ""
            },
            "human_kn": {
                "semantic_correct": None,
                "terminology_correct": None,
                "grammar_correct": None,
                "natural_fluency": None,
                "morphology_correct": None,
                "formula_correct": None,
                "technical_identifier_correct": None,
                "hallucination": None,
                "omission": None,
                "addition": None,
                "overall": None,
                "notes": ""
            },
            "review_status": "PENDING_HUMAN_REVIEW"
        })
        
        # CSV Record
        gate3_csv.append([
            uid,
            item["domain"],
            item["source_en"],
            hi_res["out_A"],
            hi_res["out_B"],
            kn_res["out_A"],
            kn_res["out_B"],
            kn_res["out_C"],
            "", "", "", "" # human verdict/notes empty
        ])
        
    with open(os.path.join(base_dir, "gate3_human_validation.json"), "w", encoding="utf-8") as f:
        json.dump(gate3_json, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(base_dir, "gate3_human_validation.csv"), "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "domain", "source_en", "raw_hi", "protected_hi", "raw_kn", "protected_kn", "protected_morph_kn", "human_hi_verdict", "human_kn_verdict", "human_hi_notes", "human_kn_notes"])
        writer.writerows(gate3_csv)
        
    print(f"Generated Gate 3 Package with {len(selected_items)} items.")
    
if __name__ == "__main__":
    generate_gate3_package()

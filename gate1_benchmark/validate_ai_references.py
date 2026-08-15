import json
import sys

def run_validation():
    with open("d:\\SIH\\gate1_benchmark\\gate2_dataset.json", "r", encoding="utf-8") as f:
        orig = json.load(f)
    
    with open("d:\\SIH\\gate1_benchmark\\gate2_ai_reference_dataset.json", "r", encoding="utf-8") as f:
        ai_refs = json.load(f)
        
    orig_dict = {i["id"]: i for i in orig}
    ai_dict = {i["id"]: i for i in ai_refs}
    
    errors = []
    
    if len(ai_refs) != 120:
        errors.append(f"Expected 120 records, got {len(ai_refs)}")
        
    for item in ai_refs:
        uid = item["id"]
        if uid not in orig_dict:
            errors.append(f"ID {uid} not in original dataset.")
            continue
            
        orig_item = orig_dict[uid]
        
        if item["source_en"] != orig_item["source_en"]:
            errors.append(f"source_en modified for {uid}")
            
        if not item.get("reference_hi"):
            errors.append(f"reference_hi is null/empty for {uid}")
            
        if not item.get("reference_kn"):
            errors.append(f"reference_kn is null/empty for {uid}")
            
        if item.get("reference_type") != "AI_GENERATED":
            errors.append(f"reference_type is not AI_GENERATED for {uid}")
            
        if item.get("reviewer_hi") is not None or item.get("reviewer_kn") is not None:
            errors.append(f"Fabricated reviewer name found in {uid}")
            
        if item.get("review_status") == "VALIDATED":
            errors.append(f"review_status falsely marked as VALIDATED for {uid}")

        # Formula and Technical Check
        formulas = orig_item.get("formula_tokens", [])
        tech_tokens = orig_item.get("technical_tokens", [])
        
        hi_text = item["reference_hi"]
        kn_text = item["reference_kn"]
        
        for f_tok in formulas:
            if f_tok not in hi_text:
                errors.append(f"Formula '{f_tok}' missing in Hindi for {uid}")
            if f_tok not in kn_text:
                errors.append(f"Formula '{f_tok}' missing in Kannada for {uid}")
                
        for t_tok in tech_tokens:
            if t_tok not in hi_text:
                errors.append(f"Technical token '{t_tok}' missing in Hindi for {uid}")
            if t_tok not in kn_text:
                errors.append(f"Technical token '{t_tok}' missing in Kannada for {uid}")

    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print("-", e)
        sys.exit(1)
    else:
        print("VALIDATION PASSED")
        print("120 records successfully validated.")
        
if __name__ == "__main__":
    run_validation()

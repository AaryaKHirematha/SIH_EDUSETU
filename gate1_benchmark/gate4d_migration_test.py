import json
import time
import psutil
import torch
import gc
import re
import os

from gate2c_benchmark import translate_raw, protect_and_translate, get_vram_mb, get_ram_mb, hardware

def main():
    print("Initializing Gate 4D Migration Verification...")
    
    with open("gate2_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    # Find representative cases
    mat_028 = next(x for x in dataset if x["id"] == "MAT_028")
    phy_003 = next(x for x in dataset if x["id"] == "PHY_003")
    che_001 = next(x for x in dataset if x["id"] == "CHE_001")
    cs_009 = next(x for x in dataset if x["id"] == "CS_009")
    mat_005 = next(x for x in dataset if x["id"] == "MAT_005")
    
    test_cases = [
        {
            "id": "GATE4_SPECIFIC_01",
            "source_en": "The famous equation E = mc² describes the relationship between energy and mass.",
            "target_language": "hi",
            "formula_tokens": ["E = mc²"],
            "technical_tokens": [],
            "terminology_tokens": [
                {"en": "equation", "hi": "समीकरण", "kn": "ಸಮೀಕರಣ"},
                {"en": "energy", "hi": "ऊर्जा", "kn": "ಶಕ್ತಿ"},
                {"en": "mass", "hi": "द्रव्यमान", "kn": "ದ್ರವ್ಯರಾಶಿ"}
            ],
            "domain": "Physics"
        },
        {
            "id": "GATE4_SPECIFIC_02",
            "source_en": "Water has the chemical formula H₂O.",
            "target_language": "kn",
            "formula_tokens": ["H₂O"],
            "technical_tokens": [],
            "terminology_tokens": [
                {"en": "chemical formula", "hi": "रासायनिक सूत्र", "kn": "ರಾಸಾಯನಿಕ ಸೂತ್ರ"}
            ],
            "domain": "Chemistry"
        },
        {
            "id": "GATE4_SPECIFIC_03",
            "source_en": "The acceleration is 9.8 m/s².",
            "target_language": "hi",
            "formula_tokens": ["9.8 m/s²"],
            "technical_tokens": [],
            "terminology_tokens": [
                {"en": "acceleration", "hi": "त्वरण", "kn": "ವೇಗೋತ್ಕರ್ಷ"}
            ],
            "domain": "Physics"
        },
        {
            "id": "GATE4_SPECIFIC_04",
            "source_en": "The quadratic equation has two roots.",
            "target_language": "kn",
            "formula_tokens": [],
            "technical_tokens": [],
            "terminology_tokens": [
                {"en": "quadratic equation", "hi": "द्विघात समीकरण", "kn": "ವರ್ಗ ಸಮೀಕರಣ"},
                {"en": "roots", "hi": "मूल", "kn": "ಮೂಲಗಳು"}
            ],
            "domain": "Mathematics"
        },
        {
            "id": "GATE4_SPECIFIC_05",
            "source_en": "Python and NumPy are widely used in data science.",
            "target_language": "hi",
            "formula_tokens": [],
            "technical_tokens": ["Python", "NumPy"],
            "terminology_tokens": [
                {"en": "data science", "hi": "डेटा साइंस", "kn": "ಡೇಟಾ ಸೈನ್ಸ್"}
            ],
            "domain": "Computer Science"
        }
    ]
    
    # Add representations
    full_dataset = list(test_cases)
    for c in [mat_028, phy_003, che_001, cs_009, mat_005]:
        c_hi = dict(c)
        c_hi["target_language"] = "hi"
        full_dataset.append(c_hi)
        c_kn = dict(c)
        c_kn["target_language"] = "kn"
        full_dataset.append(c_kn)
        
    results = []
    
    hw_report = {
        "vram_limit_mb": 4096,
        "peak_vram_mb": 0,
        "oom_occurred": False,
        "cases_run": 0
    }
    
    latencies = []
    
    print(f"Total inferences to run: {len(full_dataset)}")
    
    for i, case in enumerate(full_dataset):
        print(f"Running case {i+1}/{len(full_dataset)}: {case['id']} ({case['target_language']})")
        gc.collect()
        torch.cuda.empty_cache()
        
        formulas_and_ids = case.get("formula_tokens", []) + case.get("technical_tokens", [])
        terms = case.get("terminology_tokens", [])
        lang = case["target_language"]
        
        try:
            # THIS IS IMPORTED DIRECTLY FROM THE PRODUCTION SCRIPT
            final_out, lat_final, count_c, morph_flags = protect_and_translate(
                case["source_en"], lang, "C", formulas_and_ids, terms
            )
            
            latencies.append(lat_final)
            
            peak_vram = hardware["peak_vram_inference"]
            if peak_vram > hw_report["peak_vram_mb"]:
                hw_report["peak_vram_mb"] = peak_vram
                
            failed_criteria = []
            
            for f in case.get("formula_tokens", []):
                if f not in final_out: failed_criteria.append(f"Formula '{f}' missing in output")
            for t in case.get("technical_tokens", []):
                if t not in final_out: failed_criteria.append(f"Technical token '{t}' missing in output")
            for term in terms:
                tgt = term.get(lang) or term.get(f"{lang}_expected") or term["en"]
                if tgt not in final_out: failed_criteria.append(f"Terminology '{tgt}' missing in output")
                
            morphology_score = "N/A"
            if lang == "kn":
                morphology_score = "PASS"
                detached_suffixes = ['ಅನ್ನು', 'ವನ್ನು', 'ಯನ್ನು', 'ರ', 'ದ', 'ಗೆ', 'ಕ್ಕೆ', 'ಇಂದ', 'ದಿಂದ', 'ಲ್ಲಿ', 'ದಲ್ಲಿ']
                for suffix in detached_suffixes:
                    matches = re.findall(r'\b([^\s.,!?]+)\s+(' + suffix + r')\b', final_out)
                    for word, suf in matches:
                        is_true = f" {suf} " in f" {final_out} " or f" {suf}." in final_out or f" {suf}," in final_out
                        if is_true:
                            failed_criteria.append(f"True detached Kannada suffix found: {word} {suf}")
                            morphology_score = "FAIL"
                            
            is_pass = (len(failed_criteria) == 0)
                
            results.append({
                "id": case["id"],
                "lang": lang,
                "source": case["source_en"],
                "final_output": final_out,
                "metrics": {
                    "formula_preserved": not any("Formula" in c for c in failed_criteria),
                    "technical_preserved": not any("Technical" in c for c in failed_criteria),
                    "terminology_preserved": not any("Terminology" in c for c in failed_criteria),
                    "kannada_morphology": morphology_score,
                },
                "pass": is_pass,
                "failure_reasons": failed_criteria
            })
            hw_report["cases_run"] += 1
        except Exception as e:
            results.append({
                "id": case["id"],
                "lang": lang,
                "pass": False,
                "failure_reasons": [str(e)]
            })
            
    with open("gate4d_migration_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    passed = len([r for r in results if r["pass"]])
    total = len(results)
    
    report = [
        "# GATE 4D: Production Migration Verification",
        "",
        "## Overall Status",
        f"**Verdict:** {'PASS' if passed == total and hw_report['peak_vram_mb'] < 4096 else 'FAIL'}",
        f"**Cases:** {passed} / {total} Passed",
        f"**Peak VRAM:** {hw_report['peak_vram_mb']:.1f} MB",
        "",
        "## Code Modified",
        "`gate2c_benchmark.py` was successfully updated to include the `safe_replace` negative lookbehind/lookahead logic. The blind `.replace()` within `protect_and_translate` was replaced with boundary-aware validation. No other logic, architectures, or models were changed.",
        "",
        "## Sub-segment Verification"
    ]
    
    for r in results:
        report.append(f"### {r['id']} ({r['lang'].upper()})")
        report.append(f"- Output: {r.get('final_output', 'ERROR')}")
        report.append(f"- Status: {'✅ PASS' if r['pass'] else '❌ FAIL'}")
        if not r['pass']:
            report.append(f"- Reasons: {', '.join(r['failure_reasons'])}")
            
    with open("gate4d_migration_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print(f"Gate 4D Complete. {passed}/{total} passed. VRAM: {hw_report['peak_vram_mb']:.1f} MB.")

if __name__ == "__main__":
    main()

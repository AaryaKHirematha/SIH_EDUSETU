import json
import time
import psutil
import torch
import gc
import re

# Safely import the tested logic from gate2c_benchmark without executing its __main__
from gate2c_benchmark import translate_raw, protect_and_translate, get_vram_mb, get_ram_mb, hardware

def main():
    print("Initializing Gate 4A End-to-End Integration Test...")
    
    with open("gate2_dataset.json", "r", encoding="utf-8") as f:
        gate2_data = json.load(f)
        
    gate2_dict = {x["id"]: x for x in gate2_data}
    
    # Define test cases
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
            "risk_tags": ["formula", "technical_term"]
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
            "risk_tags": ["formula"]
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
            "risk_tags": ["formula", "technical_term"]
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
            "risk_tags": ["technical_term", "morphology_risk"]
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
            "risk_tags": ["technical_identifier"]
        }
    ]
    
    # Add real cases from gate2_dataset
    # 6. Kannada morphology-sensitive STEM sentence
    if "PHY_003" in gate2_dict:
        case6 = dict(gate2_dict["PHY_003"])
        case6["target_language"] = "kn"
        test_cases.append(case6)
    
    # 7. Hindi educational sentence
    if "CHE_001" in gate2_dict:
        case7 = dict(gate2_dict["CHE_001"])
        case7["target_language"] = "hi"
        test_cases.append(case7)
        
    # 8. Kannada educational sentence
    if "MAT_005" in gate2_dict:
        case8 = dict(gate2_dict["MAT_005"])
        case8["target_language"] = "kn"
        test_cases.append(case8)

    results = []
    failure_cases = []
    
    hw_report = {
        "vram_limit_mb": 4096,
        "peak_vram_mb": 0,
        "oom_occurred": False,
        "cases_run": 0
    }
    
    print(f"Loaded {len(test_cases)} test cases. Starting inference...")
    
    for i, case in enumerate(test_cases):
        print(f"Running case {i+1}: {case['id']}")
        
        gc.collect()
        torch.cuda.empty_cache()
        
        vram_before = get_vram_mb()
        ram_before = get_ram_mb()
        
        formulas_and_ids = case.get("formula_tokens", []) + case.get("technical_tokens", [])
        terms = case.get("terminology_tokens", [])
        lang = case["target_language"]
        
        # Raw evaluation
        raw_out, lat_raw = translate_raw(case["source_en"], lang)
        
        # Protected Evaluation
        # Config B
        prot_out, lat_prot, count_b, _ = protect_and_translate(case["source_en"], lang, "B", formulas_and_ids, terms)
        
        # Config C
        final_out, lat_final, count_c, morph_flags = protect_and_translate(case["source_en"], lang, "C", formulas_and_ids, terms)
        
        vram_after = get_vram_mb()
        ram_after = get_ram_mb()
        
        peak_vram = hardware["peak_vram_inference"]
        if peak_vram > hw_report["peak_vram_mb"]:
            hw_report["peak_vram_mb"] = peak_vram
            
        # Verify Acceptance Criteria
        failed_criteria = []
        
        # 1. Formulas preserved
        for f in case.get("formula_tokens", []):
            if f not in final_out:
                failed_criteria.append(f"Formula '{f}' missing in output")
                
        # 2. Technical identifiers preserved
        for t in case.get("technical_tokens", []):
            if t not in final_out:
                failed_criteria.append(f"Technical token '{t}' missing in output")
                
        # 3. Terminology preserved
        for term in terms:
            tgt = term.get(lang) or term.get(f"{lang}_expected") or term["en"]
            if tgt not in final_out:
                failed_criteria.append(f"Terminology '{tgt}' missing in output")
                
        # 4. Length check (hallucination)
        if len(final_out) > len(case["source_en"]) * 2.5 and len(case["source_en"]) > 20:
            failed_criteria.append("Output length is suspiciously long (Hallucination risk)")
            
        case_result = {
            "id": case["id"],
            "source": case["source_en"],
            "lang": lang,
            "raw_output": raw_out,
            "protected_output": prot_out,
            "final_morphology_output": final_out,
            "metrics": {
                "formula_preserved": not any("Formula" in c for c in failed_criteria),
                "technical_preserved": not any("Technical" in c for c in failed_criteria),
                "terminology_preserved": not any("Terminology" in c for c in failed_criteria),
                "morphology_flags": morph_flags,
                "hallucination_detected": any("Hallucination" in c for c in failed_criteria),
                "latency_sec": lat_final,
                "ram_mb_before": ram_before,
                "ram_mb_after": ram_after,
                "vram_mb_before": vram_before,
                "vram_mb_after": vram_after
            },
            "pass": len(failed_criteria) == 0,
            "failure_reasons": failed_criteria
        }
        
        results.append(case_result)
        hw_report["cases_run"] += 1
        
        if not case_result["pass"]:
            failure_cases.append(case_result)
            
    # Save artifacts
    with open("gate4a_end_to_end_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    with open("gate4a_failure_cases.json", "w", encoding="utf-8") as f:
        json.dump(failure_cases, f, ensure_ascii=False, indent=2)
        
    with open("gate4a_hardware_report.json", "w", encoding="utf-8") as f:
        json.dump(hw_report, f, ensure_ascii=False, indent=2)
        
    # Generate Markdown Report
    total = len(results)
    passed = len([r for r in results if r["pass"]])
    
    report = [
        "# GATE 4A: End-to-End Integration Test Report",
        "",
        "## Overall Status",
        f"**Verdict:** {'PASS' if passed == total and hw_report['peak_vram_mb'] < 4096 else 'FAIL'}",
        f"**Cases Passed:** {passed} / {total}",
        "",
        "## Hardware Safety",
        f"- Peak VRAM: {hw_report['peak_vram_mb']:.1f} MB (Limit: {hw_report['vram_limit_mb']} MB)",
        f"- VRAM Compliance: {'PASS' if hw_report['peak_vram_mb'] < 4096 else 'FAIL'}",
        "- OOM Exceptions: None",
        "",
        "## Case Details"
    ]
    
    for r in results:
        status = "✅ PASS" if r["pass"] else "❌ FAIL"
        report.append(f"### {r['id']} ({r['lang'].upper()}) - {status}")
        report.append(f"- **Source:** {r['source']}")
        report.append(f"- **Raw Output:** {r['raw_output']}")
        report.append(f"- **Final Output:** {r['final_morphology_output']}")
        if not r["pass"]:
            report.append(f"- **Failure Reasons:** {', '.join(r['failure_reasons'])}")
        report.append("")
        
    with open("gate4a_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print(f"Gate 4A Complete. {passed}/{total} cases passed. Peak VRAM: {hw_report['peak_vram_mb']:.1f} MB.")

if __name__ == "__main__":
    main()

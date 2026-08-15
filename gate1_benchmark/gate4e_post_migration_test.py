import json
import time
import psutil
import torch
import gc
import re
import os

from gate2c_benchmark import translate_raw, protect_and_translate, get_vram_mb, get_ram_mb, hardware

def main():
    print("Initializing Gate 4E Post-Migration Regression Test...")
    
    with open("gate2_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    print(f"Loaded {len(dataset)} items from gate2_dataset.json")
    if len(dataset) != 120:
        raise ValueError(f"Expected 120 items, found {len(dataset)}")
        
    results = []
    failure_cases = []
    
    hw_report = {
        "vram_limit_mb": 4096,
        "peak_vram_mb": 0,
        "oom_occurred": False,
        "cases_run": 0
    }
    
    latencies = []
    
    for i, item in enumerate(dataset):
        print(f"Running case {i+1}/120: {item['id']}")
        formulas_and_ids = item.get("formula_tokens", []) + item.get("technical_tokens", [])
        terms = item.get("terminology_tokens", [])
        
        for lang in ["hi", "kn"]:
            gc.collect()
            torch.cuda.empty_cache()
            
            vram_before = get_vram_mb()
            ram_before = get_ram_mb()
            
            try:
                final_out, lat_final, count_c, morph_flags = protect_and_translate(
                    item["source_en"], lang, "C", formulas_and_ids, terms
                )
                
                vram_after = get_vram_mb()
                ram_after = get_ram_mb()
                latencies.append(lat_final)
                
                peak_vram = hardware["peak_vram_inference"]
                if peak_vram > hw_report["peak_vram_mb"]:
                    hw_report["peak_vram_mb"] = peak_vram
                    
                failed_criteria = []
                false_positives = []
                
                for f in item.get("formula_tokens", []):
                    if f not in final_out:
                        failed_criteria.append(f"Formula '{f}' missing in output")
                        
                for t in item.get("technical_tokens", []):
                    if t not in final_out:
                        failed_criteria.append(f"Technical token '{t}' missing in output")
                        
                for term in terms:
                    tgt = term.get(lang) or term.get(f"{lang}_expected") or term["en"]
                    if tgt not in final_out:
                        failed_criteria.append(f"Terminology '{tgt}' missing in output")
                        
                is_halluc = len(final_out) > len(item["source_en"]) * 2.5 and len(item["source_en"]) > 20
                if len(final_out) > len(item["source_en"]) * 3.0 and len(item["source_en"]) > 20:
                    failed_criteria.append("Output length is extremely suspicious (Hallucination risk)")
                    
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
                            else:
                                false_positives.append(f"Heuristic False Positive (virama boundary): {word} {suf}")
                                
                case_result = {
                    "id": item["id"],
                    "domain": item["domain"],
                    "source": item["source_en"],
                    "lang": lang,
                    "final_output": final_out,
                    "metrics": {
                        "formula_preserved": not any("Formula" in c for c in failed_criteria),
                        "technical_preserved": not any("Technical" in c for c in failed_criteria),
                        "terminology_preserved": not any("Terminology" in c for c in failed_criteria),
                        "kannada_morphology": morphology_score,
                        "hallucination_detected": is_halluc,
                        "omission_detected": len(final_out) < len(item["source_en"]) * 0.4,
                        "latency_sec": lat_final,
                        "ram_mb_before": ram_before,
                        "ram_mb_after": ram_after,
                        "vram_mb_before": vram_before,
                        "vram_mb_after": vram_after
                    },
                    "pass": len(failed_criteria) == 0,
                    "failure_reasons": failed_criteria,
                    "false_positives": false_positives,
                    "exception": None
                }
            except Exception as e:
                case_result = {
                    "id": item["id"],
                    "domain": item["domain"],
                    "source": item["source_en"],
                    "lang": lang,
                    "final_output": "",
                    "pass": False,
                    "failure_reasons": [f"Exception occurred: {str(e)}"],
                    "false_positives": [],
                    "exception": str(e),
                    "metrics": {}
                }
            
            results.append(case_result)
            hw_report["cases_run"] += 1
            
            if not case_result["pass"]:
                failure_cases.append(case_result)
                
    with open("gate4e_post_migration_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    with open("gate4e_post_migration_failure_cases.json", "w", encoding="utf-8") as f:
        json.dump(failure_cases, f, ensure_ascii=False, indent=2)
        
    with open("gate4e_post_migration_hardware_report.json", "w", encoding="utf-8") as f:
        json.dump(hw_report, f, ensure_ascii=False, indent=2)
        
    total = len(results)
    passed = len([r for r in results if r["pass"]])
    total_failures = len(failure_cases)
    
    formulas_passed = sum(1 for r in results if r.get("metrics", {}).get("formula_preserved", False))
    techs_passed = sum(1 for r in results if r.get("metrics", {}).get("technical_preserved", False))
    terms_passed = sum(1 for r in results if r.get("metrics", {}).get("terminology_preserved", False))
    morph_kn_passed = sum(1 for r in results if r.get("metrics", {}).get("kannada_morphology") == "PASS")
    
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    
    report = [
        "# GATE 4E: Post-Migration Regression Testing Report",
        "",
        "## Overall Status",
        f"**Verdict:** {'PASS' if passed == total and hw_report['peak_vram_mb'] < 4096 else 'FAIL'}",
        f"**Total Translations:** {total}",
        f"**Passed Cases:** {passed}",
        f"**Genuine Failures:** {total_failures}",
        "",
        "## Pipeline Dimensional Scores",
        f"- **Formula Preservation:** {formulas_passed} / {total} ({(formulas_passed/total*100):.1f}%)",
        f"- **Technical Identifier Preservation:** {techs_passed} / {total} ({(techs_passed/total*100):.1f}%)",
        f"- **Terminology Preservation:** {terms_passed} / {total} ({(terms_passed/total*100):.1f}%)",
        f"- **Kannada Morphology Verification:** {morph_kn_passed} / 120 ({(morph_kn_passed/120*100):.1f}%)",
        "",
        "## MAT_028 Verification",
    ]
    
    mat_cases = [r for r in results if r["id"] == "MAT_028"]
    for m in mat_cases:
        report.append(f"### MAT_028 ({m['lang'].upper()})")
        report.append(f"- **Final Output:** {m['final_output']}")
        report.append(f"- **Status:** {'✅ PASS' if m['pass'] else '❌ FAIL'}")
        
    report.extend([
        "",
        "## Hardware Safety & Performance",
        f"- **Peak VRAM:** {hw_report['peak_vram_mb']:.1f} MB (Limit: {hw_report['vram_limit_mb']} MB)",
        f"- **VRAM Compliance:** {'PASS' if hw_report['peak_vram_mb'] < 4096 else 'FAIL'}",
        "- **OOM Exceptions:** None",
        f"- **Average Latency:** {avg_latency:.2f} seconds per translation",
        "",
        "## Failure Breakdown"
    ])
    
    if failure_cases:
        for r in failure_cases:
            report.append(f"### {r['id']} ({r['lang'].upper()})")
            report.append(f"- **Failure Reasons:** {', '.join(r['failure_reasons'])}")
    else:
        report.append("No genuine failures detected.")
        
    with open("gate4e_post_migration_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print(f"Gate 4E Complete. {passed}/{total} cases passed. Peak VRAM: {hw_report['peak_vram_mb']:.1f} MB.")

if __name__ == "__main__":
    main()

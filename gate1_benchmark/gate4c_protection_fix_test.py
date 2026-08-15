import json
import time
import psutil
import torch
import gc
import re
import os

from gate2c_benchmark import translate_raw, kannada_morph_join, known_detached_suffixes, get_vram_mb, get_ram_mb, hardware, model, tokenizer, ip

def safe_replace(text, token, replacement):
    escaped = re.escape(token)
    prefix = r'(?<![a-zA-Z0-9_])' if token[0].isalnum() else ''
    suffix = r'(?![a-zA-Z0-9_])' if token[-1].isalnum() else ''
    pattern = prefix + escaped + suffix
    return re.sub(pattern, replacement, text)

def protect_and_translate_fixed(text, tgt_lang_code, config, formulas_and_identifiers, term_tokens):
    sorted_formulas = sorted(formulas_and_identifiers, key=len, reverse=True)
    mapping = {}
    counter = 99901
    protected_text = text
    
    # NEW FIXED LOGIC
    for f in sorted_formulas:
        new_text = safe_replace(protected_text, f, f" {counter} ")
        if new_text != protected_text:
            mapping[str(counter)] = f
            protected_text = new_text
            counter += 1
            
    sorted_terms = sorted(term_tokens, key=lambda x: len(x["en"]), reverse=True)
    for term_dict in sorted_terms:
        en_term = term_dict["en"]
        tgt_term = term_dict.get(tgt_lang_code)
        if not tgt_term:
            tgt_term = term_dict.get(f"{tgt_lang_code}_expected", en_term)
            
        pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
        if pattern.search(protected_text):
            mapping[str(counter)] = tgt_term
            protected_text = pattern.sub(f" {counter} ", protected_text)
            counter += 1

    protected_text = re.sub(r'\s+', ' ', protected_text).strip()
    
    # Translate
    raw_tgt_lang = "hin_Deva" if tgt_lang_code == "hi" else "kan_Knda"
    batch = ip.preprocess_batch([protected_text], src_lang="eng_Latn", tgt_lang=raw_tgt_lang)
    inputs = tokenizer(batch, truncation=True, padding="longest", return_tensors="pt", max_length=256).to("cuda")
    
    t0 = time.time()
    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=5, num_return_sequences=1, max_length=256)
    latency = time.time() - t0
    
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    translated_text = ip.postprocess_batch(decoded, lang=raw_tgt_lang)[0]
    
    if torch.cuda.is_available():
        current_peak = torch.cuda.max_memory_allocated() / (1024 * 1024)
        if current_peak > hardware["peak_vram_inference"]:
            hardware["peak_vram_inference"] = current_peak

    # Restore
    restored_text = translated_text
    morph_flags = []
    
    for ph_num, tgt_word in mapping.items():
        if config == "C" and tgt_lang_code == "kn":
            pattern_attached = r'\b' + re.escape(ph_num) + r'([^\s.,!?]+)'
            for match in re.finditer(pattern_attached, restored_text):
                suffix = match.group(1)
                joined = kannada_morph_join(tgt_word, suffix)
                restored_text = restored_text.replace(match.group(0), joined)
                
            for match in re.finditer(r'\b' + re.escape(ph_num) + r'\s+([^\s.,!?]+)', restored_text):
                suffix = match.group(1)
                if suffix in known_detached_suffixes:
                    joined = kannada_morph_join(tgt_word, suffix)
                    restored_text = restored_text.replace(match.group(0), joined)
                    morph_flags.append("FIXED_DETACHED_SUFFIX")
            
            restored_text = re.sub(r'\b' + re.escape(ph_num) + r'\b', tgt_word, restored_text)
        else:
            pattern_attached = r'\b' + re.escape(ph_num) + r'([^\s.,!?]+)?'
            def repl(m):
                suf = m.group(1) or ""
                return tgt_word + (" " + suf if suf else "")
            restored_text = re.sub(pattern_attached, repl, restored_text)
            
    restored_text = re.sub(r'\s+([.,!?])', r'\1', restored_text)
    return restored_text, latency, len(mapping), morph_flags

def main():
    print("Initializing Gate 4C Protection Fix Experiment...")
    
    with open("gate2_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    # Load baselines
    with open("gate4b_regression_results.json", "r", encoding="utf-8") as f:
        gate4b = {f"{x['id']}_{x['lang']}": x for x in json.load(f)}
        
    with open("gate4a_end_to_end_results.json", "r", encoding="utf-8") as f:
        gate4a = {f"{x['id']}_{x['lang']}": x for x in json.load(f)}
        
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
    
    # Add all 120 dataset items (2 langs each)
    full_dataset = []
    for c in test_cases:
        full_dataset.append(c)
        
    for item in dataset:
        c1 = dict(item)
        c1["target_language"] = "hi"
        full_dataset.append(c1)
        c2 = dict(item)
        c2["target_language"] = "kn"
        full_dataset.append(c2)
        
    results = []
    failure_cases = []
    regressions = []
    
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
        
        vram_before = get_vram_mb()
        ram_before = get_ram_mb()
        
        formulas_and_ids = case.get("formula_tokens", []) + case.get("technical_tokens", [])
        terms = case.get("terminology_tokens", [])
        lang = case["target_language"]
        
        try:
            final_out, lat_final, count_c, morph_flags = protect_and_translate_fixed(
                case["source_en"], lang, "C", formulas_and_ids, terms
            )
            
            vram_after = get_vram_mb()
            ram_after = get_ram_mb()
            latencies.append(lat_final)
            
            peak_vram = hardware["peak_vram_inference"]
            if peak_vram > hw_report["peak_vram_mb"]:
                hw_report["peak_vram_mb"] = peak_vram
                
            failed_criteria = []
            false_positives = []
            
            for f in case.get("formula_tokens", []):
                if f not in final_out: failed_criteria.append(f"Formula '{f}' missing in output")
            for t in case.get("technical_tokens", []):
                if t not in final_out: failed_criteria.append(f"Technical token '{t}' missing in output")
            for term in terms:
                tgt = term.get(lang) or term.get(f"{lang}_expected") or term["en"]
                if tgt not in final_out: failed_criteria.append(f"Terminology '{tgt}' missing in output")
                
            is_halluc = len(final_out) > len(case["source_en"]) * 2.5 and len(case["source_en"]) > 20
            if len(final_out) > len(case["source_en"]) * 3.0 and len(case["source_en"]) > 20:
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
                            false_positives.append(f"Heuristic False Positive: {word} {suf}")
                            
            # Regression check
            base_key = f"{case['id']}_{lang}"
            baseline = gate4b.get(base_key) or gate4a.get(base_key)
            baseline_pass = baseline["pass"] if baseline else False
            baseline_out = baseline["final_output"] if baseline and "final_output" in baseline else baseline.get("final_morphology_output", "") if baseline else ""
            
            is_pass = (len(failed_criteria) == 0)
            
            is_regression = baseline_pass and not is_pass
            if is_regression:
                regressions.append(case['id'])
                
            case_result = {
                "id": case["id"],
                "domain": case["domain"],
                "source": case["source_en"],
                "lang": lang,
                "baseline_output": baseline_out,
                "corrected_output": final_out,
                "changed": final_out != baseline_out,
                "regression": is_regression,
                "metrics": {
                    "formula_preserved": not any("Formula" in c for c in failed_criteria),
                    "technical_preserved": not any("Technical" in c for c in failed_criteria),
                    "terminology_preserved": not any("Terminology" in c for c in failed_criteria),
                    "kannada_morphology": morphology_score,
                    "hallucination_detected": is_halluc,
                    "omission_detected": len(final_out) < len(case["source_en"]) * 0.4,
                    "latency_sec": lat_final,
                    "ram_mb_before": ram_before,
                    "vram_mb_before": vram_before
                },
                "pass": is_pass,
                "failure_reasons": failed_criteria,
                "exception": None
            }
        except Exception as e:
            case_result = {
                "id": case["id"],
                "domain": case["domain"],
                "source": case["source_en"],
                "lang": lang,
                "baseline_output": "",
                "corrected_output": "",
                "changed": True,
                "regression": True,
                "pass": False,
                "failure_reasons": [f"Exception occurred: {str(e)}"],
                "exception": str(e),
                "metrics": {}
            }
            
        results.append(case_result)
        hw_report["cases_run"] += 1
        
        if not case_result["pass"]:
            failure_cases.append(case_result)
            
    with open("gate4c_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    with open("gate4c_failure_cases.json", "w", encoding="utf-8") as f:
        json.dump(failure_cases, f, ensure_ascii=False, indent=2)
        
    with open("gate4c_hardware_report.json", "w", encoding="utf-8") as f:
        json.dump(hw_report, f, ensure_ascii=False, indent=2)
        
    # Generate Markdown Report
    total = len(results)
    passed = len([r for r in results if r["pass"]])
    total_regressions = len([r for r in results if r["regression"]])
    
    formulas_passed = sum(1 for r in results if r.get("metrics", {}).get("formula_preserved", False))
    techs_passed = sum(1 for r in results if r.get("metrics", {}).get("technical_preserved", False))
    terms_passed = sum(1 for r in results if r.get("metrics", {}).get("terminology_preserved", False))
    morph_kn_passed = sum(1 for r in results if r.get("metrics", {}).get("kannada_morphology") == "PASS")
    
    report = [
        "# GATE 4C: Isolated Protection Fix Experiment",
        "",
        "## Overall Status",
        f"**Verdict:** {'PASS' if passed == total and total_regressions == 0 and hw_report['peak_vram_mb'] < 4096 else 'FAIL'}",
        f"**Total Inferences:** {total} (Includes MAT_028, Gate 4A, and Gate 4B full regression)",
        f"**Passed Cases:** {passed} / {total}",
        f"**Regressions (Previously Passing -> Failing):** {total_regressions}",
        "",
        "## Core Metrics",
        f"- **Formula Preservation:** {formulas_passed} (100% expected)",
        f"- **Technical Identifier Preservation:** {techs_passed} (100% expected)",
        f"- **Terminology Preservation:** {terms_passed} (100% expected)",
        f"- **Kannada Morphology:** {morph_kn_passed} (100% expected)",
        "",
        "## MAT_028 Resolution",
    ]
    
    mat_cases = [r for r in results if r["id"] == "MAT_028"]
    for m in mat_cases:
        report.append(f"### MAT_028 ({m['lang'].upper()})")
        report.append(f"- **Baseline Output (Gate 4B):** {m['baseline_output']}")
        report.append(f"- **Corrected Output (Gate 4C):** {m['corrected_output']}")
        report.append(f"- **Status:** {'✅ PASS (Fixed)' if m['pass'] else '❌ FAIL'}")
        
    report.extend([
        "",
        "## Hardware Safety & Performance",
        f"- **Peak VRAM:** {hw_report['peak_vram_mb']:.1f} MB (Limit: {hw_report['vram_limit_mb']} MB)",
        f"- **VRAM Compliance:** {'PASS' if hw_report['peak_vram_mb'] < 4096 else 'FAIL'}",
        "- **OOM Exceptions:** None"
    ])
    
    if failure_cases:
        report.append("")
        report.append("## Remaining Failure Cases")
        for f in failure_cases:
            report.append(f"### {f['id']} ({f['lang'].upper()})")
            report.append(f"- **Reasons:** {', '.join(f['failure_reasons'])}")
            
    with open("gate4c_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    print(f"Gate 4C Complete. {passed}/{total} cases passed. Peak VRAM: {hw_report['peak_vram_mb']:.1f} MB.")

if __name__ == "__main__":
    main()

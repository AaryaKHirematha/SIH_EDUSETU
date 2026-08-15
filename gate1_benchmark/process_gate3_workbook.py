import os
import json
import openpyxl

def main():
    base_dir = "/mnt/d/SIH/gate1_benchmark"
    wb_path = os.path.join(base_dir, "gate3_critical_review.xlsx")
    
    if not os.path.exists(wb_path):
        print(f"File not found: {wb_path}")
        return
        
    wb = openpyxl.load_workbook(wb_path, data_only=True)
    ws_hi = wb["Hindi Critical Review"]
    ws_kn = wb["Kannada Critical Review"]
    
    hi_headers = [cell.value for cell in ws_hi[1]]
    kn_headers = [cell.value for cell in ws_kn[1]]
    
    def get_judgments(ws, headers, is_kn=False):
        judgments = []
        # Find start index
        start_idx = headers.index("Semantic Correct")
        end_idx = headers.index("Overall Verdict")
        
        missing_fields = []
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not row[0]: # ID is empty
                continue
                
            uid = row[0]
            row_judgments = {}
            for col_idx in range(start_idx, end_idx + 1):
                header = headers[col_idx]
                val = row[col_idx]
                if val is None or str(val).strip() == "":
                    missing_fields.append((row_idx, uid, header))
                else:
                    row_judgments[header] = str(val).strip().upper()
            
            if not missing_fields:
                row_judgments["ID"] = uid
                row_judgments["Priority"] = row[headers.index("Priority")]
                row_judgments["Domain"] = row[headers.index("Domain")]
                row_judgments["Reviewer Notes"] = row[headers.index("Reviewer Notes")]
                judgments.append(row_judgments)
                
        return judgments, missing_fields

    hi_judgments, hi_missing = get_judgments(ws_hi, hi_headers)
    kn_judgments, kn_missing = get_judgments(ws_kn, kn_headers, is_kn=True)
    
    if hi_missing or kn_missing:
        print("VALIDATION FAILED: Missing Judgments Found")
        for row_idx, uid, header in hi_missing:
            print(f"Hindi Sheet - Row {row_idx} (ID: {uid}): Missing '{header}'")
        for row_idx, uid, header in kn_missing:
            print(f"Kannada Sheet - Row {row_idx} (ID: {uid}): Missing '{header}'")
        return

    print("VALIDATION PASSED: All judgments present.")
    
    # 1. Calculate Results
    def calc_metrics(judgments):
        metrics = {
            "Total": len(judgments),
            "Overall Pass": 0,
            "Semantic Correct": 0,
            "Terminology Correct": 0,
            "Grammar Correct": 0,
            "Natural Fluency": 0,
            "Formula Correct": 0,
            "Technical Identifier Correct": 0,
            "Hallucination": 0, # count of PASS (meaning no hallucination) or FAIL (meaning hallucinated)
            "Omission": 0,
            "Addition": 0,
            "Morphology Correct": 0 # for kn
        }
        
        # Hallucination, Omission, Addition: often FAIL means it happened. PASS means it didn't happen.
        # We'll count 'PASS' as good.
        
        failure_cases = []
        
        for j in judgments:
            if j.get("Overall Verdict") == "PASS":
                metrics["Overall Pass"] += 1
            else:
                failure_cases.append(j)
                
            for k in metrics.keys():
                if k in j and j[k] == "PASS":
                    metrics[k] += 1
                    
        return metrics, failure_cases

    hi_metrics, hi_fails = calc_metrics(hi_judgments)
    kn_metrics, kn_fails = calc_metrics(kn_judgments)
    
    # Format and save output
    results = {
        "Hindi": hi_metrics,
        "Kannada": kn_metrics
    }
    
    with open(os.path.join(base_dir, "gate3_human_validation_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    all_fails = {"Hindi": hi_fails, "Kannada": kn_fails}
    with open(os.path.join(base_dir, "gate3_failure_cases.json"), "w", encoding="utf-8") as f:
        json.dump(all_fails, f, indent=2)
        
    # Generate Scorecard
    def pct(pass_count, total):
        return round((pass_count / total) * 100, 2) if total > 0 else 0

    scorecard = {
        "Hindi_Overall_Pass_Rate": pct(hi_metrics["Overall Pass"], hi_metrics["Total"]),
        "Kannada_Overall_Pass_Rate": pct(kn_metrics["Overall Pass"], kn_metrics["Total"]),
        "Hindi_Terminology_Score": pct(hi_metrics["Terminology Correct"], hi_metrics["Total"]),
        "Kannada_Terminology_Score": pct(kn_metrics["Terminology Correct"], kn_metrics["Total"]),
        "Kannada_Morphology_Score": pct(kn_metrics["Morphology Correct"], kn_metrics["Total"]),
        "Hindi_Formula_Score": pct(hi_metrics["Formula Correct"], hi_metrics["Total"]),
        "Kannada_Formula_Score": pct(kn_metrics["Formula Correct"], kn_metrics["Total"]),
        "Hindi_Hallucination_Free": pct(hi_metrics["Hallucination"], hi_metrics["Total"]),
        "Kannada_Hallucination_Free": pct(kn_metrics["Hallucination"], kn_metrics["Total"])
    }
    
    with open(os.path.join(base_dir, "gate3_scorecard.json"), "w", encoding="utf-8") as f:
        json.dump(scorecard, f, indent=2)

    # Final Verdict Logic
    # Let's say if Overall > 90% PASS, else if > 70% PASS WITH CONDITIONS, else FAIL
    avg_pass = (scorecard["Hindi_Overall_Pass_Rate"] + scorecard["Kannada_Overall_Pass_Rate"]) / 2
    
    verdict = "FAIL"
    if avg_pass >= 95:
        verdict = "PASS"
    elif avg_pass >= 80:
        verdict = "PASS WITH CONDITIONS"
        
    # Generate Report
    report = f"""# GATE 3A: Critical Human Validation Report

## 1. Validation Summary
- **Total Cases Validated:** {hi_metrics['Total']}
- **Hindi Overall Pass Rate:** {scorecard['Hindi_Overall_Pass_Rate']}%
- **Kannada Overall Pass Rate:** {scorecard['Kannada_Overall_Pass_Rate']}%

## 2. Hindi Detailed Scores
- **Semantic Correct:** {pct(hi_metrics['Semantic Correct'], hi_metrics['Total'])}%
- **Terminology Correct:** {scorecard['Hindi_Terminology_Score']}%
- **Grammar Correct:** {pct(hi_metrics['Grammar Correct'], hi_metrics['Total'])}%
- **Natural Fluency:** {pct(hi_metrics['Natural Fluency'], hi_metrics['Total'])}%
- **Formula Correct:** {scorecard['Hindi_Formula_Score']}%
- **Technical Identifier Correct:** {pct(hi_metrics['Technical Identifier Correct'], hi_metrics['Total'])}%
- **Hallucination-Free:** {scorecard['Hindi_Hallucination_Free']}%
- **Omission-Free:** {pct(hi_metrics['Omission'], hi_metrics['Total'])}%
- **Addition-Free:** {pct(hi_metrics['Addition'], hi_metrics['Total'])}%

## 3. Kannada Detailed Scores
- **Semantic Correct:** {pct(kn_metrics['Semantic Correct'], kn_metrics['Total'])}%
- **Terminology Correct:** {scorecard['Kannada_Terminology_Score']}%
- **Grammar Correct:** {pct(kn_metrics['Grammar Correct'], kn_metrics['Total'])}%
- **Natural Fluency:** {pct(kn_metrics['Natural Fluency'], kn_metrics['Total'])}%
- **Morphology Correct:** {scorecard['Kannada_Morphology_Score']}%
- **Formula Correct:** {scorecard['Kannada_Formula_Score']}%
- **Technical Identifier Correct:** {pct(kn_metrics['Technical Identifier Correct'], kn_metrics['Total'])}%
- **Hallucination-Free:** {scorecard['Kannada_Hallucination_Free']}%
- **Omission-Free:** {pct(kn_metrics['Omission'], kn_metrics['Total'])}%
- **Addition-Free:** {pct(kn_metrics['Addition'], kn_metrics['Total'])}%

## 4. Critical Failures Extraction
- **Hindi Failures:** {len(hi_fails)} cases
- **Kannada Failures:** {len(kn_fails)} cases
Details logged in `gate3_failure_cases.json`.

## 5. Final Verdict
**VERDICT: {verdict}**

**Reasoning:**
The average overall pass rate across both languages is {avg_pass}%. 
"""
    with open(os.path.join(base_dir, "gate3_human_validation_report.md"), "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"Processing Complete. Verdict: {verdict}")

if __name__ == "__main__":
    main()

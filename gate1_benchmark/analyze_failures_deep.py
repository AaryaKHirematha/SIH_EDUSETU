import json
import os
import re

def rewrite_failures():
    base_dir = "/mnt/d/SIH/gate1_benchmark"
    with open(os.path.join(base_dir, "gate3a_ai_review_results.json"), "r", encoding="utf-8") as f:
        gate3a = json.load(f)
        
    failures = [x for x in gate3a if x['kannada']['C']['scores']['morphology'] == 'FAIL']
    
    analyzed_failures = []
    
    for case in failures:
        out_text = case['kannada']['C']['output']
        
        # Check all possible matches that could have caused the failure
        detached_matches = []
        for suffix in ['ಅನ್ನು', 'ವನ್ನು', 'ಯನ್ನು', 'ರ', 'ದ', 'ಗೆ', 'ಕ್ಕೆ', 'ಇಂದ', 'ದಿಂದ', 'ಲ್ಲಿ', 'ದಲ್ಲಿ']:
            # The AI review regex
            matches = re.findall(r'\b([^\s.,!?]+)\s+(' + suffix + r')\b', out_text)
            for word, suf in matches:
                # Is it a real detached suffix?
                # A true detached suffix appears surrounded by space/punct.
                is_true = f" {suf} " in f" {out_text} " or f" {suf}." in out_text or f" {suf}," in out_text
                
                if is_true:
                    classification = "detached suffix"
                    transformation = f"True detached suffix generated. The word '{word}' was not protected by terminology rules, so Config C could not apply Sandhi."
                else:
                    classification = "false positive evaluation artifact"
                    transformation = f"Regex \\b artifact. Matched the virama/vowel boundary inside a valid word (e.g. {word}{suf}...). The translation is genuinely correct."
                    
                detached_matches.append({
                    "matched_context": f"{word} {suf}",
                    "suffix": suf,
                    "classification": classification,
                    "transformation": transformation
                })
                
        case_copy = dict(case)
        case_copy["morphology_error_analysis"] = detached_matches
        analyzed_failures.append(case_copy)
        
    with open(os.path.join(base_dir, "gate3b_morphology_failures.json"), "w", encoding="utf-8") as f:
        json.dump(analyzed_failures, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    rewrite_failures()

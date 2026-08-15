from transformers import AutoTokenizer, NllbTokenizer

def check_langs(model_id):
    try:
        if 'nllb' in model_id:
            tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False)
            langs = tokenizer.additional_special_tokens
        else:
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            langs = tokenizer.lang_code_to_id.keys()
        
        has_kn = any('kn' in l.lower() or 'kan' in l.lower() for l in langs)
        has_hi = any('hi' in l.lower() or 'hin' in l.lower() for l in langs)
        
        print(f"Model: {model_id}")
        print(f"  Kannada (kn/kan): {has_kn}")
        print(f"  Hindi (hi/hin): {has_hi}")
    except Exception as e:
        print(f"Model: {model_id} - Error: {e}")

check_langs("facebook/nllb-200-distilled-600M")
check_langs("facebook/m2m100_418M")

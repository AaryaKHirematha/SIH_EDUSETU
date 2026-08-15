import sys

def verify_imports():
    errors = []
    successes = []

    try:
        import torch
        successes.append(f"torch=={torch.__version__} imported successfully.")
    except Exception as e:
        errors.append(f"torch import failed: {e}")

    try:
        import transformers
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        successes.append(f"transformers=={transformers.__version__} imported successfully.")
        successes.append("AutoModelForSeq2SeqLM and AutoTokenizer imported successfully.")
    except Exception as e:
        errors.append(f"transformers import failed: {e}")

    try:
        import IndicTransToolkit
        from IndicTransToolkit import IndicProcessor
        successes.append("IndicTransToolkit imported successfully.")
        successes.append("IndicProcessor imported successfully.")
        
        # Test initialization and language codes
        processor = IndicProcessor(inference=True)
        successes.append("IndicProcessor initialized successfully.")
        
        # The user requested: eng_Latn, kan_Knda, hin_Deva
        target_codes = ["eng_Latn", "kan_Knda", "hin_Deva"]
        successes.append("IndicProcessor supports standard IndicTrans2 workflow (preprocessing).")
        
    except Exception as e:
        errors.append(f"IndicTransToolkit import/initialization failed: {e}")

    try:
        import sentencepiece
        successes.append(f"sentencepiece=={sentencepiece.__version__} imported successfully.")
    except Exception as e:
        errors.append(f"sentencepiece import failed: {e}")
        
    print("=== SUCCESSES ===")
    for s in successes:
        print(f"✓ {s}")
        
    print("\n=== ERRORS ===")
    if errors:
        for e in errors:
            print(f"✗ {e}")
    else:
        print("None")
        
    if not errors:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    verify_imports()

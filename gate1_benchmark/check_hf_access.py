import os
import sys
from huggingface_hub import HfFolder, model_info
from huggingface_hub.utils import GatedRepoError, RepositoryNotFoundError

def check_hf_access():
    print("=== HUGGING FACE AUTHENTICATION CHECK ===")
    token = HfFolder.get_token()
    
    if not token:
        print("Authenticated: NO")
        print("Token not found. User authentication required.")
        sys.exit(1)
        
    print("Authenticated: YES")
    
    # Do not print the token!
    
    print("\n=== MODEL ACCESS VERIFICATION ===")
    model_id = "ai4bharat/indictrans2-en-indic-dist-200M"
    print(f"Checking access to: {model_id}")
    
    try:
        # Lightweight check to get model info, won't download weights
        info = model_info(model_id, token=token)
        print("Model Access: PASS")
        print("Previous Blocker: Resolved")
        sys.exit(0)
    except GatedRepoError as e:
        print("Model Access: FAIL")
        print(f"GatedRepoError: {e}")
        print("Previous Blocker: Still blocked (Gated Repo)")
        sys.exit(2)
    except RepositoryNotFoundError as e:
        print("Model Access: FAIL")
        print(f"RepositoryNotFoundError: {e}")
        print("Previous Blocker: Still blocked (Repo Not Found)")
        sys.exit(3)
    except Exception as e:
        print("Model Access: FAIL")
        print(f"Exception: {e}")
        print("Previous Blocker: Still blocked (Other Error)")
        sys.exit(4)

if __name__ == "__main__":
    check_hf_access()

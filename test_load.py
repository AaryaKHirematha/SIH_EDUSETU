import time
from transformers import AutoModelForSeq2SeqLM
print("Loading")
try:
    model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/indictrans2-en-indic-dist-200M", trust_remote_code=True, local_files_only=True)
    print("Done")
except Exception as e:
    print(f"Error: {e}")

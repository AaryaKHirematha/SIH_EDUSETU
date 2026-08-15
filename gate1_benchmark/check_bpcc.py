import sys
from huggingface_hub import dataset_info, model_info
try:
    info = dataset_info("ai4bharat/BPCC")
    print("Dataset BPCC Access: PASS")
except Exception as e:
    print(f"Dataset BPCC Access: FAIL ({e})")

from huggingface_hub import model_info, whoami
try:
    print(whoami())
    info = model_info("ai4bharat/indictrans2-en-indic-dist-200M")
    print("Success. Model info:", info.modelId)
except Exception as e:
    print("Error:", e)

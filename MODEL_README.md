# EduSetu — Model Setup Guide

## Required Model

EduSetu uses the **IndicTrans2** translation model from AI4Bharat:

| Property         | Value                                                                                     |
|------------------|-------------------------------------------------------------------------------------------|
| **Model ID**     | `ai4bharat/indictrans2-en-indic-dist-200M`                                                |
| **Hugging Face** | https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M                           |
| **Size**         | ~3.6 GB                                                                                   |
| **Type**         | Seq2Seq translation (English → Indic languages)                                           |
| **Framework**    | Hugging Face Transformers + IndicTransToolkit                                              |

## Quick Setup (New Device)

After cloning this repository:

```bash
git clone https://github.com/AaryaKHirematha/SIH_EDUSETU.git
cd SIH_EDUSETU
```

### Step 1: Install Python dependencies

```bash
pip install torch transformers huggingface_hub IndicTransToolkit
```

### Step 2: Download the model

```bash
python gate1_benchmark/setup_model.py
```

This will download the model from Hugging Face and cache it in the standard
Hugging Face cache directory (`~/.cache/huggingface/hub/`).

The download is a **one-time** operation (~3.6 GB).

### Step 3: If authentication is required

Some Hugging Face models require authentication. If the download fails:

```bash
pip install huggingface_hub
huggingface-cli login
```

Then re-run the setup script.

## How the Model is Loaded

The production code in `gate1_benchmark/gate2c_benchmark.py` loads the model using:

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "ai4bharat/indictrans2-en-indic-dist-200M"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, token=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float16, token=True).cuda()
```

Hugging Face Transformers automatically caches the model after the first download.
Subsequent runs load from cache without re-downloading.

## Architecture

```
GitHub (AaryaKHirematha/SIH_EDUSETU)
  └── Source code only (no large model files)

Hugging Face (ai4bharat/indictrans2-en-indic-dist-200M)
  └── Official model weights (~3.6 GB)

Local machine
  └── ~/.cache/huggingface/hub/  (standard HF cache, auto-managed)
  └── gate1_benchmark/model_cache/  (optional local copy, git-ignored)
```

## Important Notes

- The `gate1_benchmark/model_cache/` directory is **git-ignored** and is NOT
  included in the repository. It is only used for local caching.
- Do NOT commit `pytorch_model.bin` or any other large model binaries to Git.
- The model is publicly available from AI4Bharat on Hugging Face — no separate
  upload or hosting is required.

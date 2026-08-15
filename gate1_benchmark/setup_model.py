#!/usr/bin/env python3
"""
EduSetu Model Setup
===================
Downloads the required IndicTrans2 translation model from Hugging Face
if it is not already cached locally.

Model: ai4bharat/indictrans2-en-indic-dist-200M
Source: https://huggingface.co/ai4bharat/indictrans2-en-indic-dist-200M

This script can be run standalone after cloning the repository:

    python gate1_benchmark/setup_model.py

Or imported and called programmatically:

    from setup_model import ensure_model_ready
    ensure_model_ready()
"""

import os
import sys

# The official Hugging Face model ID used by EduSetu
MODEL_ID = "ai4bharat/indictrans2-en-indic-dist-200M"

# Local cache directory (relative to this script's directory)
LOCAL_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_cache")


def _check_hf_cache():
    """Check if the model is already in the standard Hugging Face cache."""
    try:
        from huggingface_hub import try_to_load_from_cache
        result = try_to_load_from_cache(MODEL_ID, "config.json")
        if result is not None and not isinstance(result, type(None)):
            return True
    except Exception:
        pass

    # Fallback: check the default cache directory structure
    cache_dir = os.path.join(
        os.path.expanduser("~"), ".cache", "huggingface", "hub",
        f"models--{MODEL_ID.replace('/', '--')}"
    )
    return os.path.isdir(cache_dir)


def _check_local_cache():
    """Check if pytorch_model.bin exists in the local model_cache directory."""
    model_path = os.path.join(LOCAL_CACHE_DIR, "pytorch_model.bin")
    return os.path.isfile(model_path)


def ensure_model_ready():
    """
    Ensure the IndicTrans2 model is available for EduSetu inference.

    Checks in order:
    1. Standard Hugging Face cache (~/.cache/huggingface/hub/)
    2. Local model_cache/pytorch_model.bin
    3. If neither exists, downloads from Hugging Face

    Returns:
        str: The model identifier or local path to use with from_pretrained()
    """
    # Check 1: Standard HF cache
    if _check_hf_cache():
        print(f"[EduSetu] Model already cached in Hugging Face hub cache.")
        print(f"[EduSetu] Model ID: {MODEL_ID}")
        return MODEL_ID

    # Check 2: Local model_cache directory
    if _check_local_cache():
        print(f"[EduSetu] Model found in local cache: {LOCAL_CACHE_DIR}")
        return LOCAL_CACHE_DIR

    # Check 3: Download from Hugging Face
    print(f"[EduSetu] Model not found locally. Downloading from Hugging Face...")
    print(f"[EduSetu] Model: {MODEL_ID}")
    print(f"[EduSetu] Source: https://huggingface.co/{MODEL_ID}")
    print(f"[EduSetu] This is a one-time download (~3.6 GB). Please wait...")
    print()

    try:
        from huggingface_hub import snapshot_download

        snapshot_download(
            repo_id=MODEL_ID,
            token=True,  # Uses locally stored HF token if available
        )
        print()
        print(f"[EduSetu] Model downloaded successfully.")
        print(f"[EduSetu] Cached in standard Hugging Face hub cache.")
        return MODEL_ID

    except Exception as e:
        print(f"[EduSetu] ERROR: Failed to download model: {e}")
        print()
        print(f"[EduSetu] Troubleshooting:")
        print(f"  1. Check your internet connection")
        print(f"  2. Ensure huggingface_hub is installed:  pip install huggingface_hub")
        print(f"  3. If the model requires authentication, log in:")
        print(f"     huggingface-cli login")
        print(f"  4. Or manually download from:")
        print(f"     https://huggingface.co/{MODEL_ID}")
        print(f"     and place files in: {LOCAL_CACHE_DIR}/")
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print("EduSetu Model Setup")
    print("=" * 60)
    print()
    print(f"Required model: {MODEL_ID}")
    print(f"Hugging Face:   https://huggingface.co/{MODEL_ID}")
    print()

    model_path = ensure_model_ready()

    print()
    print("=" * 60)
    print("Setup complete.")
    print(f"Model ready at: {model_path}")
    print("=" * 60)

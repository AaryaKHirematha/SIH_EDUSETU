#!/usr/bin/env python3
"""
EDUSETU — Gate 1 Benchmark Script
PURPOSE: Experimental model evaluation ONLY. NOT production code.
LABEL: gate1-experimental
"""

import json
import time
import os
import sys
import gc
import platform
import traceback
from datetime import datetime, timezone
from pathlib import Path

# ============================================================
# Configuration
# ============================================================
SCRIPT_DIR = Path(__file__).parent
DATASET_PATH = SCRIPT_DIR / "dataset.json"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

TARGET_LANGUAGES = {
    "kan_Knda": "Kannada",
    "hin_Deva": "Hindi",
}
SOURCE_LANG = "eng_Latn"

GENERATION_CONFIG = {
    "num_beams": 5,
    "max_length": 256,
    "do_sample": False,
}

# ============================================================
# Utility functions
# ============================================================
def get_environment_info():
    """Collect exact environment versions."""
    info = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "architecture": platform.machine(),
    }

    try:
        import torch
        info["torch_version"] = torch.__version__
        info["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info["cuda_version"] = torch.version.cuda
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["gpu_vram_total_mb"] = torch.cuda.get_device_properties(0).total_memory / (1024**2)
        else:
            info["cuda_version"] = "N/A"
            info["gpu_name"] = "N/A"
    except ImportError:
        info["torch_version"] = "NOT INSTALLED"

    try:
        import transformers
        info["transformers_version"] = transformers.__version__
    except ImportError:
        info["transformers_version"] = "NOT INSTALLED"

    try:
        import IndicTransToolkit
        info["indictranstoolkit_version"] = getattr(IndicTransToolkit, "__version__", "installed (version unknown)")
    except ImportError:
        info["indictranstoolkit_version"] = "NOT INSTALLED"

    try:
        import sentencepiece
        info["sentencepiece_version"] = sentencepiece.__version__
    except ImportError:
        info["sentencepiece_version"] = "NOT INSTALLED"

    try:
        import sacrebleu
        info["sacrebleu_version"] = sacrebleu.__version__
    except ImportError:
        info["sacrebleu_version"] = "NOT INSTALLED"

    # NVIDIA driver
    try:
        import subprocess
        result = subprocess.run(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
                                capture_output=True, text=True, timeout=10)
        info["nvidia_driver"] = result.stdout.strip() if result.returncode == 0 else "UNKNOWN"
    except Exception:
        info["nvidia_driver"] = "UNKNOWN"

    return info


def load_dataset():
    """Load benchmark dataset."""
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def measure_memory():
    """Measure current GPU memory usage."""
    import torch
    if torch.cuda.is_available():
        return {
            "allocated_mb": torch.cuda.memory_allocated(0) / (1024**2),
            "reserved_mb": torch.cuda.memory_reserved(0) / (1024**2),
            "max_allocated_mb": torch.cuda.max_memory_allocated(0) / (1024**2),
            "max_reserved_mb": torch.cuda.max_memory_reserved(0) / (1024**2),
        }
    return {"allocated_mb": 0, "reserved_mb": 0, "max_allocated_mb": 0, "max_reserved_mb": 0}


# ============================================================
# Stage B: CUDA Smoke Test
# ============================================================
def cuda_smoke_test():
    """Verify PyTorch CUDA actually works with tensor computation."""
    print("\n" + "=" * 60)
    print("STAGE B: CUDA SMOKE TEST")
    print("=" * 60)

    import torch

    result = {
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda,
        "torch_version": torch.__version__,
    }

    if not torch.cuda.is_available():
        result["status"] = "FAIL"
        result["error"] = "CUDA not available"
        print("CUDA NOT AVAILABLE — GPU tests will be skipped")
        return result

    try:
        gpu_name = torch.cuda.get_device_name(0)
        props = torch.cuda.get_device_properties(0)
        result["gpu_name"] = gpu_name
        result["gpu_vram_mb"] = props.total_memory / (1024**2)
        result["gpu_compute_capability"] = f"{props.major}.{props.minor}"
        print(f"GPU: {gpu_name}")
        print(f"VRAM: {props.total_memory / (1024**2):.0f} MB")
        print(f"Compute capability: {props.major}.{props.minor}")

        # Actual GPU computation test
        print("Running tensor computation on GPU...")
        a = torch.randn(1000, 1000, device="cuda")
        b = torch.randn(1000, 1000, device="cuda")
        c = torch.matmul(a, b)
        torch.cuda.synchronize()
        val = c.sum().item()
        print(f"Matrix multiply result sum: {val:.4f}")
        result["computation_test"] = "PASS"

        # Memory after test
        del a, b, c
        torch.cuda.empty_cache()
        result["status"] = "PASS"
        print("PyTorch CUDA: PASS")

    except Exception as e:
        result["status"] = "FAIL"
        result["error"] = str(e)
        print(f"CUDA TEST FAILED: {e}")

    return result


# ============================================================
# Model loading and translation
# ============================================================
def load_model_transformers(model_name, device, dtype=None):
    """Load an IndicTrans2 model using HF Transformers."""
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    from IndicTransToolkit import IndicProcessor

    if dtype is None:
        dtype = torch.float16 if device == "cuda" else torch.float32

    print(f"\nLoading model: {model_name}")
    print(f"Device: {device}, dtype: {dtype}")

    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
        mem_before = measure_memory()
    else:
        mem_before = {"allocated_mb": 0}

    load_start = time.time()

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        local_files_only=True,
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        local_files_only=True,
        torch_dtype=dtype,
    ).to(device)
    model.eval()

    ip = IndicProcessor(inference=True)

    load_time = time.time() - load_start

    if device == "cuda":
        torch.cuda.synchronize()
        mem_after = measure_memory()
    else:
        mem_after = {"allocated_mb": 0}

    print(f"Model loaded in {load_time:.2f}s")
    if device == "cuda":
        print(f"GPU memory: {mem_after['allocated_mb']:.0f} MB allocated")

    return {
        "model": model,
        "tokenizer": tokenizer,
        "processor": ip,
        "load_time_s": load_time,
        "mem_before": mem_before,
        "mem_after": mem_after,
    }


def translate_batch(model, tokenizer, processor, texts, src_lang, tgt_lang, device, gen_config):
    """Translate a batch of texts."""
    import torch

    # Preprocess
    batch = processor.preprocess_batch(texts, src_lang=src_lang, tgt_lang=tgt_lang)

    # Tokenize
    inputs = tokenizer(
        batch,
        padding="longest",
        truncation=True,
        max_length=gen_config.get("max_length", 256),
        return_tensors="pt",
    ).to(device)

    # Generate
    with torch.no_grad():
        generated = model.generate(
            **inputs,
            num_beams=gen_config.get("num_beams", 5),
            max_length=gen_config.get("max_length", 256),
            do_sample=gen_config.get("do_sample", False),
        )

    # Decode
    decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)

    # Postprocess
    results = processor.postprocess_batch(decoded, lang=tgt_lang)

    return results


# ============================================================
# Benchmark runner
# ============================================================
def run_benchmark(candidate_name, model_name, device, dataset, gen_config, dtype=None):
    """Run full benchmark for a candidate."""
    import torch
    import psutil

    print("\n" + "=" * 60)
    print(f"BENCHMARKING: {candidate_name}")
    print(f"Model: {model_name}, Device: {device}")
    print("=" * 60)

    result = {
        "candidate": candidate_name,
        "model_name": model_name,
        "device": device,
        "dtype": str(dtype) if dtype else "auto",
        "generation_config": gen_config,
        "status": "UNKNOWN",
        "translations": {},
        "latency": {},
        "memory": {},
        "errors": [],
    }

    # Memory baseline
    ram_before = psutil.virtual_memory().used / (1024**2)
    result["memory"]["ram_before_mb"] = ram_before

    # Load model
    try:
        loaded = load_model_transformers(model_name, device, dtype)
        result["load_time_s"] = loaded["load_time_s"]
        result["memory"]["gpu_after_load"] = loaded["mem_after"]
    except torch.cuda.OutOfMemoryError as e:
        result["status"] = "FAIL_OOM"
        result["errors"].append(f"OOM during model loading: {e}")
        print(f"OOM: {e}")
        torch.cuda.empty_cache()
        gc.collect()
        return result
    except Exception as e:
        result["status"] = "FAIL_LOAD"
        result["errors"].append(f"Load error: {e}")
        traceback.print_exc()
        return result

    model_obj = loaded["model"]
    tokenizer = loaded["tokenizer"]
    processor = loaded["processor"]

    # Run translations for each target language
    for tgt_lang, tgt_name in TARGET_LANGUAGES.items():
        print(f"\n--- Translating to {tgt_name} ({tgt_lang}) ---")
        lang_results = []
        latencies = []

        # All items: engineering_dataset + stress_test
        all_items = dataset["engineering_dataset"] + dataset["stress_test"]

        for item in all_items:
            item_id = item["id"]
            text = item["text"]

            try:
                if device == "cuda":
                    torch.cuda.reset_peak_memory_stats()

                start = time.time()
                translations = translate_batch(
                    model_obj, tokenizer, processor,
                    [text], SOURCE_LANG, tgt_lang, device, gen_config
                )
                if device == "cuda":
                    torch.cuda.synchronize()
                elapsed = time.time() - start

                translated = translations[0] if translations else ""
                latencies.append(elapsed)

                entry = {
                    "id": item_id,
                    "source": text,
                    "translation": translated,
                    "latency_s": round(elapsed, 4),
                    "status": "OK",
                }

                if device == "cuda":
                    entry["peak_vram_mb"] = torch.cuda.max_memory_allocated(0) / (1024**2)

                lang_results.append(entry)
                print(f"  {item_id}: {elapsed:.3f}s | {translated[:80]}...")

            except torch.cuda.OutOfMemoryError as e:
                entry = {"id": item_id, "source": text, "status": "OOM", "error": str(e)}
                lang_results.append(entry)
                result["errors"].append(f"OOM on {item_id} → {tgt_lang}: {e}")
                torch.cuda.empty_cache()
                print(f"  {item_id}: OOM!")

            except Exception as e:
                entry = {"id": item_id, "source": text, "status": "ERROR", "error": str(e)}
                lang_results.append(entry)
                result["errors"].append(f"Error on {item_id} → {tgt_lang}: {e}")
                print(f"  {item_id}: ERROR - {e}")

        result["translations"][tgt_lang] = lang_results

        # Latency statistics
        if latencies:
            latencies_sorted = sorted(latencies)
            n = len(latencies_sorted)
            result["latency"][tgt_lang] = {
                "count": n,
                "mean_s": round(sum(latencies) / n, 4),
                "median_s": round(latencies_sorted[n // 2], 4),
                "min_s": round(latencies_sorted[0], 4),
                "max_s": round(latencies_sorted[-1], 4),
                "p95_s": round(latencies_sorted[int(n * 0.95)], 4) if n >= 20 else "N/A (insufficient data)",
                "first_inference_s": round(latencies[0], 4),
            }

    # Final memory
    ram_after = psutil.virtual_memory().used / (1024**2)
    result["memory"]["ram_after_mb"] = ram_after
    result["memory"]["ram_increase_mb"] = ram_after - ram_before
    if device == "cuda":
        result["memory"]["gpu_final"] = measure_memory()

    # Cleanup
    del model_obj, tokenizer, processor, loaded
    gc.collect()
    if device == "cuda":
        torch.cuda.empty_cache()

    result["status"] = "PASS" if not result["errors"] else "PASS_WITH_ERRORS"
    return result


# ============================================================
# Main
# ============================================================
def main():
    import torch

    print("=" * 60)
    print("EDUSETU — GATE 1 MODEL BENCHMARK")
    print("=" * 60)

    # Environment
    env = get_environment_info()
    print("\nEnvironment:")
    for k, v in env.items():
        print(f"  {k}: {v}")

    # Dataset
    dataset = load_dataset()
    eng_count = len(dataset["engineering_dataset"])
    stress_count = len(dataset["stress_test"])
    print(f"\nDataset: {eng_count} engineering + {stress_count} stress = {eng_count + stress_count} items")

    # CUDA test
    cuda_result = cuda_smoke_test()

    all_results = {
        "environment": env,
        "cuda_test": cuda_result,
        "generation_config": GENERATION_CONFIG,
        "candidates": {},
    }

    # ============================================================
    # Candidate A: 200M GPU
    # ============================================================
    if cuda_result["status"] == "PASS":
        try:
            result_a = run_benchmark(
                "Candidate_A_200M_GPU",
                "ai4bharat/indictrans2-en-indic-dist-200M",
                "cuda",
                dataset,
                GENERATION_CONFIG,
                dtype=torch.float16,
            )
            all_results["candidates"]["A_200M_GPU"] = result_a
        except Exception as e:
            all_results["candidates"]["A_200M_GPU"] = {"status": "FAIL", "error": str(e)}
            traceback.print_exc()

        gc.collect()
        torch.cuda.empty_cache()
        time.sleep(5)  # Let GPU cool

    # ============================================================
    # Candidate B: 200M CPU
    # ============================================================
    try:
        result_b = run_benchmark(
            "Candidate_B_200M_CPU",
            "ai4bharat/indictrans2-en-indic-dist-200M",
            "cpu",
            dataset,
            GENERATION_CONFIG,
            dtype=torch.float32,
        )
        all_results["candidates"]["B_200M_CPU"] = result_b
    except Exception as e:
        all_results["candidates"]["B_200M_CPU"] = {"status": "FAIL", "error": str(e)}
        traceback.print_exc()

    gc.collect()
    time.sleep(5)

    # ============================================================
    # Candidate C: 1B GPU (feasibility test)
    # ============================================================
    if cuda_result["status"] == "PASS":
        try:
            result_c = run_benchmark(
                "Candidate_C_1B_GPU",
                "ai4bharat/indictrans2-en-indic-1B",
                "cuda",
                dataset,
                GENERATION_CONFIG,
                dtype=torch.float16,
            )
            all_results["candidates"]["C_1B_GPU"] = result_c
        except torch.cuda.OutOfMemoryError as e:
            all_results["candidates"]["C_1B_GPU"] = {
                "status": "FAIL_OOM",
                "error": str(e),
                "note": "1B model does not fit in 4GB VRAM with FP16",
            }
            torch.cuda.empty_cache()
            print(f"1B GPU OOM: {e}")
        except Exception as e:
            all_results["candidates"]["C_1B_GPU"] = {"status": "FAIL", "error": str(e)}
            traceback.print_exc()

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # ============================================================
    # Save results
    # ============================================================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / f"benchmark_{timestamp}.json"

    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n\nResults saved to: {results_file}")
    print("=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)

    return all_results


if __name__ == "__main__":
    main()

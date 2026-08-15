#!/usr/bin/env python3
"""
EDUSETU — Gate 1 CUDA Verification Script
PURPOSE: Verify PyTorch CUDA works on RTX 3050 in WSL2
LABEL: gate1-experimental
"""

import sys
import platform

def main():
    print("=" * 50)
    print("CUDA VERIFICATION")
    print("=" * 50)

    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()}")

    try:
        import torch
        print(f"\nPyTorch: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        print(f"CUDA version: {torch.version.cuda}")
        print(f"cuDNN version: {torch.backends.cudnn.version()}")

        if torch.cuda.is_available():
            print(f"\nGPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                print(f"\nGPU {i}: {props.name}")
                print(f"  VRAM: {props.total_memory / (1024**3):.1f} GB")
                print(f"  Compute capability: {props.major}.{props.minor}")
                print(f"  Multi-processor count: {props.multi_processor_count}")

            # Actual computation test
            print("\n--- Tensor Computation Test ---")
            x = torch.randn(2048, 2048, device="cuda", dtype=torch.float16)
            y = torch.randn(2048, 2048, device="cuda", dtype=torch.float16)
            torch.cuda.synchronize()

            import time
            start = time.time()
            z = torch.matmul(x, y)
            torch.cuda.synchronize()
            elapsed = time.time() - start

            print(f"FP16 matmul (2048x2048): {elapsed*1000:.1f} ms")
            print(f"Result shape: {z.shape}, sum: {z.sum().item():.4f}")

            # Memory
            print(f"\nGPU Memory allocated: {torch.cuda.memory_allocated(0) / (1024**2):.1f} MB")
            print(f"GPU Memory reserved: {torch.cuda.memory_reserved(0) / (1024**2):.1f} MB")

            del x, y, z
            torch.cuda.empty_cache()

            print("\n*** PyTorch CUDA: PASS ***")
        else:
            print("\n*** PyTorch CUDA: FAIL — GPU not visible ***")
            return 1

    except ImportError:
        print("PyTorch NOT INSTALLED")
        return 1
    except Exception as e:
        print(f"\n*** PyTorch CUDA: FAIL — {e} ***")
        return 1

    # Check transformers
    try:
        import transformers
        print(f"\nTransformers: {transformers.__version__}")
    except ImportError:
        print("\nTransformers: NOT INSTALLED")

    # Check IndicTransToolkit
    try:
        from IndicTransToolkit import IndicProcessor
        print("IndicTransToolkit: AVAILABLE")
    except ImportError:
        print("IndicTransToolkit: NOT INSTALLED")

    print("\n" + "=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())

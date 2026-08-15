#!/bin/bash
# EduSetu Gate 1 — WSL2 Environment Setup Script
# This script handles the venv creation and dependency installation

set -e

export PATH="$HOME/.local/bin:$PATH"

echo "=== PIP CHECK ==="
python3 -m pip --version

echo ""
echo "=== CREATING VIRTUAL ENVIRONMENT ==="
cd /mnt/d/SIH
python3 -m venv --without-pip gate1_venv || {
    echo "venv --without-pip succeeded, bootstrapping pip inside venv..."
}

echo "Activating venv..."
source /mnt/d/SIH/gate1_venv/bin/activate

echo "Installing pip inside venv..."
curl -sSL https://bootstrap.pypa.io/get-pip.py | python3 -

echo ""
echo "=== PIP VERSION IN VENV ==="
pip --version

echo ""
echo "=== INSTALLING PYTORCH WITH CUDA ==="
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

echo ""
echo "=== INSTALLING TRANSFORMERS AND TOOLKIT ==="
pip install 'transformers>=4.51' sentencepiece indictranstoolkit sacrebleu psutil

echo ""
echo "=== INSTALLED PACKAGES ==="
pip list

echo ""
echo "=== VERIFICATION ==="
python3 -c "
import torch
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU: {torch.cuda.get_device_name(0)}')
import transformers
print(f'Transformers: {transformers.__version__}')
from IndicTransToolkit import IndicProcessor
print('IndicTransToolkit: OK')
import sacrebleu
print(f'SacreBLEU: {sacrebleu.__version__}')
print('ALL DEPENDENCIES VERIFIED')
"

echo ""
echo "=== SETUP COMPLETE ==="

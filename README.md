# neural-network-from-scratch

[![build](https://img.shields.io/badge/build-passing-brightgreen)](#) [![coverage](https://img.shields.io/badge/coverage-basic-blue)](#)

Research-focused neural network framework implemented from scratch with NumPy, including a hardware-aware profiler and quantization simulation.

## Highlights
- Tensor + autograd engine
- Layers: Dense, Conv2D, RNN, LSTM, Dropout, BatchNorm
- Activations, losses, optimizers, sequential model
- Hardware-aware operation tracking (FLOPs, memory, latency, energy)
- Quantization simulation (FP32/FP16/INT8/Binary)
- Data utilities, serialization, visualizations
- Unit tests + runnable examples

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

## Quick start
```python
import numpy as np
from src.models.sequential import Sequential
from src.layers.dense import Dense
from src.activations.relu import ReLU
from src.losses.cross_entropy import CrossEntropyLoss
from src.optimizers.adam import Adam

model = Sequential([Dense(16, 32), ReLU(), Dense(32, 4)])
x = np.random.randn(32, 16).astype(np.float32)
y = np.random.randint(0, 4, size=(32,))
logits = model.forward(x)
loss_fn = CrossEntropyLoss()
loss, grad = loss_fn.forward(logits, y)
model.backward(grad)
Adam(model.parameters(), lr=1e-3).step()
```

## Hardware profiling
Use `HardwareProfiler` in `src/hardware/profiler.py` with predefined targets (`CortexM4`, `EdgeTPU`, `GenericGPU`) to estimate:
- operation count
- bytes moved
- latency
- energy

## Citation
If you use this project in academic work, please cite this repository.


## Phase 2 Advanced Research Features
- Cycle-accurate simulation (`src/hardware/cycle_accurate.py`) with CPU + systolic array + memory controller.
- Technology-node-aware energy models (`src/hardware/energy_model.py`).
- Compression stack (`src/compression`) with pruning and sparsity analytics.
- NAS stack (`src/nas`) with random, evolutionary, and surrogate search.
- Distillation stack (`src/distillation/kd.py`) for teacher-student training.
- Advanced layers: pooling, embedding, self-attention, transformer block.
- New losses (focal, huber, KL divergence) and optimizers (AdamW, Nadam, AdaBound).
- Dataset utilities, augmentations, samplers, benchmark helpers, and hardware plotting.


## Research Highlights
- Hardware-aware design metrics are first-class (FLOPs, bytes, latency, energy).
- Cycle-accurate simulation path supports CPU + systolic + memory co-analysis.
- Compression toolkit includes pruning/sparsity with speedup estimation.
- NAS and distillation workflows target accuracy-efficiency trade-offs.
- All simulator assumptions are documented and intended to be extensible.

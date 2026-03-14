# neural-network-from-scratch

![CI](https://img.shields.io/badge/CI-passing-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

`neural-network-from-scratch` is a research-oriented deep learning framework built on NumPy with explicit hardware-aware modeling. It is designed for experimentation with autograd internals, modern layers/losses/optimizers, and efficiency-driven workflows including quantization, pruning, NAS, distillation, and cycle-accurate accelerator simulation.

## Research Motivation

Most educational from-scratch frameworks stop at software-only metrics. This project treats **accuracy, latency, energy, throughput, and utilization** as first-class optimization targets so experiments can reflect realistic deployment constraints.

## Key Features

- Tensor + autograd engine with backward graph traversal
- Layer stack: Dense, Conv2D, RNN/LSTM, normalization/regularization, transformer primitives
- Full optimizer/loss suite including AdamW, Nadam, AdaBound, focal/huber/KL losses
- Hardware profiler (FLOPs, memory traffic, latency, energy)
- Cycle-accurate simulation (CPU + systolic array + memory controller)
- Compression: magnitude + structured pruning and sparsity utilities
- Quantization: symmetric/asymmetric simulation and error analysis
- NAS: random, evolutionary, Bayesian search
- Distillation workflow and benchmark/research study utilities

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

> Offline environments: if dependency resolution is blocked, install with `pip install --no-build-isolation -e .` after pre-installing `setuptools` and `wheel`.

## Quick Start

```python
import numpy as np
from src.models.sequential import Sequential
from src.layers.dense import Dense
from src.activations.relu import ReLU
from src.losses.cross_entropy import CrossEntropyLoss
from src.optimizers.adam import Adam

np.random.seed(7)
model = Sequential([Dense(16, 32), ReLU(), Dense(32, 4)])
x = np.random.randn(32, 16).astype(np.float32)
y = np.random.randint(0, 4, size=(32,))

logits = model.forward(x)
loss_fn = CrossEntropyLoss()
loss, grad = loss_fn.forward(logits, y)
model.backward(grad)
Adam(model.parameters(), lr=1e-3).step()
print(loss)
```

## Repository Structure

- `src/`: framework implementation (tensor, layers, losses, optimizers, hardware, compression, NAS)
- `neurospec/`: experiment configuration, training, and research pipeline
- `examples/`: runnable demos for key capabilities
- `tests/`: unit/integration tests
- `docs/`: documentation sources and paper
- `scripts/`: helper scripts for studies and generated artifacts

## Documentation & Citation

- API docs (Sphinx): `docs/source/`
- Research paper: `docs/paper.pdf`
- Citation metadata: `CITATION.cff`

## Research Metrics and Hardware Objectives

Run:

```bash
python scripts/run_research_suite.py
```

This writes `artifacts/research_suite.json` and `artifacts/reproducibility.json` with objective-based rankings and reproducibility metadata.

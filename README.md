# NeuroSpec: Hardware-Aware Neural Network From Scratch

NeuroSpec is a research-focused project implementing a neural network from scratch (NumPy only) and coupling it with a hardware estimator to evaluate AI accelerator characteristics.

## Key features
- Fully manual forward/backward implementation for dense neural networks.
- Synthetic hardware-aware dataset generation.
- Hardware estimation of throughput, latency, energy, and roofline utilization.
- Multi-objective research metrics combining model quality and hardware efficiency.
- CLI for reproducible experiments.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
neurospec-train --epochs 10 --batch-size 128 --precision-bits 8 --output artifacts
```

The command writes `artifacts/result.json`.

## Research objective
The benchmark objective combines:
- validation accuracy,
- validation loss,
- hardware efficiency,
- performance-per-watt,
- normalized energy-delay product.

This provides a compact proxy for hardware-model co-design quality.

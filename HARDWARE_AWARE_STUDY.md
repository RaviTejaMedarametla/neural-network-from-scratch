# Hardware-Aware Study Guide

This guide links repository experiments to edge/embedded AI concerns.

## 1) Precision trade-offs
Run:
```bash
python "Neural Network from Scratch/task/statistical_analysis.py" --repeats 5
```
Inspect:
- `benchmarks/statistical/accuracy_vs_latency.png`
- `benchmarks/statistical/accuracy_vs_memory.png`
- `benchmarks/statistical/accuracy_vs_energy.png`
- `benchmarks/statistical/pareto_frontier.png`

## 2) Memory and batch constraints
Run:
```bash
python "Neural Network from Scratch/task/hardware_stress_test.py"
```
Inspect:
- `experiments/scaling/hardware_stress.csv`

This covers low-memory limits, precision scaling, and batch-size constraints.

## 3) CPU-only scenario
Default scripts are CPU-oriented; no GPU is required.
Use:
```bash
python "Neural Network from Scratch/task/inference.py" --weights experiments/checkpoints/<ckpt>.npz --precision float32
```

## 4) Embedded-style constraints
Use `simulate_hardware.py` and `hardware_stress_test.py` to mimic:
- reduced memory budgets,
- reduced precision,
- compute slowdown.

## 5) Deployment relevance
- `task/deployment.py` exposes inference latency/throughput measurement.
- Optional ONNX export is included for interoperability when torch is available.

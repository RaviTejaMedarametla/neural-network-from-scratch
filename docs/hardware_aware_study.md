# Hardware-Aware Study Guide

This guide describes a reproducible process for analyzing latency, memory, and precision behavior using repository tooling.

## Design intent

The current model and scripts are intended for controlled CPU-bound experiments:
- identify where memory usage scales with architecture size,
- measure precision-mode effects on latency and estimated energy,
- capture failure boundaries under constrained-memory scenarios.

## 1) Operator and layer profiling
Run:
```bash
python "Neural Network from Scratch/task/profiler.py" --config "Neural Network from Scratch/task/config.py"
```
Output:
- `profiling/profile_neuralnetwork.json`

Use this artifact to inspect per-layer parameter count and activation-memory footprint. This is the primary input for layer-wise memory breakdown.

## 2) Baseline benchmark sweep and statistical repeats
Run:
```bash
python "Neural Network from Scratch/task/benchmark.py" --seed 42
python "Neural Network from Scratch/task/statistical_analysis.py" --repeats 5 --seed 42
```
Inspect:
- `benchmarks/benchmark_results.csv`
- `benchmarks/statistical/summary_stats.csv`
- `benchmarks/statistical/accuracy_vs_latency.png`
- `benchmarks/statistical/accuracy_vs_memory.png`
- `benchmarks/statistical/accuracy_vs_energy.png`
- `benchmarks/statistical/pareto_frontier.png`

## 3) Hardware tables (latency, memory, bandwidth proxy)
Run:
```bash
python "Neural Network from Scratch/task/hardware_analysis_report.py" \
  --benchmark-csv benchmarks/benchmark_results.csv \
  --profile-json profiling/profile_neuralnetwork.json \
  --output-dir hardware_results
```
Inspect:
- `hardware_results/layer_memory_breakdown.csv`
- `hardware_results/precision_tradeoff_table.csv`

`precision_tradeoff_table.csv` includes an effective-bandwidth proxy (`throughput * peak_memory`) to compare memory pressure across precision modes.

## 4) Constrained scenarios and bottleneck checks
Run:
```bash
python "Neural Network from Scratch/task/simulate_hardware.py"
python "Neural Network from Scratch/task/hardware_stress_test.py"
```
Inspect:
- `hardware_results/`
- `experiments/scaling/hardware_stress.csv`

These runs highlight where memory budgets, precision scaling, and artificial compute slowdowns degrade throughput or force configuration changes.

## Precision and quantization notes
- `float16` and `int8` behavior in this repository are simulation-based paths.
- Reported improvements are directional indicators; native kernel-level quantization can differ materially.

## Assumptions
- CPU-only execution path is used unless optional dependencies are configured.
- Benchmark runs use fixed seeds and stable host load for comparison quality.
- Profiling JSON is generated from the same architecture used in benchmarks.

## Limitations
- No hardware-counter sampling (cache misses, branch misses, DRAM bandwidth) is included.
- Effective-bandwidth values are coarse estimates and should not be interpreted as direct bus measurements.
- Single-node execution omits cross-device communication and scheduler effects.

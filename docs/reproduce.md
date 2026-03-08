# Reproduce End-to-End Results

This procedure runs the same pipeline used by local validation and CI-oriented checks.

## 1) Validate environment
```bash
pip install -r requirements-dev.txt
python scripts/verify_environment.py
```

## 2) Optional dataset retrieval
```bash
python scripts/download_fashion_mnist.py --out-dir "neural_network_from_scratch/Data"
```

## 3) Deterministic baseline training
```bash
python "neural_network_from_scratch/train.py" --experiment baseline
```

## 3a) Record run manifest (recommended)
```bash
python scripts/write_run_manifest.py --experiment baseline --seed 42
```

## 4) Real dataset training (requires valid Fashion-MNIST CSV)
```bash
python "neural_network_from_scratch/train.py" --experiment real_fashion_mnist
```

## 5) Benchmark and repeated statistical evaluation
```bash
python "neural_network_from_scratch/benchmark.py"
python "neural_network_from_scratch/statistical_analysis.py" --repeats 5
python "neural_network_from_scratch/benchmark_report.py" --input benchmarks/benchmark_results.csv --output benchmarks/benchmark_summary.csv
```

## 6) Profiling, hardware scenarios, and scaling
```bash
python "neural_network_from_scratch/profiler.py" --config "neural_network_from_scratch/config.py"
python "neural_network_from_scratch/simulate_hardware.py"
python "neural_network_from_scratch/hardware_stress_test.py"
python "neural_network_from_scratch/scaling_study.py" --quick
```

## 7) Framework comparison and deployment checks
```bash
python "neural_network_from_scratch/compare.py"
python "neural_network_from_scratch/inference.py" --weights experiments/checkpoints/<ckpt>.npz --precision float32
```

## 8) Artifacts to verify
- `experiments/logs/`
- `experiments/checkpoints/`
- `benchmarks/benchmark_results.csv`
- `benchmarks/comparison/`
- `benchmarks/statistical/`
- `experiments/scaling/`
- `hardware_results/`
- `profiling/`

## Assumptions
- Python dependencies are installed from the provided requirement files.
- The host allows file writes in repository-relative output directories.
- When using real-data mode, Fashion-MNIST CSV files satisfy schema checks.

## Limitations
- Runtime can vary due to CPU scheduling and background load.
- Optional torch/onnx paths are skipped if unavailable.
- Synthetic-data benchmarks should be treated as controlled comparisons, not production latency guarantees.

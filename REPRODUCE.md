# Reproduce End-to-End Results

## 1) Environment
```bash
pip install -r requirements-dev.txt
python scripts/verify_environment.py
```

## 2) Real dataset preparation (online + offline options)
```bash
python scripts/download_fashion_mnist.py --out-dir "Neural Network from Scratch/task/Data"
```
Offline fallback:
```bash
python scripts/prepare_offline_dataset.py
```
Alternative offline mirror:
```bash
export FASHION_MNIST_LOCAL_DIR=/path/to/local/csv_folder
python "Neural Network from Scratch/task/train.py" --experiment real_fashion_mnist
```

## 3) Deterministic baseline run (fully reproducible)
```bash
python "Neural Network from Scratch/task/train.py" --experiment baseline
```

## 4) Real dataset run (requires valid Fashion-MNIST CSV)
```bash
python "Neural Network from Scratch/task/train.py" --experiment real_fashion_mnist
```

## 5) Benchmark and statistical evaluation
```bash
python "Neural Network from Scratch/task/benchmark.py"
python "Neural Network from Scratch/task/statistical_analysis.py" --repeats 5
```

## 6) Profiling, hardware scenarios, scaling
```bash
python "Neural Network from Scratch/task/profiler.py" --config "Neural Network from Scratch/task/config.py"
python "Neural Network from Scratch/task/simulate_hardware.py"
python "Neural Network from Scratch/task/hardware_stress_test.py"
python "Neural Network from Scratch/task/scaling_study.py" --quick
```

## 7) Framework comparison and deployment checks
```bash
python "Neural Network from Scratch/task/compare.py"
python "Neural Network from Scratch/task/inference.py" --weights experiments/checkpoints/<ckpt>.npz --precision float32
python "Neural Network from Scratch/task/inference.py" --weights experiments/checkpoints/<ckpt>.npz --export-onnx
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

## Notes
- ONNX export requires torch + onnx + onnxruntime and fails with explicit guidance when missing.
- Dataset integrity failures are explicit by design (no silent fallback unless synthetic mode is enabled).

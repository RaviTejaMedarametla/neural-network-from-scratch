# Reproduce Pipeline Results

Use these commands to run a deterministic analytics pipeline cycle end to end.

## 1) Environment bootstrap
```bash
pip install -r requirements-dev.txt
python scripts/verify_environment.py
```

## 2) Optional dataset download
```bash
python scripts/download_fashion_mnist.py --out-dir "Neural Network from Scratch/task/Data"
```

## 3) Record run manifest
```bash
python scripts/write_run_manifest.py --experiment baseline --seed 42
```

## 4) Train baseline model
```bash
python "Neural Network from Scratch/task/train.py" --experiment baseline
```

## 5) Execute benchmark and statistical passes
```bash
python "Neural Network from Scratch/task/benchmark.py" --seed 42
python "Neural Network from Scratch/task/statistical_analysis.py" --repeats 5 --seed 42
python "Neural Network from Scratch/task/benchmark_report.py" --input benchmarks/benchmark_results.csv --output benchmarks/benchmark_summary.csv
```

## 6) Run profiling and hardware analysis
```bash
python "Neural Network from Scratch/task/profiler.py" --config "Neural Network from Scratch/task/config.py"
python "Neural Network from Scratch/task/hardware_analysis_report.py" --benchmark-csv benchmarks/benchmark_results.csv --profile-json profiling/profile_neuralnetwork.json --output-dir hardware_results
```

## 7) Validate deployment compatibility
```bash
python "Neural Network from Scratch/task/inference.py" --weights experiments/checkpoints/<ckpt>.npz --precision float32
python "Neural Network from Scratch/task/compare.py"
```

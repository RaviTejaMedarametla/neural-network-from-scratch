import csv
import argparse
import threading
import time
import tracemalloc
from pathlib import Path

import numpy as np
import psutil

from neural_network_from_scratch.config import PrecisionConfig
from neural_network_from_scratch.student import NeuralNetwork
from neural_network_from_scratch.reproducibility import set_global_seed
from neural_network_from_scratch.energy_estimation import estimate_runtime_energy_j


def _repo_root():
    return Path(__file__).resolve().parents[2]


def _maybe_profile_model(model, precision_config, batch_size):
    if not getattr(precision_config, "enable_profiling", False):
        return None

    from neural_network_from_scratch.profiler import profile_model

    report, output_file = profile_model(model=model, batch_size=batch_size, output_dir="profiling")
    return {"report": report, "output_file": str(output_file)}


def make_synthetic_data(n_samples, n_features, n_classes, seed=42):
    set_global_seed(seed)
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n_samples, n_features)).astype(np.float32)
    y = rng.integers(0, n_classes, size=n_samples, dtype=np.int32)
    return X, y


def _measure_peak_memory_mb(callable_fn, *args, **kwargs):
    tracemalloc.start()
    try:
        result = callable_fn(*args, **kwargs)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return result, peak / (1024 * 1024)


def _measure_cpu_percent(callable_fn, *args, sample_interval=0.05, **kwargs):
    process = psutil.Process()
    samples = []
    stop_flag = {"stop": False}

    def sampler():
        process.cpu_percent(interval=None)
        while not stop_flag["stop"]:
            samples.append(process.cpu_percent(interval=sample_interval))

    worker = threading.Thread(target=sampler, daemon=True)
    worker.start()
    try:
        result = callable_fn(*args, **kwargs)
    finally:
        stop_flag["stop"] = True
        worker.join()

    cpu_avg = float(np.mean(samples)) if samples else 0.0
    return result, cpu_avg


def measure_training_time_per_epoch(model, X, y, epochs=3, alpha=0.1, batch_size=32, seed=42):
    t0 = time.perf_counter()
    history = model.fit(X, y, epochs=epochs, alpha=alpha, batch_size=batch_size, shuffle=True, seed=seed)
    elapsed = time.perf_counter() - t0
    return history, elapsed / epochs


def measure_inference_latency_per_sample(model, X, precision="float32", runs=5):
    model.forward(X, training=False, precision=precision)
    timings = []
    for _ in range(runs):
        t0 = time.perf_counter()
        model.forward(X, training=False, precision=precision)
        timings.append(time.perf_counter() - t0)
    return float(np.mean(timings)) / X.shape[0]


def measure_batch_throughput(model, X, precision="float32", runs=5):
    model.forward(X, training=False, precision=precision)
    timings = []
    for _ in range(runs):
        t0 = time.perf_counter()
        model.forward(X, training=False, precision=precision)
        timings.append(time.perf_counter() - t0)
    avg_time = float(np.mean(timings))
    return X.shape[0] / avg_time if avg_time > 0 else float("inf")


def benchmark_one_setup(layer_sizes, activations, precision_mode, batch_size, n_samples=512, epochs=2, seed=42, enable_profiling=False):
    set_global_seed(seed)
    n_features = layer_sizes[0]
    n_classes = layer_sizes[-1]
    X, y = make_synthetic_data(n_samples=n_samples, n_features=n_features, n_classes=n_classes, seed=seed)

    cfg = PrecisionConfig(train_dtype="float32", infer_precision=precision_mode, seed=seed, enable_profiling=enable_profiling)
    model = NeuralNetwork(layer_sizes=layer_sizes, activations=activations, precision_config=cfg)
    profiling_payload = _maybe_profile_model(model, cfg, batch_size)

    def train_call():
        return measure_training_time_per_epoch(model, X, y, epochs=epochs, batch_size=batch_size, seed=seed)

    (history, time_per_epoch), peak_memory_mb = _measure_peak_memory_mb(train_call)
    (_, cpu_percent) = _measure_cpu_percent(lambda: model.fit(X, y, epochs=1, alpha=0.1, batch_size=batch_size, seed=seed))

    latency = measure_inference_latency_per_sample(model, X, precision=precision_mode)
    throughput = measure_batch_throughput(model, X, precision=precision_mode)
    energy_per_epoch = estimate_runtime_energy_j(time_per_epoch, precision_mode=precision_mode)

    result = {
        "seed": seed,
        "layer_sizes": "x".join(str(s) for s in layer_sizes),
        "precision_mode": precision_mode,
        "batch_size": batch_size,
        "epochs": epochs,
        "n_samples": n_samples,
        "train_time_per_epoch_s": round(time_per_epoch, 6),
        "inference_latency_per_sample_s": round(latency, 8),
        "batch_throughput_samples_per_s": round(throughput, 3),
        "peak_memory_mb": round(peak_memory_mb, 3),
        "cpu_utilization_percent": round(cpu_percent, 3),
        "final_train_accuracy": round(float(history["accuracy"][-1]), 6),
        "energy_per_epoch_j": round(energy_per_epoch, 6),
    }

    if profiling_payload is not None:
        result["profiling_report"] = profiling_payload["output_file"]

    return result


def run_benchmarks(
    batch_sizes,
    precision_modes,
    model_sizes,
    activations=None,
    output_csv="benchmark_results.csv",
    n_samples=512,
    epochs=2,
    seed=42,
    enable_profiling=False,
):
    activations = ["relu", "softmax"] if activations is None else activations
    set_global_seed(seed)

    results = []
    for layer_sizes in model_sizes:
        for batch_size in batch_sizes:
            for precision_mode in precision_modes:
                result = benchmark_one_setup(
                    layer_sizes=layer_sizes,
                    activations=activations,
                    precision_mode=precision_mode,
                    batch_size=batch_size,
                    n_samples=n_samples,
                    epochs=epochs,
                    seed=seed,
                    enable_profiling=enable_profiling,
                )
                results.append(result)

    benchmark_dir = _repo_root() / "benchmarks"
    benchmark_dir.mkdir(parents=True, exist_ok=True)
    output_path = benchmark_dir / output_csv

    fieldnames = list(results[0].keys()) if results else []
    with output_path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    return output_path, results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run benchmark sweep for predefined model/precision settings")
    parser.add_argument("--seed", type=int, default=42, help="Global seed for reproducible benchmark generation")
    parser.add_argument("--output-csv", default="benchmark_results.csv", help="Output CSV filename under benchmarks/")
    args = parser.parse_args()

    path, rows = run_benchmarks(
        batch_sizes=[16, 32],
        precision_modes=["float32", "float16", "int8"],
        model_sizes=[[16, 32, 4], [16, 64, 4]],
        n_samples=256,
        epochs=1,
        seed=args.seed,
        output_csv=args.output_csv,
    )
    print(f"Saved {len(rows)} benchmark rows to {path}")

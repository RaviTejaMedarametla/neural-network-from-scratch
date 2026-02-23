# Reproducibility Checklist

Use this checklist before publishing numbers or sharing artifacts.

## Environment
- [ ] Python version is recorded (`python --version`).
- [ ] Dependency set is pinned from `requirements.txt` and `requirements-dev.txt`.
- [ ] `python scripts/verify_environment.py` passes.
- [ ] CPU model, memory size, and OS are recorded.

## Dataset integrity
- [ ] Dataset source and version are recorded.
- [ ] SHA256 hash is computed and archived.
- [ ] Shape checks pass (`features == 784`, minimum row count).
- [ ] Label range checks pass (`0..9` for Fashion-MNIST).

## Determinism controls
- [ ] Global random seed is fixed.
- [ ] Experiment configuration is stored as JSON or tracked config name.
- [ ] Precision mode is explicit (`float32`, `float16`, `int8` simulation).

## Experiment execution
- [ ] Training logs are saved in `experiments/logs/`.
- [ ] Model checkpoints are saved in `experiments/checkpoints/`.
- [ ] Benchmark outputs are archived under `benchmarks/`.
- [ ] Hardware-stress outputs are archived under `experiments/scaling/`.

## Reporting quality
- [ ] Mean and confidence intervals are reported for repeated runs.
- [ ] Latency-memory-accuracy trade-off plots are regenerated.
- [ ] Any skipped optional dependency path is clearly marked.

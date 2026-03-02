# Reproducibility Checklist

Use this checklist before sharing benchmark numbers or derived artifacts.

## Environment capture
- [ ] Python version is recorded (`python --version`).
- [ ] Dependencies come from `requirements.txt` and `requirements-dev.txt`.
- [ ] `python scripts/verify_environment.py` passes.
- [ ] CPU model, memory size, and OS details are recorded.

## Dataset controls
- [ ] Dataset source and version are recorded.
- [ ] SHA256 hash is archived where applicable.
- [ ] Shape checks pass (`features == 784`, minimum row count).
- [ ] Label range checks pass (`0..9` for Fashion-MNIST).

## Determinism controls
- [ ] Global random seed is fixed.
- [ ] Experiment configuration is captured (name or JSON payload).
- [ ] Precision mode is explicit (`float32`, `float16`, `int8` simulation).
- [ ] Statistical repeat count is fixed and logged.

## Execution artifacts
- [ ] Training logs are saved in `experiments/logs/`.
- [ ] Model checkpoints are saved in `experiments/checkpoints/`.
- [ ] Benchmark outputs are saved in `benchmarks/`.
- [ ] Hardware and scaling outputs are saved in `experiments/scaling/`.
- [ ] Profiling reports are saved in `profiling/`.

## Reporting quality
- [ ] Means and confidence intervals are reported for repeated runs.
- [ ] Hardware assumptions are documented alongside results.
- [ ] Skipped optional dependency paths are explicitly marked.
- [ ] Any failed run includes a root-cause note and rerun status.

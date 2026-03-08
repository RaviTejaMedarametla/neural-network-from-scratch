# Hardware-Aware Neural Network Pipeline from Scratch

A reproducible, NumPy-based machine learning system for training and evaluating compact neural networks under practical hardware constraints.

## Overview
This repository implements an end-to-end workflow for supervised image classification using a feed-forward neural network developed from first principles. The system emphasizes deterministic execution, structured experiment management, and quantitative evaluation across performance dimensions such as latency, memory usage, and numerical behavior.

The project addresses a common systems challenge in machine learning: model quality alone is insufficient when deployment targets operate under constrained compute or memory budgets. By combining training, benchmarking, profiling, and hardware-constraint simulation in a single workflow, the repository supports technically grounded, reproducible experimentation suitable for research-oriented engineering.

## Project Motivation
Modern ML applications increasingly require models that are not only accurate but also efficient and predictable in resource-constrained settings. This project is motivated by three practical research needs: (1) evaluating model behavior under explicit hardware limits, (2) reducing ambiguity in experimental outcomes through deterministic setup and repeatable workflows, and (3) creating a transparent baseline implementation that can be extended for systems-level optimization studies.

## System Architecture
The repository is organized as a modular pipeline with five core components:

- **Data Pipeline**  
  Handles dataset retrieval, validation, and preprocessing inputs for training and evaluation workflows.

- **Model Training**  
  Implements training loops, checkpointing, and configurable experiment execution for a compact feed-forward network.

- **Model Compression / Constraint Simulation**  
  Includes tools for studying numerical precision and hardware-related constraints that influence deployability.

- **Hardware-Aware Evaluation**  
  Provides benchmarking and profiling paths to measure runtime behavior, memory footprint, and stability across repeated runs.

- **Inference and Artifacts**  
  Produces outputs, manifests, and reports to support experiment tracking and downstream analysis.

## Repository Structure
- `neural_network_from_scratch/`  
  Core implementation: model components, training logic, inference utilities, profiling, and evaluation modules.

- `scripts/`  
  Command-line utilities for environment validation, dataset acquisition, workflow execution, and run-manifest generation.

- `docs/`  
  Reproducibility guides, experiment documentation, and hardware-aware study references.

- `experiments/`  
  Experiment manifests, scaling runs, and organized run outputs.

- `benchmarks/`  
  Benchmark comparison outputs and statistical summaries.

- `artifacts/`  
  Generated deliverables and report-oriented outputs.

- `utils/`  
  Supporting utilities used by pipeline components.

## Features
- Deterministic training and evaluation workflows with explicit run controls.
- Hardware-aware benchmarking for latency, memory, and precision-oriented analysis.
- Scripted experiment orchestration for reproducible execution.
- Structured experiment artifacts and manifest generation for traceability.
- Optional interoperability checks aligned with export and framework-comparison workflows.

## Installation
Install runtime and development dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Validate the local environment:

```bash
python scripts/verify_environment.py
```

## Usage
Download Fashion-MNIST data (if not already available):

```bash
python scripts/download_fashion_mnist.py --out-dir "neural_network_from_scratch/Data"
```

Run the complete workflow:

```bash
python scripts/run_workflow.py --mode full --experiment baseline --stats-repeats 5
```

Run selected phases:

```bash
python scripts/run_workflow.py --mode train --experiment real_fashion_mnist
python scripts/run_workflow.py --mode benchmark --stats-repeats 7
```

## Reproducibility
This repository is designed for repeatable experimentation through:

- **Configuration-driven execution** via workflow arguments and run manifests.
- **Deterministic controls** through explicit seeds and pinned dependencies.
- **Experiment artifacts** stored in dedicated directories for auditability and reruns.

For detailed reproducibility guidance, see:
- `docs/reproduce.md`
- `docs/reproducibility_checklist.md`
- `docs/experiment_tracking_template.md`
- `docs/hardware_aware_study.md`

## Related Projects
This repository is part of a broader portfolio focused on hardware-aware machine learning, edge AI optimization, deterministic ML pipelines, and production-oriented ML systems.

Related repositories:
- `neural-network-from-scratch`
- `classification-of-handwritten-digits1`
- `edge-ai-hardware-optimization`
- `data-analysis-for-hospitals`
- `nba-data-preprocessing`
- `Data-Science-AI-Portfolio`

## Future Work
Potential extensions include:

- Deployment-focused validation on embedded or edge hardware targets.
- Additional compression and quantization strategies for resource-limited inference.
- Expanded benchmarking frameworks with broader workload and platform coverage.

## License
This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

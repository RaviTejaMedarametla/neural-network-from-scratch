# Experiment Tracking Template

Use this template for experiment notes, issue reports, and result handoff.

## Metadata
- Experiment ID:
- Date/time (UTC):
- Commit SHA:
- System profile (CPU / RAM / OS):
- Runtime constraints (single process, background load notes):

## Configuration
- Dataset and version:
- Dataset SHA256 (if applicable):
- Model architecture (layer sizes, activations):
- Precision mode:
- Hyperparameters (`epochs`, `alpha`, `batch_size`, `seed`):

## Results
- Final training loss:
- Final validation loss:
- Final validation accuracy:
- Training time per epoch (s):
- Inference latency (ms/sample):
- Throughput (samples/s):
- Peak memory (MB):
- Estimated energy per epoch (J or relative units):

## Hardware analysis
- Layer-wise parameter/memory table path:
- Precision trade-off table path:
- Dominant bottleneck observed (compute, memory, or I/O):
- Failure mode observed (if any):

## Artifacts
- Manifest file:
- Log file:
- Checkpoint path:
- Benchmark CSV:
- Statistical summary:
- Plots:

## Assumptions and limitations
- Assumptions during run:
- Limitations affecting interpretation:
- Follow-up validation required:

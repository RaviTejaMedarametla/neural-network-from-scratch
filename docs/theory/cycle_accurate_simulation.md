# Cycle-Accurate Simulation

Cycle models account for:
- compute cycles on CPU / accelerator
- memory transfer stalls
- utilization penalties

A simplified latency estimator:

\[
\text{Latency} = \frac{C_{cpu} + C_{acc}}{f} + \sum_i \frac{B_i}{BW}
\]

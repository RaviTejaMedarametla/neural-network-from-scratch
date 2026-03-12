# Hardware Objective Modeling

## Multi-objective formulation
We optimize a scalarized objective:

\[
J = w_a A + w_l rac{1}{1+L} + w_e rac{1}{1+E} + w_t\left(1-e^{-T/	au}ight) + w_u U
\]

Where:
- \(A\): accuracy
- \(L\): latency in ms
- \(E\): energy in mJ
- \(T\): throughput samples/sec
- \(U\): utilization

## Constraint handling
Given target constraints \(C\), we report per-axis nonnegative violations:

\[
v_i = \max(0, m_i - c_i) \quad 	ext{or} \quad v_i = \max(0, c_i - m_i)
\]

depending on whether the metric is upper- or lower-bounded.

## Why this matters
Scalarized and constraint-aware objectives allow direct comparison of model variants under hardware budgets and are practical for NAS and compression studies.

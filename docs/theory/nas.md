# Hardware-Constrained NAS

Objective combines accuracy and system costs:

\[
\max_{a \in \mathcal{A}} \; \text{Acc}(a) - \lambda_1 \cdot \text{Latency}(a) - \lambda_2 \cdot \text{Energy}(a)
\]

where architecture `a` is sampled from a search space of operations.

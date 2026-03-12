# Pruning and Sparsity Theory

Magnitude pruning removes parameters with small absolute value:

\[
W' = W \odot \mathbb{1}(|W| > \tau)
\]

This improves memory and can improve latency if hardware exploits sparse kernels.

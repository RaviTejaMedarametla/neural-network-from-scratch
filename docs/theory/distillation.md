# Knowledge Distillation

Student learns from hard labels and teacher soft logits:

\[
\mathcal{L} = \alpha \mathcal{L}_{CE}(y, s) + (1-\alpha)T^2 \mathcal{L}_{KL}(\sigma(t/T), \sigma(s/T))
\]

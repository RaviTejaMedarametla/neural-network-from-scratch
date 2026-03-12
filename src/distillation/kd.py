from __future__ import annotations

import numpy as np

from src.losses.cross_entropy import CrossEntropyLoss
from src.losses.kldiv import KLDivLoss


class Distiller:
    """Knowledge distillation trainer for teacher-student pairs."""

    def __init__(self, teacher, student, temperature: float = 3.0) -> None:
        self.teacher = teacher
        self.student = student
        self.temperature = temperature
        self.ce_loss = CrossEntropyLoss()
        self.kld = KLDivLoss()

    def _log_softmax(self, x: np.ndarray) -> np.ndarray:
        z = x - np.max(x, axis=1, keepdims=True)
        return z - np.log(np.sum(np.exp(z), axis=1, keepdims=True) + 1e-9)

    def train_step(self, inputs: np.ndarray, targets: np.ndarray, optimizer, alpha: float = 0.7) -> float:
        student_logits = self.student.forward(inputs)
        teacher_logits = self.teacher.forward(inputs)

        ce, grad_ce = self.ce_loss.forward(student_logits, targets)
        s_log = self._log_softmax(student_logits / self.temperature)
        t_log = self._log_softmax(teacher_logits / self.temperature)
        kd = self.kld.forward(s_log, t_log) * (self.temperature**2)

        # Gradient proxy: CE gradient dominates; KD gradient approximated with softened probs.
        grad_kd = (np.exp(s_log) - np.exp(t_log)) / student_logits.shape[0]
        grad = alpha * grad_ce + (1.0 - alpha) * grad_kd

        self.student.backward(grad)
        optimizer.step()
        optimizer.zero_grad()
        return float(alpha * ce + (1.0 - alpha) * kd)

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .config import ModelConfig, TrainingConfig
from .data import Dataset, iterate_minibatches
from .layers import MLPModel
from .math_ops import accuracy, cross_entropy_with_logits, stat_summary
from .optim import make_optimizer


@dataclass(slots=True)
class EpochMetrics:
    epoch: int
    train_loss: float
    train_acc: float
    val_loss: float
    val_acc: float
    grad_norm: float
    weight_norm: float
    activation_sparsity: float


@dataclass(slots=True)
class TrainResult:
    history: list[EpochMetrics]
    best_val_accuracy: float
    final_val_accuracy: float
    final_val_loss: float

    def to_dict(self) -> dict:
        return {
            "history": [asdict(h) for h in self.history],
            "best_val_accuracy": self.best_val_accuracy,
            "final_val_accuracy": self.final_val_accuracy,
            "final_val_loss": self.final_val_loss,
        }


class Trainer:
    def __init__(self, model_cfg: ModelConfig, train_cfg: TrainingConfig):
        self.model_cfg = model_cfg
        self.train_cfg = train_cfg
        self.rng = np.random.default_rng(train_cfg.seed)

        self.model = MLPModel(
            input_dim=model_cfg.input_dim,
            hidden_dims=model_cfg.hidden_dims,
            output_dim=model_cfg.output_dim,
            activation=model_cfg.activation,
            init=model_cfg.weight_init,
            dropout=model_cfg.dropout,
            layer_norm=model_cfg.layer_norm,
            seed=train_cfg.seed,
        )
        self.optimizer = make_optimizer(
            name=train_cfg.optimizer,
            params=self.model.parameters(),
            lr=train_cfg.learning_rate,
            weight_decay=train_cfg.weight_decay,
        )

    def _global_grad_norm(self) -> float:
        total = 0.0
        for p in self.model.parameters():
            total += float(np.sum(np.square(p.grad)))
        return float(np.sqrt(total))

    def _global_weight_norm(self) -> float:
        total = 0.0
        for p in self.model.parameters():
            total += float(np.sum(np.square(p.data)))
        return float(np.sqrt(total))

    def _clip_gradients(self) -> None:
        grad_norm = self._global_grad_norm()
        if grad_norm < self.train_cfg.grad_clip_norm:
            return
        scale = self.train_cfg.grad_clip_norm / (grad_norm + 1e-12)
        for p in self.model.parameters():
            p.grad *= scale

    def _evaluate(self, x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        logits = self.model.forward(x, training=False)
        loss, _ = cross_entropy_with_logits(logits, y, label_smoothing=0.0)
        acc = accuracy(logits, y)
        return loss, acc

    def train(self, data: Dataset) -> TrainResult:
        history: list[EpochMetrics] = []
        best_val = 0.0

        for epoch in range(1, self.train_cfg.epochs + 1):
            losses: list[float] = []
            accs: list[float] = []
            activation_sparsity: list[float] = []

            for xb, yb in iterate_minibatches(data.x_train, data.y_train, self.train_cfg.batch_size, self.rng):
                self.model.zero_grad()
                logits = self.model.forward(xb, training=True)
                loss, grad_logits = cross_entropy_with_logits(
                    logits,
                    yb,
                    label_smoothing=self.train_cfg.label_smoothing,
                )
                self.model.backward(grad_logits)
                self._clip_gradients()
                self.optimizer.step()

                losses.append(loss)
                accs.append(accuracy(logits, yb))
                activation_sparsity.append(stat_summary(logits).sparsity)

            val_loss, val_acc = self._evaluate(data.x_val, data.y_val)
            grad_norm = self._global_grad_norm()
            weight_norm = self._global_weight_norm()
            best_val = max(best_val, val_acc)

            history.append(
                EpochMetrics(
                    epoch=epoch,
                    train_loss=float(np.mean(losses)),
                    train_acc=float(np.mean(accs)),
                    val_loss=float(val_loss),
                    val_acc=float(val_acc),
                    grad_norm=float(grad_norm),
                    weight_norm=float(weight_norm),
                    activation_sparsity=float(np.mean(activation_sparsity)),
                )
            )

        return TrainResult(
            history=history,
            best_val_accuracy=float(best_val),
            final_val_accuracy=float(history[-1].val_acc),
            final_val_loss=float(history[-1].val_loss),
        )

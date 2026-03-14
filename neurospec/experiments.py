from __future__ import annotations

import json
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from .config import ExperimentConfig
from .data import SyntheticHardwareDataset
from .hardware import HardwareEstimator, hardware_efficiency_score
from .training import TrainResult, Trainer
from src.hardware import build_metric_bundle


@dataclass(slots=True)
class ResearchMetrics:
    validation_accuracy: float
    validation_loss: float
    hardware_efficiency: float
    performance_per_watt: float
    energy_delay_product: float
    objective_score: float


@dataclass(slots=True)
class ExperimentResult:
    config: dict
    train: dict
    hardware: dict
    research_metrics: dict

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)




def _safe_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def _pip_freeze() -> list[str]:
    try:
        out = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
        return [line for line in out.splitlines() if line]
    except Exception:
        return []

def _objective(metrics: ResearchMetrics) -> float:
    return (
        0.42 * metrics.validation_accuracy
        - 0.08 * metrics.validation_loss
        + 0.22 * metrics.hardware_efficiency
        + 0.18 * metrics.performance_per_watt
        - 0.10 * metrics.energy_delay_product
    )


def evaluate_research_metrics(train: TrainResult, hardware_report: dict, hw_eff: float) -> ResearchMetrics:
    throughput = hardware_report["estimated_throughput_samples_s"]
    power_w = hardware_report["estimated_power_w"]
    latency_ms = hardware_report["estimated_latency_ms"]
    energy_mj = hardware_report["estimated_energy_mj_per_batch"]

    perf_per_watt = throughput / max(power_w, 1e-9)
    perf_per_watt_norm = 1.0 - np.exp(-perf_per_watt / 20.0)

    edp = (latency_ms / 10.0) * (energy_mj / 2.0)
    edp_norm = min(3.0, edp) / 3.0

    base = ResearchMetrics(
        validation_accuracy=train.final_val_accuracy,
        validation_loss=train.final_val_loss,
        hardware_efficiency=hw_eff,
        performance_per_watt=float(perf_per_watt_norm),
        energy_delay_product=float(edp_norm),
        objective_score=0.0,
    )
    base.objective_score = float(_objective(base))
    return base


def run_research_experiment(config: ExperimentConfig, output_dir: str | Path = "artifacts") -> ExperimentResult:
    dataset = SyntheticHardwareDataset(
        input_dim=config.model.input_dim,
        classes=config.model.output_dim,
        seed=config.training.seed,
    ).build(
        train_samples=config.training.train_samples,
        val_samples=config.training.val_samples,
    )

    trainer = Trainer(config.model, config.training)
    train_result = trainer.train(dataset)

    estimator = HardwareEstimator(config.hardware)
    hw_report = estimator.estimate_network(config.model, config.training)
    hw_eff = hardware_efficiency_score(hw_report, config.hardware)

    research = evaluate_research_metrics(train_result, hw_report.to_dict(), hw_eff)

    objective_bundle = build_metric_bundle(
        accuracy=train_result.final_val_accuracy,
        latency_ms=hw_report.estimated_latency_ms,
        energy_mj=hw_report.estimated_energy_mj_per_batch,
        throughput_sps=hw_report.estimated_throughput_samples_s,
        utilization=float(np.mean([l.utilization for l in hw_report.layer_stats])),
        achieved_tops=hw_report.achieved_tops,
        peak_tops=max(hw_report.roofline_tops, 1e-9),
    )

    result = ExperimentResult(
        config=asdict(config),
        train=train_result.to_dict(),
        hardware=hw_report.to_dict(),
        research_metrics={**asdict(research), "hardware_objectives": asdict(objective_bundle)},
    )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "result.json").write_text(result.to_json())

    repro = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "seed": config.training.seed,
        "pythonhashseed": str(config.training.seed),
        "git_commit": _safe_git_commit(),
        "pip_freeze": _pip_freeze(),
    }
    (output_path / "reproducibility.json").write_text(json.dumps(repro, indent=2))

    return result

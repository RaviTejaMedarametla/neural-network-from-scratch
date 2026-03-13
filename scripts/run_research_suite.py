#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.benchmark import HardwareOptimizationStudy
from src.hardware import CycleAccurateHardwareModel, GenericGPU, HardwareProfiler, MemoryController, SimpleCPU, SystolicArray
from src.layers import Dense
from src.models.sequential import Sequential


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run hardware research suite")
    parser.add_argument("--use-cycle-model", action="store_true", help="Attach cycle-accurate hardware simulation")
    return parser.parse_args()


def _profile_reference_model(use_cycle_model: bool) -> dict:
    model = Sequential([Dense(16, 32), Dense(32, 8)])
    profiler = HardwareProfiler(GenericGPU)
    if use_cycle_model:
        profiler.set_cycle_model(CycleAccurateHardwareModel(SimpleCPU(), SystolicArray(), MemoryController()))
    return profiler.profile_model(model, (4, 16))


def main() -> None:
    args = _parse_args()
    np.random.seed(7)
    study = HardwareOptimizationStudy()

    candidates = [
        ("baseline_fp32", 0.84, 7.9, 2.8, 1800, 0.52, 7.1, 16.2),
        ("int8_quant", 0.82, 4.8, 1.1, 3400, 0.74, 8.7, 16.2),
        ("sparse_int8", 0.81, 3.9, 0.9, 3900, 0.78, 9.2, 16.2),
        ("distilled_sparse", 0.80, 3.1, 0.7, 4300, 0.81, 9.5, 16.2),
    ]

    results = [study.evaluate_candidate(*c) for c in candidates]
    ranked = study.rank(results)
    summary = study.summarize(ranked)

    payload = {
        "summary": summary,
        "ranked": [r.__dict__ for r in ranked],
        "reference_profile": _profile_reference_model(args.use_cycle_model),
        "cycle_model_enabled": bool(args.use_cycle_model),
    }

    outdir = Path("artifacts")
    outdir.mkdir(exist_ok=True)
    out = outdir / "research_suite.json"
    out.write_text(json.dumps(payload, indent=2))

    print(json.dumps(payload, indent=2))
    print(f"wrote: {out.resolve()}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.benchmark import HardwareOptimizationStudy


def main() -> None:
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
    }

    outdir = Path("artifacts")
    outdir.mkdir(exist_ok=True)
    out = outdir / "research_suite.json"
    out.write_text(json.dumps(payload, indent=2))

    print(json.dumps(payload, indent=2))
    print(f"wrote: {out.resolve()}")


if __name__ == "__main__":
    main()

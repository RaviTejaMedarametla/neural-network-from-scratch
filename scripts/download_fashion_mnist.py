"""Download Fashion-MNIST CSV files using repository dataset configuration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = REPO_ROOT / "Neural Network from Scratch" / "task"
sys.path.insert(0, str(TASK_DIR))

from dataset_config import FASHION_MNIST_SPEC, download_fashion_mnist  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Download Fashion-MNIST CSV files")
    parser.add_argument("--out-dir", default=None, help="Optional override output dir")
    args = parser.parse_args()

    if args.out_dir:
        from dataclasses import replace

        out = Path(args.out_dir)
        spec = replace(
            FASHION_MNIST_SPEC,
            train_path=str(out / "fashion-mnist_train.csv"),
            test_path=str(out / "fashion-mnist_test.csv"),
        )
    else:
        spec = FASHION_MNIST_SPEC

    hashes = download_fashion_mnist(spec)
    print(json.dumps({"dataset": spec.name, "version": spec.version, **hashes}, indent=2))


if __name__ == "__main__":
    main()

"""Prepare local offline Fashion-MNIST CSV files from bundled example data."""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_SRC = Path("examples/datasets")
DEFAULT_DST = Path("Neural Network from Scratch/task/Data")


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy bundled example dataset files for offline runs")
    parser.add_argument("--src", default=str(DEFAULT_SRC), help="Source directory containing example CSV files")
    parser.add_argument("--dst", default=str(DEFAULT_DST), help="Destination task Data directory")
    args = parser.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)

    train_src = src / "fashion-mnist_example_train.csv"
    test_src = src / "fashion-mnist_example_test.csv"
    if not train_src.exists() or not test_src.exists():
        raise FileNotFoundError(f"Missing expected example files in {src}")

    dst.mkdir(parents=True, exist_ok=True)
    train_dst = dst / "fashion-mnist_train.csv"
    test_dst = dst / "fashion-mnist_test.csv"
    train_dst.write_bytes(train_src.read_bytes())
    test_dst.write_bytes(test_src.read_bytes())

    print(f"Copied offline dataset to: {dst}")
    print(f"  - {train_dst}")
    print(f"  - {test_dst}")


if __name__ == "__main__":
    main()

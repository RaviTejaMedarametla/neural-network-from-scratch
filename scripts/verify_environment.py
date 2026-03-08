"""Environment verification for reproducible research runs."""

from __future__ import annotations

import importlib
import platform
import sys
from pathlib import Path

REQUIRED = ["numpy", "matplotlib", "psutil", "requests", "tqdm"]
OPTIONAL = ["torch", "pytest"]

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def check_module(name: str) -> str:
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, "__version__", "unknown")
        return f"OK ({version})"
    except Exception as exc:
        return f"MISSING ({exc})"


def dataset_status() -> str:
    try:
        from neural_network_from_scratch.dataset_config import FASHION_MNIST_SPEC

        train = Path(FASHION_MNIST_SPEC.train_path)
        test = Path(FASHION_MNIST_SPEC.test_path)
        return f"train_exists={train.exists()} size={train.stat().st_size if train.exists() else 0}, test_exists={test.exists()} size={test.stat().st_size if test.exists() else 0}"
    except Exception as exc:
        return f"unavailable ({exc})"


def main() -> None:
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    print("\nRequired packages:")
    for m in REQUIRED:
        print(f"  - {m}: {check_module(m)}")
    print("\nOptional packages:")
    for m in OPTIONAL:
        print(f"  - {m}: {check_module(m)}")
    print("\nDataset status:")
    print(f"  - fashion-mnist: {dataset_status()}")


if __name__ == "__main__":
    main()

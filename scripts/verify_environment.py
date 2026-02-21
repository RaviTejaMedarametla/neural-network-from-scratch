"""Environment verification for reproducible research runs."""
from __future__ import annotations
import importlib, platform, sys
from pathlib import Path
REQUIRED = ["numpy", "matplotlib", "psutil", "requests", "tqdm", "onnx", "onnxruntime"]
OPTIONAL = ["torch", "pytest"]
REPO_ROOT = Path(__file__).resolve().parents[1]; TASK_DIR = REPO_ROOT / "Neural Network from Scratch" / "task"; sys.path.insert(0, str(TASK_DIR))
def check_module(name: str) -> str:
    try: mod = importlib.import_module(name); return f"OK ({getattr(mod, '__version__', 'unknown')})"
    except ImportError as exc: return f"MISSING ({exc})"
def dataset_status() -> str:
    try:
        from dataset_config import FASHION_MNIST_SPEC
        train, test = Path(FASHION_MNIST_SPEC.train_path), Path(FASHION_MNIST_SPEC.test_path)
        return f"train_exists={train.exists()} size={train.stat().st_size if train.exists() else 0}, test_exists={test.exists()} size={test.stat().st_size if test.exists() else 0}"
    except (ImportError, FileNotFoundError, OSError, AttributeError) as exc: return f"unavailable ({exc})"
def main() -> None:
    print(f"Python: {sys.version.split()[0]}"); print(f"Platform: {platform.platform()}")
    print("\nRequired packages:"); [print(f"  - {m}: {check_module(m)}") for m in REQUIRED]
    print("\nOptional packages:"); [print(f"  - {m}: {check_module(m)}") for m in OPTIONAL]
    print("\nDataset status:"); print(f"  - fashion-mnist: {dataset_status()}")
if __name__ == "__main__": main()

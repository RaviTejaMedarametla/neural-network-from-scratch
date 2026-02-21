"""Dataset configuration, integrity checks, and preparation helpers."""
from __future__ import annotations
import hashlib, os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple
import numpy as np, requests

@dataclass(frozen=True)
class DatasetSpec:
    name: str; version: str; train_path: str; test_path: str; expected_features: int = 784; expected_min_rows: int = 100; download_base_url: str = "https://pjreddie.com/media/files"

FASHION_MNIST_SPEC = DatasetSpec(name="fashion-mnist", version="v1", train_path="Neural Network from Scratch/task/Data/fashion-mnist_train.csv", test_path="Neural Network from Scratch/task/Data/fashion-mnist_test.csv")

def manual_dataset_instructions(spec: DatasetSpec = FASHION_MNIST_SPEC) -> str:
    return ("Manual dataset setup required. Place CSV files at:\n"
            f"  - train: {spec.train_path}\n  - test:  {spec.test_path}\n"
            "Expected format: header + 785 columns (label + 784 pixels), label in [0,9].\n"
            "Offline option: set FASHION_MNIST_LOCAL_DIR to a folder containing\n"
            "fashion-mnist_train.csv and fashion-mnist_test.csv, then rerun training.")

def _sha256(path: Path) -> str:
    h=hashlib.sha256();
    with path.open("rb") as fp:
        for c in iter(lambda: fp.read(65536), b""): h.update(c)
    return h.hexdigest()

def file_digest(path: str | Path) -> str:
    p=Path(path)
    if not p.exists(): raise FileNotFoundError(f"Dataset file not found: {p}")
    return _sha256(p)

def validate_dataset_file(path: str | Path, expected_features: int, expected_min_rows: int, expected_sha256: Optional[str] = None) -> Tuple[int,int]:
    p=Path(path)
    if not p.exists(): raise FileNotFoundError(f"Dataset file not found: {p}")
    if p.stat().st_size==0: raise ValueError(f"Dataset file is empty: {p}")
    if expected_sha256 is not None:
        actual=_sha256(p)
        if actual.lower()!=expected_sha256.lower(): raise ValueError(f"Dataset hash mismatch for {p}. expected={expected_sha256}, actual={actual}")
    data=np.genfromtxt(str(p), delimiter=",", skip_header=1)
    if data.size==0: raise ValueError(f"Dataset file has no rows after header: {p}")
    data=np.atleast_2d(data); n_rows,n_cols=data.shape
    if n_cols!=expected_features+1: raise ValueError(f"Unexpected dataset shape for {p}: got {data.shape}, expected (*, {expected_features + 1})")
    if n_rows<expected_min_rows: raise ValueError(f"Too few rows in {p}: got {n_rows}, expected at least {expected_min_rows}")
    if np.isnan(data).any(): raise ValueError(f"NaN values detected in dataset: {p}")
    labels=data[:,0]
    if labels.min()<0 or labels.max()>9: raise ValueError(f"Label range out of expected [0,9] for {p}")
    return n_rows,n_cols

def load_dataset(path: str | Path) -> Tuple[np.ndarray,np.ndarray]:
    data=np.atleast_2d(np.genfromtxt(str(Path(path)), delimiter=",", skip_header=1)); y=data[:,0].astype(np.int32); X=data[:,1:].astype(np.float32); X/= (np.max(X) if np.max(X)>0 else 1.0); return X,y

def _download_file(url: str, target: Path) -> None:
    r=requests.get(url, timeout=120); r.raise_for_status(); target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(r.content)

def _copy_local_dataset(local_dir: Path, spec: DatasetSpec) -> None:
    train_src,test_src=local_dir/"fashion-mnist_train.csv",local_dir/"fashion-mnist_test.csv"
    if not train_src.exists() or not test_src.exists(): raise FileNotFoundError(f"Missing dataset files in {local_dir}. Required: fashion-mnist_train.csv and fashion-mnist_test.csv")
    train_dst,test_dst=Path(spec.train_path),Path(spec.test_path); train_dst.parent.mkdir(parents=True, exist_ok=True); test_dst.parent.mkdir(parents=True, exist_ok=True)
    train_dst.write_bytes(train_src.read_bytes()); test_dst.write_bytes(test_src.read_bytes())

def download_fashion_mnist(spec: DatasetSpec = FASHION_MNIST_SPEC) -> Dict[str,str]:
    local_dir=os.getenv("FASHION_MNIST_LOCAL_DIR")
    if local_dir:
        _copy_local_dataset(Path(local_dir), spec); return {"train_sha256": file_digest(spec.train_path), "test_sha256": file_digest(spec.test_path)}
    _download_file(f"{spec.download_base_url.rstrip('/')}/fashion-mnist_train.csv", Path(spec.train_path)); _download_file(f"{spec.download_base_url.rstrip('/')}/fashion-mnist_test.csv", Path(spec.test_path))
    return {"train_sha256": file_digest(spec.train_path), "test_sha256": file_digest(spec.test_path)}

def ensure_dataset_ready(spec: DatasetSpec, expected_features: int, expected_min_rows: int, auto_download: bool = False, expected_sha256: Optional[str] = None) -> Tuple[int,int]:
    try:
        return validate_dataset_file(spec.train_path, expected_features=expected_features, expected_min_rows=expected_min_rows, expected_sha256=expected_sha256)
    except (FileNotFoundError, ValueError) as exc:
        if not auto_download: raise RuntimeError(f"Dataset validation failed: {exc}\n{manual_dataset_instructions(spec)}") from exc
        try: download_fashion_mnist(spec)
        except (requests.RequestException, FileNotFoundError, OSError) as dl_exc:
            raise RuntimeError(f"Dataset preparation failed: {dl_exc}\n{manual_dataset_instructions(spec)}") from exc
        return validate_dataset_file(spec.train_path, expected_features=expected_features, expected_min_rows=expected_min_rows, expected_sha256=expected_sha256)

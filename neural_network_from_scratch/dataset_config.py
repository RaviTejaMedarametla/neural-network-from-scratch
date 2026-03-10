"""Dataset configuration, integrity checks, and preparation helpers."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

import numpy as np
import requests


@dataclass(frozen=True)
class DatasetSpec:
    """Static description of a dataset used by this repository."""

    name: str
    version: str
    train_path: str
    test_path: str
    expected_features: int = 784
    expected_min_rows: int = 100
    download_base_url: str = "https://pjreddie.com/media/files"


FASHION_MNIST_SPEC = DatasetSpec(
    name="fashion-mnist",
    version="v1",
    train_path="neural_network_from_scratch/Data/fashion-mnist_train.csv",
    test_path="neural_network_from_scratch/Data/fashion-mnist_test.csv",
)


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def file_digest(path: str | Path) -> str:
    """Return SHA256 digest for a file path."""

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset file not found: {p}")
    return _sha256(p)


def validate_dataset_file(
    path: str | Path,
    expected_features: int,
    expected_min_rows: int,
    expected_sha256: Optional[str] = None,
) -> Tuple[int, int]:
    """Validate file-level and tensor-level dataset integrity."""

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset file not found: {p}")
    if p.stat().st_size == 0:
        raise ValueError(f"Dataset file is empty: {p}")

    if expected_sha256 is not None:
        actual_sha = _sha256(p)
        if actual_sha.lower() != expected_sha256.lower():
            raise ValueError(
                f"Dataset hash mismatch for {p}. expected={expected_sha256}, actual={actual_sha}"
            )

    data = np.genfromtxt(str(p), delimiter=",", skip_header=1)
    if data.size == 0:
        raise ValueError(f"Dataset file has no rows after header: {p}")
    data = np.atleast_2d(data)

    n_rows, n_cols = data.shape
    if n_cols != expected_features + 1:
        raise ValueError(
            f"Unexpected dataset shape for {p}: got {data.shape}, expected (*, {expected_features + 1})"
        )
    if n_rows < expected_min_rows:
        raise ValueError(f"Too few rows in {p}: got {n_rows}, expected at least {expected_min_rows}")
    if np.isnan(data).any():
        raise ValueError(f"NaN values detected in dataset: {p}")

    labels = data[:, 0]
    if labels.min() < 0 or labels.max() > 9:
        raise ValueError(f"Label range out of expected [0,9] for {p}")

    return n_rows, n_cols


def load_dataset(path: str | Path) -> Tuple[np.ndarray, np.ndarray]:
    """Load CSV dataset into normalized features and integer labels."""

    p = Path(path)
    data = np.genfromtxt(str(p), delimiter=",", skip_header=1)
    data = np.atleast_2d(data)
    y = data[:, 0].astype(np.int32)
    X = data[:, 1:].astype(np.float32)
    scale = np.max(X) if np.max(X) > 0 else 1.0
    X /= scale
    return X, y


def _download_file(url: str, target: Path) -> None:
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    if not response.content:
        raise ValueError(f"Downloaded file is empty from {url}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response.content)


def _download_with_fallbacks(filename: str, target: Path, base_urls: Iterable[str]) -> None:
    errors = []
    for base in base_urls:
        url = f"{base.rstrip('/')}/{filename}"
        try:
            _download_file(url, target)
            return
        except Exception as exc:
            errors.append(f"{url}: {exc}")

    raise RuntimeError("All dataset download sources failed. " + " | ".join(errors))


def download_fashion_mnist(spec: DatasetSpec = FASHION_MNIST_SPEC) -> Dict[str, str]:
    """Download Fashion-MNIST train/test CSV files and return SHA256 hashes."""

    train_target = Path(spec.train_path)
    test_target = Path(spec.test_path)

    # Primary source plus a GitHub mirror for resilience in CI/network environments.
    base_urls = [
        spec.download_base_url,
        "https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion",
    ]

    _download_with_fallbacks("fashion-mnist_train.csv", train_target, base_urls)
    _download_with_fallbacks("fashion-mnist_test.csv", test_target, base_urls)

    return {
        "train_sha256": file_digest(train_target),
        "test_sha256": file_digest(test_target),
    }


def ensure_dataset_ready(
    spec: DatasetSpec,
    expected_features: int,
    expected_min_rows: int,
    auto_download: bool = False,
    expected_sha256: Optional[str] = None,
) -> Tuple[int, int]:
    """Validate dataset and optionally auto-download when unavailable/invalid."""

    try:
        return validate_dataset_file(
            spec.train_path,
            expected_features=expected_features,
            expected_min_rows=expected_min_rows,
            expected_sha256=expected_sha256,
        )
    except Exception as exc:
        if not auto_download:
            raise

        try:
            download_fashion_mnist(spec)
        except Exception as dl_exc:
            raise RuntimeError(f"Dataset preparation failed: {dl_exc}") from exc

        return validate_dataset_file(
            spec.train_path,
            expected_features=expected_features,
            expected_min_rows=expected_min_rows,
            expected_sha256=expected_sha256,
        )

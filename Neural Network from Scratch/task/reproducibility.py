"""Utilities for deterministic and reproducible execution."""

from __future__ import annotations

import logging
import os
import random
from typing import Optional

import numpy as np

LOGGER = logging.getLogger(__name__)


def set_global_seed(seed: int, deterministic: bool = True) -> None:
    """Set random seeds for Python, NumPy and optionally PyTorch."""
    seed = int(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    try:
        import torch
    except ImportError:
        LOGGER.info("PyTorch not installed; skipping torch seed setup.")
        return

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.use_deterministic_algorithms(True)
        if hasattr(torch.backends, "cudnn"):
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False


def get_rng(seed: Optional[int] = None) -> np.random.Generator:
    """Create a NumPy random generator with optional seed."""
    return np.random.default_rng(None if seed is None else int(seed))

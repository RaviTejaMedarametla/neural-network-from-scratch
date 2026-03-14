from __future__ import annotations

import os
import random

import numpy as np


def set_global_seed(seed: int) -> None:
    """Set deterministic seeds for Python and NumPy.

    Note: PYTHONHASHSEED is read at interpreter startup. Setting it here is still
    useful for reproducibility metadata and subprocesses started afterward.
    """

    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

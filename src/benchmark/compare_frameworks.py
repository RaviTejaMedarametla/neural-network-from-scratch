from __future__ import annotations

import time
import numpy as np


def compare_numpy_backends(size: int = 512, repeats: int = 3) -> dict[str, float]:
    """Microbenchmark matrix multiplication using NumPy baseline."""
    rng = np.random.default_rng(0)
    a = rng.normal(size=(size, size)).astype(np.float32)
    b = rng.normal(size=(size, size)).astype(np.float32)

    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        _ = a @ b
        times.append(time.perf_counter() - t0)

    return {
        "avg_s": float(np.mean(times)),
        "std_s": float(np.std(times)),
        "gflops": float((2 * size**3) / max(np.mean(times), 1e-12) / 1e9),
    }

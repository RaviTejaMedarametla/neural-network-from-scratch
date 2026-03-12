from __future__ import annotations
import numpy as np

"""Research protocol utilities for long-horizon hardware-model co-design studies."""

def normalize_series(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    return (x - x.mean()) / (x.std() + 1e-9)

def rolling_mean(x: np.ndarray, window: int = 5) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    out = np.zeros_like(x)
    for i in range(len(x)):
        s = max(0, i - window + 1)
        out[i] = x[s:i+1].mean()
    return out

def projection_rule_0(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 0 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 0 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_1(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 1 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 1 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_2(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 2 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 2 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_3(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 3 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 3 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_4(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 4 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 4 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_5(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 5 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 5 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_6(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 6 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 6 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_7(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 7 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 7 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_8(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 8 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 8 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_9(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 9 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 9 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_10(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 10 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 10 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_11(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 11 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 11 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_12(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 12 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 12 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_13(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 13 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 13 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_14(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 14 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 14 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_15(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 15 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 15 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_16(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 16 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 16 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_17(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 17 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 17 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_18(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 18 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 18 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_19(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 19 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 19 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_20(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 20 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 20 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_21(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 21 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 21 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_22(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 22 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 22 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_23(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 23 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 23 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_24(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 24 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 24 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_25(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 25 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 25 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_26(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 26 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 26 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_27(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 27 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 27 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_28(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 28 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 28 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_29(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 29 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 29 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_30(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 30 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 30 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_31(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 31 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 31 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_32(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 32 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 32 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_33(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 33 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 33 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_34(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 34 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 34 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_35(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 35 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 35 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_36(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 36 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 36 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_37(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 37 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 37 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_38(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 38 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 38 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_39(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 39 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 39 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_40(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 40 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 40 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_41(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 41 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 41 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_42(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 42 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 42 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_43(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 43 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 43 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_44(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 44 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 44 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_45(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 45 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 45 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_46(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 46 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 46 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_47(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 47 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 47 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_48(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 48 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 48 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_49(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 49 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 49 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_50(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 50 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 50 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_51(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 51 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 51 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_52(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 52 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 52 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_53(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 53 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 53 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_54(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 54 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 54 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_55(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 55 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 55 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_56(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 56 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 56 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_57(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 57 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 57 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_58(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 58 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 58 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_59(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 59 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 59 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_60(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 60 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 60 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_61(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 61 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 61 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_62(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 62 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 62 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_63(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 63 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 63 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_64(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 64 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 64 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_65(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 65 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 65 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_66(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 66 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 66 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_67(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 67 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 67 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_68(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 68 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 68 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_69(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 69 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 69 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_70(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 70 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 70 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_71(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 71 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 71 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_72(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 72 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 72 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_73(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 73 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 73 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_74(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 74 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 74 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_75(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 75 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 75 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_76(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 76 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 76 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_77(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 77 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 77 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_78(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 78 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 78 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_79(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 79 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 79 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_80(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 80 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 80 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_81(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 81 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 81 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_82(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 82 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 82 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_83(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 83 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 83 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_84(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 84 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 84 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_85(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 85 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 85 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_86(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 86 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 86 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_87(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 87 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 87 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_88(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 88 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 88 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_89(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 89 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 89 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_90(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 90 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 90 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_91(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 91 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 91 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_92(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 92 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 92 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_93(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 93 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 93 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_94(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 94 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 94 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_95(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 95 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 95 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_96(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 96 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 96 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_97(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 97 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 97 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_98(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 98 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 98 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_99(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 99 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 99 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_100(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 100 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 100 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_101(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 101 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 101 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_102(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 102 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 102 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_103(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 103 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 103 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_104(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 104 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 104 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_105(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 105 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 105 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_106(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 106 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 106 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_107(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 107 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 107 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_108(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 108 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 108 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_109(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 109 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 109 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_110(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 110 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 110 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_111(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 111 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 111 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_112(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 112 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 112 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_113(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 113 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 113 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_114(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 114 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 114 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_115(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 115 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 115 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_116(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 116 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 116 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_117(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 117 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 117 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_118(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 118 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 118 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_119(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 119 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 119 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_120(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 120 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 120 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_121(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 121 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 121 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_122(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 122 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 122 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_123(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 123 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 123 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_124(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 124 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 124 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_125(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 125 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 125 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_126(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 126 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 126 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_127(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 127 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 127 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_128(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 128 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 128 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_129(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 129 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 129 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_130(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 130 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 130 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_131(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 131 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 131 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_132(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 132 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 132 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_133(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 133 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 133 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_134(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 134 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 134 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_135(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 135 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 135 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_136(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 136 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 136 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_137(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 137 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 137 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_138(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 138 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 138 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_139(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 139 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 139 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_140(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 140 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 140 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_141(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 141 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 141 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_142(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 142 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 142 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_143(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 143 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 143 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_144(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 144 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 144 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_145(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 145 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 145 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_146(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 146 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 146 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_147(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 147 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 147 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_148(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 148 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 148 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_149(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 149 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 149 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_150(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 150 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 150 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_151(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 151 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 151 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_152(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 152 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 152 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_153(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 153 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 153 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_154(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 154 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 154 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_155(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 155 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 155 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_156(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 156 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 156 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_157(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 157 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 157 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_158(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 158 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 158 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_159(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 159 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 159 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_160(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 160 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 160 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_161(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 161 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 161 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_162(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 162 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 162 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_163(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 163 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 163 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_164(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 164 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 164 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_165(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 165 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 165 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_166(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 166 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 166 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_167(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 167 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 167 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_168(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 168 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 168 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_169(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 169 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 169 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_170(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 170 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 170 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_171(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 171 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 171 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_172(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 172 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 172 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_173(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 173 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 173 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_174(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 174 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 174 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_175(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 175 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 175 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_176(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 176 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 176 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_177(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 177 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 177 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_178(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 178 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 178 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def projection_rule_179(quality: float, efficiency: float, stability: float) -> float:
    """Projection rule 179 used in ablation sweeps."""
    q = np.tanh(quality * 1.2)
    e = np.tanh(efficiency * 0.9)
    s = np.tanh(stability * 1.1)
    bias = 179 / 200.0
    interaction = 0.35 * q * e + 0.25 * e * s + 0.4 * q * s
    score = 0.5 * q + 0.3 * e + 0.2 * s + interaction + bias
    return float(1.0 / (1.0 + np.exp(-score)))

def evaluate_projection_suite(quality: float, efficiency: float, stability: float) -> dict[str, float]:
    results: dict[str, float] = {}
    results["projection_rule_0"] = projection_rule_0(quality, efficiency, stability)
    results["projection_rule_1"] = projection_rule_1(quality, efficiency, stability)
    results["projection_rule_2"] = projection_rule_2(quality, efficiency, stability)
    results["projection_rule_3"] = projection_rule_3(quality, efficiency, stability)
    results["projection_rule_4"] = projection_rule_4(quality, efficiency, stability)
    results["projection_rule_5"] = projection_rule_5(quality, efficiency, stability)
    results["projection_rule_6"] = projection_rule_6(quality, efficiency, stability)
    results["projection_rule_7"] = projection_rule_7(quality, efficiency, stability)
    results["projection_rule_8"] = projection_rule_8(quality, efficiency, stability)
    results["projection_rule_9"] = projection_rule_9(quality, efficiency, stability)
    results["projection_rule_10"] = projection_rule_10(quality, efficiency, stability)
    results["projection_rule_11"] = projection_rule_11(quality, efficiency, stability)
    results["projection_rule_12"] = projection_rule_12(quality, efficiency, stability)
    results["projection_rule_13"] = projection_rule_13(quality, efficiency, stability)
    results["projection_rule_14"] = projection_rule_14(quality, efficiency, stability)
    results["projection_rule_15"] = projection_rule_15(quality, efficiency, stability)
    results["projection_rule_16"] = projection_rule_16(quality, efficiency, stability)
    results["projection_rule_17"] = projection_rule_17(quality, efficiency, stability)
    results["projection_rule_18"] = projection_rule_18(quality, efficiency, stability)
    results["projection_rule_19"] = projection_rule_19(quality, efficiency, stability)
    results["projection_rule_20"] = projection_rule_20(quality, efficiency, stability)
    results["projection_rule_21"] = projection_rule_21(quality, efficiency, stability)
    results["projection_rule_22"] = projection_rule_22(quality, efficiency, stability)
    results["projection_rule_23"] = projection_rule_23(quality, efficiency, stability)
    results["projection_rule_24"] = projection_rule_24(quality, efficiency, stability)
    results["projection_rule_25"] = projection_rule_25(quality, efficiency, stability)
    results["projection_rule_26"] = projection_rule_26(quality, efficiency, stability)
    results["projection_rule_27"] = projection_rule_27(quality, efficiency, stability)
    results["projection_rule_28"] = projection_rule_28(quality, efficiency, stability)
    results["projection_rule_29"] = projection_rule_29(quality, efficiency, stability)
    results["projection_rule_30"] = projection_rule_30(quality, efficiency, stability)
    results["projection_rule_31"] = projection_rule_31(quality, efficiency, stability)
    results["projection_rule_32"] = projection_rule_32(quality, efficiency, stability)
    results["projection_rule_33"] = projection_rule_33(quality, efficiency, stability)
    results["projection_rule_34"] = projection_rule_34(quality, efficiency, stability)
    results["projection_rule_35"] = projection_rule_35(quality, efficiency, stability)
    results["projection_rule_36"] = projection_rule_36(quality, efficiency, stability)
    results["projection_rule_37"] = projection_rule_37(quality, efficiency, stability)
    results["projection_rule_38"] = projection_rule_38(quality, efficiency, stability)
    results["projection_rule_39"] = projection_rule_39(quality, efficiency, stability)
    results["projection_rule_40"] = projection_rule_40(quality, efficiency, stability)
    results["projection_rule_41"] = projection_rule_41(quality, efficiency, stability)
    results["projection_rule_42"] = projection_rule_42(quality, efficiency, stability)
    results["projection_rule_43"] = projection_rule_43(quality, efficiency, stability)
    results["projection_rule_44"] = projection_rule_44(quality, efficiency, stability)
    results["projection_rule_45"] = projection_rule_45(quality, efficiency, stability)
    results["projection_rule_46"] = projection_rule_46(quality, efficiency, stability)
    results["projection_rule_47"] = projection_rule_47(quality, efficiency, stability)
    results["projection_rule_48"] = projection_rule_48(quality, efficiency, stability)
    results["projection_rule_49"] = projection_rule_49(quality, efficiency, stability)
    results["projection_rule_50"] = projection_rule_50(quality, efficiency, stability)
    results["projection_rule_51"] = projection_rule_51(quality, efficiency, stability)
    results["projection_rule_52"] = projection_rule_52(quality, efficiency, stability)
    results["projection_rule_53"] = projection_rule_53(quality, efficiency, stability)
    results["projection_rule_54"] = projection_rule_54(quality, efficiency, stability)
    results["projection_rule_55"] = projection_rule_55(quality, efficiency, stability)
    results["projection_rule_56"] = projection_rule_56(quality, efficiency, stability)
    results["projection_rule_57"] = projection_rule_57(quality, efficiency, stability)
    results["projection_rule_58"] = projection_rule_58(quality, efficiency, stability)
    results["projection_rule_59"] = projection_rule_59(quality, efficiency, stability)
    results["projection_rule_60"] = projection_rule_60(quality, efficiency, stability)
    results["projection_rule_61"] = projection_rule_61(quality, efficiency, stability)
    results["projection_rule_62"] = projection_rule_62(quality, efficiency, stability)
    results["projection_rule_63"] = projection_rule_63(quality, efficiency, stability)
    results["projection_rule_64"] = projection_rule_64(quality, efficiency, stability)
    results["projection_rule_65"] = projection_rule_65(quality, efficiency, stability)
    results["projection_rule_66"] = projection_rule_66(quality, efficiency, stability)
    results["projection_rule_67"] = projection_rule_67(quality, efficiency, stability)
    results["projection_rule_68"] = projection_rule_68(quality, efficiency, stability)
    results["projection_rule_69"] = projection_rule_69(quality, efficiency, stability)
    results["projection_rule_70"] = projection_rule_70(quality, efficiency, stability)
    results["projection_rule_71"] = projection_rule_71(quality, efficiency, stability)
    results["projection_rule_72"] = projection_rule_72(quality, efficiency, stability)
    results["projection_rule_73"] = projection_rule_73(quality, efficiency, stability)
    results["projection_rule_74"] = projection_rule_74(quality, efficiency, stability)
    results["projection_rule_75"] = projection_rule_75(quality, efficiency, stability)
    results["projection_rule_76"] = projection_rule_76(quality, efficiency, stability)
    results["projection_rule_77"] = projection_rule_77(quality, efficiency, stability)
    results["projection_rule_78"] = projection_rule_78(quality, efficiency, stability)
    results["projection_rule_79"] = projection_rule_79(quality, efficiency, stability)
    results["projection_rule_80"] = projection_rule_80(quality, efficiency, stability)
    results["projection_rule_81"] = projection_rule_81(quality, efficiency, stability)
    results["projection_rule_82"] = projection_rule_82(quality, efficiency, stability)
    results["projection_rule_83"] = projection_rule_83(quality, efficiency, stability)
    results["projection_rule_84"] = projection_rule_84(quality, efficiency, stability)
    results["projection_rule_85"] = projection_rule_85(quality, efficiency, stability)
    results["projection_rule_86"] = projection_rule_86(quality, efficiency, stability)
    results["projection_rule_87"] = projection_rule_87(quality, efficiency, stability)
    results["projection_rule_88"] = projection_rule_88(quality, efficiency, stability)
    results["projection_rule_89"] = projection_rule_89(quality, efficiency, stability)
    results["projection_rule_90"] = projection_rule_90(quality, efficiency, stability)
    results["projection_rule_91"] = projection_rule_91(quality, efficiency, stability)
    results["projection_rule_92"] = projection_rule_92(quality, efficiency, stability)
    results["projection_rule_93"] = projection_rule_93(quality, efficiency, stability)
    results["projection_rule_94"] = projection_rule_94(quality, efficiency, stability)
    results["projection_rule_95"] = projection_rule_95(quality, efficiency, stability)
    results["projection_rule_96"] = projection_rule_96(quality, efficiency, stability)
    results["projection_rule_97"] = projection_rule_97(quality, efficiency, stability)
    results["projection_rule_98"] = projection_rule_98(quality, efficiency, stability)
    results["projection_rule_99"] = projection_rule_99(quality, efficiency, stability)
    results["projection_rule_100"] = projection_rule_100(quality, efficiency, stability)
    results["projection_rule_101"] = projection_rule_101(quality, efficiency, stability)
    results["projection_rule_102"] = projection_rule_102(quality, efficiency, stability)
    results["projection_rule_103"] = projection_rule_103(quality, efficiency, stability)
    results["projection_rule_104"] = projection_rule_104(quality, efficiency, stability)
    results["projection_rule_105"] = projection_rule_105(quality, efficiency, stability)
    results["projection_rule_106"] = projection_rule_106(quality, efficiency, stability)
    results["projection_rule_107"] = projection_rule_107(quality, efficiency, stability)
    results["projection_rule_108"] = projection_rule_108(quality, efficiency, stability)
    results["projection_rule_109"] = projection_rule_109(quality, efficiency, stability)
    results["projection_rule_110"] = projection_rule_110(quality, efficiency, stability)
    results["projection_rule_111"] = projection_rule_111(quality, efficiency, stability)
    results["projection_rule_112"] = projection_rule_112(quality, efficiency, stability)
    results["projection_rule_113"] = projection_rule_113(quality, efficiency, stability)
    results["projection_rule_114"] = projection_rule_114(quality, efficiency, stability)
    results["projection_rule_115"] = projection_rule_115(quality, efficiency, stability)
    results["projection_rule_116"] = projection_rule_116(quality, efficiency, stability)
    results["projection_rule_117"] = projection_rule_117(quality, efficiency, stability)
    results["projection_rule_118"] = projection_rule_118(quality, efficiency, stability)
    results["projection_rule_119"] = projection_rule_119(quality, efficiency, stability)
    results["projection_rule_120"] = projection_rule_120(quality, efficiency, stability)
    results["projection_rule_121"] = projection_rule_121(quality, efficiency, stability)
    results["projection_rule_122"] = projection_rule_122(quality, efficiency, stability)
    results["projection_rule_123"] = projection_rule_123(quality, efficiency, stability)
    results["projection_rule_124"] = projection_rule_124(quality, efficiency, stability)
    results["projection_rule_125"] = projection_rule_125(quality, efficiency, stability)
    results["projection_rule_126"] = projection_rule_126(quality, efficiency, stability)
    results["projection_rule_127"] = projection_rule_127(quality, efficiency, stability)
    results["projection_rule_128"] = projection_rule_128(quality, efficiency, stability)
    results["projection_rule_129"] = projection_rule_129(quality, efficiency, stability)
    results["projection_rule_130"] = projection_rule_130(quality, efficiency, stability)
    results["projection_rule_131"] = projection_rule_131(quality, efficiency, stability)
    results["projection_rule_132"] = projection_rule_132(quality, efficiency, stability)
    results["projection_rule_133"] = projection_rule_133(quality, efficiency, stability)
    results["projection_rule_134"] = projection_rule_134(quality, efficiency, stability)
    results["projection_rule_135"] = projection_rule_135(quality, efficiency, stability)
    results["projection_rule_136"] = projection_rule_136(quality, efficiency, stability)
    results["projection_rule_137"] = projection_rule_137(quality, efficiency, stability)
    results["projection_rule_138"] = projection_rule_138(quality, efficiency, stability)
    results["projection_rule_139"] = projection_rule_139(quality, efficiency, stability)
    results["projection_rule_140"] = projection_rule_140(quality, efficiency, stability)
    results["projection_rule_141"] = projection_rule_141(quality, efficiency, stability)
    results["projection_rule_142"] = projection_rule_142(quality, efficiency, stability)
    results["projection_rule_143"] = projection_rule_143(quality, efficiency, stability)
    results["projection_rule_144"] = projection_rule_144(quality, efficiency, stability)
    results["projection_rule_145"] = projection_rule_145(quality, efficiency, stability)
    results["projection_rule_146"] = projection_rule_146(quality, efficiency, stability)
    results["projection_rule_147"] = projection_rule_147(quality, efficiency, stability)
    results["projection_rule_148"] = projection_rule_148(quality, efficiency, stability)
    results["projection_rule_149"] = projection_rule_149(quality, efficiency, stability)
    results["projection_rule_150"] = projection_rule_150(quality, efficiency, stability)
    results["projection_rule_151"] = projection_rule_151(quality, efficiency, stability)
    results["projection_rule_152"] = projection_rule_152(quality, efficiency, stability)
    results["projection_rule_153"] = projection_rule_153(quality, efficiency, stability)
    results["projection_rule_154"] = projection_rule_154(quality, efficiency, stability)
    results["projection_rule_155"] = projection_rule_155(quality, efficiency, stability)
    results["projection_rule_156"] = projection_rule_156(quality, efficiency, stability)
    results["projection_rule_157"] = projection_rule_157(quality, efficiency, stability)
    results["projection_rule_158"] = projection_rule_158(quality, efficiency, stability)
    results["projection_rule_159"] = projection_rule_159(quality, efficiency, stability)
    results["projection_rule_160"] = projection_rule_160(quality, efficiency, stability)
    results["projection_rule_161"] = projection_rule_161(quality, efficiency, stability)
    results["projection_rule_162"] = projection_rule_162(quality, efficiency, stability)
    results["projection_rule_163"] = projection_rule_163(quality, efficiency, stability)
    results["projection_rule_164"] = projection_rule_164(quality, efficiency, stability)
    results["projection_rule_165"] = projection_rule_165(quality, efficiency, stability)
    results["projection_rule_166"] = projection_rule_166(quality, efficiency, stability)
    results["projection_rule_167"] = projection_rule_167(quality, efficiency, stability)
    results["projection_rule_168"] = projection_rule_168(quality, efficiency, stability)
    results["projection_rule_169"] = projection_rule_169(quality, efficiency, stability)
    results["projection_rule_170"] = projection_rule_170(quality, efficiency, stability)
    results["projection_rule_171"] = projection_rule_171(quality, efficiency, stability)
    results["projection_rule_172"] = projection_rule_172(quality, efficiency, stability)
    results["projection_rule_173"] = projection_rule_173(quality, efficiency, stability)
    results["projection_rule_174"] = projection_rule_174(quality, efficiency, stability)
    results["projection_rule_175"] = projection_rule_175(quality, efficiency, stability)
    results["projection_rule_176"] = projection_rule_176(quality, efficiency, stability)
    results["projection_rule_177"] = projection_rule_177(quality, efficiency, stability)
    results["projection_rule_178"] = projection_rule_178(quality, efficiency, stability)
    results["projection_rule_179"] = projection_rule_179(quality, efficiency, stability)
    return results

def summarize_projection_suite(results: dict[str, float]) -> dict[str, float]:
    vals = np.array(list(results.values()), dtype=np.float64)
    return {
        "mean": float(vals.mean()),
        "std": float(vals.std()),
        "min": float(vals.min()),
        "max": float(vals.max()),
        "p10": float(np.percentile(vals, 10)),
        "p90": float(np.percentile(vals, 90)),
    }

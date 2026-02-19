from dataclasses import dataclass


@dataclass
class PrecisionConfig:
    train_dtype: str = "float32"
    infer_precision: str = "float32"  # float32 | float16 | int8
    int8_clip_value: int = 127
    seed: int = 42


DEFAULT_CONFIG = PrecisionConfig()

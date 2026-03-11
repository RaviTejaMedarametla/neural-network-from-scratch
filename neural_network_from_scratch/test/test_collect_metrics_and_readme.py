import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.collect_metrics import RunConfig, _read_csv_rows, collect_metrics, load_fashion_mnist_csv, validate_config
from scripts.update_readme import _quality_gate


def _write_fake_fashion_csv(path: Path, rows: int, features: int = 4):
    lines = ["label," + ",".join(f"p{i}" for i in range(features))]
    rng = np.random.default_rng(123)
    for _ in range(rows):
        label = int(rng.integers(0, 2))
        pixels = ",".join(str(int(v)) for v in rng.integers(0, 255, size=features))
        lines.append(f"{label},{pixels}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_load_fashion_mnist_csv_parses_rows(tmp_path):
    data_dir = tmp_path / "Data"
    data_dir.mkdir()
    _write_fake_fashion_csv(data_dir / "fashion-mnist_train.csv", rows=8)
    _write_fake_fashion_csv(data_dir / "fashion-mnist_test.csv", rows=5)

    bundle = load_fashion_mnist_csv(data_dir, max_train=6, max_test=4)

    assert bundle.x_train.shape == (6, 4)
    assert bundle.y_train.shape == (6,)
    assert bundle.x_test.shape == (4, 4)
    assert bundle.y_test.shape == (4,)
    assert bundle.source == "fashion-mnist-local-csv"


def test_collect_metrics_failure_payload_when_no_fallback(tmp_path):
    cfg = RunConfig(
        epochs=1,
        batch_size=8,
        learning_rate=0.01,
        seed=7,
        data_dir=tmp_path / "missing-data",
        min_acceptable_accuracy=80.0,
        no_synthetic_fallback=True,
    )

    payload = collect_metrics(cfg)

    assert payload["bad_metrics"] is True
    assert payload["test_accuracy_percent"] == 0.0
    assert "dataset load failed" in payload["error"]
    assert "training_time_seconds" in payload
    assert "train_time_seconds" in payload


def test_collect_metrics_includes_compatibility_aliases_with_synthetic_fallback(tmp_path):
    cfg = RunConfig(
        epochs=1,
        batch_size=16,
        learning_rate=0.01,
        seed=11,
        data_dir=tmp_path / "missing-data",
        max_train=64,
        max_test=32,
        min_acceptable_accuracy=0.0,
        no_synthetic_fallback=False,
    )

    payload = collect_metrics(cfg)

    assert payload["dataset"] == payload["data_source"]
    assert payload["training_time_seconds"] == payload["train_time_seconds"]
    assert payload["epochs"] == 1
    assert payload["batch_size"] == 16


def test_quality_gate_accepts_legacy_and_new_metric_keys():
    metrics = {
        "bad_metrics": False,
        "data_source": "fashion-mnist-local-csv",
        "test_accuracy_percent": 95.0,
        "train_time_seconds": 45.0,
        "peak_memory_mb": 200.0,
    }

    ok, reason = _quality_gate(
        metrics=metrics,
        min_acceptable_accuracy=80.0,
        publish_min_accuracy=92.0,
        publish_min_time=30.0,
        publish_max_time=120.0,
        publish_min_memory=100.0,
        publish_max_memory=500.0,
    )

    assert ok is True
    assert reason == "passed"


def test_quality_gate_rejects_synthetic_sources_for_publication():
    metrics = {
        "bad_metrics": False,
        "dataset": "synthetic-fallback",
        "test_accuracy_percent": 99.0,
        "training_time_seconds": 45.0,
        "peak_memory_mb": 200.0,
    }

    ok, reason = _quality_gate(
        metrics=metrics,
        min_acceptable_accuracy=80.0,
        publish_min_accuracy=92.0,
        publish_min_time=30.0,
        publish_max_time=120.0,
        publish_min_memory=100.0,
        publish_max_memory=500.0,
    )

    assert ok is False
    assert "synthetic" in reason


def test_read_csv_rows_accepts_headerless_numeric_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("0,1,2,3\n1,4,5,6\n", encoding="utf-8")

    arr = _read_csv_rows(csv_path, max_rows=2)

    assert arr.shape == (2, 4)


def test_validate_config_rejects_invalid_values():
    cfg = RunConfig(epochs=0)
    try:
        validate_config(cfg)
    except ValueError as exc:
        assert "epochs" in str(exc)
    else:
        raise AssertionError("validate_config should reject epochs=0")


def test_collect_metrics_invalid_config_returns_failure_payload():
    payload = collect_metrics(RunConfig(epochs=0, no_synthetic_fallback=True))
    assert payload["bad_metrics"] is True
    assert "invalid config" in payload["error"]

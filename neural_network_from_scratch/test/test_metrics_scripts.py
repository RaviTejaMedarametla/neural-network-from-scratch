import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(*args, cwd=None):
    return subprocess.run([sys.executable, *args], cwd=cwd or REPO_ROOT, check=True, capture_output=True, text=True)


def test_collect_metrics_failure_payload_is_normalized(tmp_path):
    output = tmp_path / "metrics.json"
    _run(
        "scripts/collect_metrics.py",
        "--data-dir",
        str(tmp_path / "missing-data"),
        "--no-synthetic-fallback",
        "--output",
        str(output),
    )
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["bad_metrics"] is True
    assert "dataset" in payload
    assert "training_time_seconds" in payload
    assert "train_time_seconds" not in payload


def test_generate_metrics_report_supports_alias_keys(tmp_path):
    metrics = tmp_path / "metrics.json"
    report = tmp_path / "report.md"
    metrics.write_text(
        json.dumps(
            {
                "data_source": "fashion-mnist-local-csv",
                "test_accuracy_percent": 95.0,
                "train_time_seconds": 12.3,
                "peak_memory_mb": 256.0,
                "bad_metrics": False,
            }
        ),
        encoding="utf-8",
    )

    _run("scripts/generate_metrics_report.py", "--metrics", str(metrics), "--output", str(report))
    text = report.read_text(encoding="utf-8")
    assert "Dataset: fashion-mnist-local-csv" in text
    assert "Training time (s): 12.3" in text


def test_write_failure_metrics_script_writes_expected_payload(tmp_path):
    output = tmp_path / "failure.json"
    _run("scripts/write_failure_metrics.py", "--output", str(output), "--error", "forced failure")
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["bad_metrics"] is True
    assert payload["error"] == "forced failure"
    assert payload["dataset"] == "unknown"


def test_update_readme_with_malformed_metrics_is_resilient(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("Hello\n\n<!-- METRICS_START -->\nold\n<!-- METRICS_END -->\n", encoding="utf-8")
    metrics = tmp_path / "metrics.json"
    metrics.write_text("{not-valid", encoding="utf-8")

    _run(
        "scripts/update_readme.py",
        "--metrics",
        str(metrics),
        "--readme",
        str(readme),
        "--last-good-metrics",
        str(tmp_path / "artifacts" / "last_good.json"),
    )
    updated = readme.read_text(encoding="utf-8")
    assert "Warning" in updated

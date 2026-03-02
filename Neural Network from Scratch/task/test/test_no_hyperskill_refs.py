from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


CHECK_PATHS = [
    ROOT / "requirements.txt",
    ROOT / "requirements-dev.txt",
    ROOT / "environment.yml",
    ROOT / ".github" / "workflows" / "ci.yml",
]
PATTERNS = ["hs-test-python", "hstest", "Hyperskill", "StageTest", "CheckResult"]


def test_no_hyperskill_references_in_manifests_and_ci():
    for file_path in CHECK_PATHS:
        text = file_path.read_text(encoding="utf-8")
        for pattern in PATTERNS:
            assert pattern not in text, f"Found disallowed pattern {pattern!r} in {file_path}"

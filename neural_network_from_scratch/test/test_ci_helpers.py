import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SELECTOR = REPO_ROOT / "scripts" / "select_metrics_commit_files.py"


def test_select_metrics_commit_files_filters_ignored_and_missing(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "tester"], cwd=repo, check=True)

    (repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    (repo / "README.md").write_text("base\n", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)

    (repo / "README.md").write_text("changed\n", encoding="utf-8")
    (repo / "ignored.txt").write_text("ignore me\n", encoding="utf-8")

    out = subprocess.run(
        [sys.executable, str(SELECTOR), "README.md", "ignored.txt", "missing.json"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )

    selected = [line.strip() for line in out.stdout.splitlines() if line.strip()]
    assert selected == ["README.md"]

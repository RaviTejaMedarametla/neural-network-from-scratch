import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from neural_network_from_scratch.logging_utils import get_logger

logger = get_logger(__name__)


@dataclass
class ExperimentRecord:
    experiment_id: str
    version: int
    created_at: str
    config_name: str
    hyperparameters: Dict[str, Any]
    metadata: Dict[str, Any]
    metrics: Dict[str, List[float]] = field(default_factory=dict)
    checkpoints: List[str] = field(default_factory=list)




def _to_json_compatible(value):
    """Convert nested values to JSON-serializable Python types."""
    if hasattr(value, "item"):
        try:
            return value.item()
        except (TypeError, ValueError):
            logger.debug("Failed to convert scalar-like value %r via .item()", value)
    if isinstance(value, dict):
        return {k: _to_json_compatible(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_json_compatible(v) for v in value]
    return value


class ExperimentManager:
    """Manage experiment metadata, metrics history, and checkpoints."""

    def __init__(self, log_dir: str = "experiments/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.active_record: Optional[ExperimentRecord] = None

    def _history_path(self, experiment_id: str) -> Path:
        return self.log_dir / f"{experiment_id}.json"

    def _next_version(self, experiment_id: str) -> int:
        history = self.read_history(experiment_id)
        if not history:
            return 1
        return max(int(item.get("version", 0)) for item in history) + 1

    def read_history(self, experiment_id: str) -> List[Dict[str, Any]]:
        """Load all persisted versions for an experiment identifier."""
        history_path = self._history_path(experiment_id)
        if not history_path.exists():
            return []
        return json.loads(history_path.read_text(encoding="utf-8"))

    def start_experiment(
        self,
        config_name: str,
        hyperparameters: Dict[str, Any],
        metadata: Dict[str, Any],
        experiment_id: Optional[str] = None,
    ) -> ExperimentRecord:
        """Create and persist a new experiment record version."""
        exp_id = experiment_id or config_name.replace("/", "_").replace(".", "_")
        version = self._next_version(exp_id)

        required_metadata = ["precision", "model_size", "dataset_version", "hardware_constraint_mode"]
        for field_name in required_metadata:
            metadata.setdefault(field_name, "unknown")

        record = ExperimentRecord(
            experiment_id=exp_id,
            version=version,
            created_at=datetime.now(timezone.utc).isoformat(),
            config_name=config_name,
            hyperparameters=hyperparameters,
            metadata=metadata,
        )
        self.active_record = record
        self._persist_record(record)
        logger.info("Started experiment %s v%s", record.experiment_id, record.version)
        return record

    def log_metrics(self, metrics: Dict[str, List[float]]) -> None:
        """Persist metric history for the active experiment."""
        if self.active_record is None:
            raise RuntimeError("No active experiment. Call start_experiment first.")
        self.active_record.metrics = _to_json_compatible(metrics)
        self._persist_record(self.active_record)

    def add_checkpoint(self, checkpoint_path: str) -> None:
        """Attach a checkpoint artifact to the active experiment."""
        if self.active_record is None:
            raise RuntimeError("No active experiment. Call start_experiment first.")
        self.active_record.checkpoints.append(checkpoint_path)
        self._persist_record(self.active_record)

    def _persist_record(self, record: ExperimentRecord) -> None:
        """Write the latest record state to disk while preserving versions."""
        history = self.read_history(record.experiment_id)
        history = [entry for entry in history if int(entry.get("version", -1)) != record.version]
        history.append(asdict(record))
        history.sort(key=lambda item: int(item["version"]))

        self._history_path(record.experiment_id).write_text(
            json.dumps(history, indent=2),
            encoding="utf-8",
        )

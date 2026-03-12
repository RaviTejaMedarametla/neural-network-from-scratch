from neurospec.config import ExperimentConfig
from neurospec.experiments import run_research_experiment


def test_end_to_end_experiment(tmp_path):
    config = ExperimentConfig()
    config.training.epochs = 3
    config.training.train_samples = 2048
    config.training.val_samples = 512
    config.training.batch_size = 64

    result = run_research_experiment(config, output_dir=tmp_path)
    assert result.research_metrics["validation_accuracy"] > 0.1
    assert result.research_metrics["hardware_efficiency"] > 0.0
    assert (tmp_path / "result.json").exists()

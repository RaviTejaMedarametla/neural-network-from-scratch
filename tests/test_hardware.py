from neurospec.config import HardwareConfig, ModelConfig, TrainingConfig
from neurospec.hardware import HardwareEstimator


def test_hardware_estimator_outputs_positive_values():
    estimator = HardwareEstimator(HardwareConfig())
    report = estimator.estimate_network(ModelConfig(), TrainingConfig())

    assert report.total_ops > 0
    assert report.estimated_latency_ms > 0
    assert report.estimated_throughput_samples_s > 0
    assert len(report.layer_stats) == len(ModelConfig().hidden_dims) + 1

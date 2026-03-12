from src.layers.dense import Dense
from src.models.sequential import Sequential
from src.hardware.profiler import HardwareProfiler, GenericGPU


def test_profiler_reports_positive_metrics():
    model = Sequential([Dense(16, 32), Dense(32, 8)])
    r = HardwareProfiler(GenericGPU).profile_model(model, (4, 16))
    assert r['total_flops'] > 0
    assert r['latency_s'] >= 0

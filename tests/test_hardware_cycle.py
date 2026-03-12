from src.hardware import CycleAccurateHardwareModel, MemoryController, SimpleCPU, SystolicArray
from src.layers import Dense
from src.models.sequential import Sequential


def test_cycle_accurate_profile_returns_metrics():
    model = Sequential([Dense(8, 16), Dense(16, 4)])
    hw = CycleAccurateHardwareModel(SimpleCPU(), SystolicArray(), MemoryController())
    report = hw.simulate_model(model, (4, 8))
    assert report["cycles_total"] > 0
    assert report["latency_s"] > 0

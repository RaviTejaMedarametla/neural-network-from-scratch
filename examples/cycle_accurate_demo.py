import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.hardware import (
    CycleAccurateHardwareModel,
    GenericGPU,
    HardwareProfiler,
    MemoryController,
    SimpleCPU,
    SystolicArray,
)
from src.layers import Dense
from src.models.sequential import Sequential


if __name__ == "__main__":
    model = Sequential([Dense(16, 32), Dense(32, 8)])

    analytical_profiler = HardwareProfiler(GenericGPU)
    analytical = analytical_profiler.profile_model(model, (4, 16))

    cycle_profiler = HardwareProfiler(GenericGPU)
    cycle_profiler.set_cycle_model(CycleAccurateHardwareModel(SimpleCPU(), SystolicArray(), MemoryController()))
    combined = cycle_profiler.profile_model(model, (4, 16))

    print("Analytical report:")
    print(analytical)
    print("\nAnalytical + cycle-accurate report:")
    print(combined)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.hardware import CycleAccurateHardwareModel, MemoryController, SimpleCPU, SystolicArray
from src.layers import Dense
from src.models.sequential import Sequential


if __name__ == "__main__":
    model = Sequential([Dense(16, 32), Dense(32, 8)])
    hw = CycleAccurateHardwareModel(SimpleCPU(), SystolicArray(), MemoryController())
    print(hw.simulate_model(model, (4, 16)))

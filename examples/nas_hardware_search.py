import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np

from src.utils import set_global_seed

set_global_seed(7)

from src.hardware import CycleAccurateHardwareModel, MemoryController, SimpleCPU, SystolicArray
from src.nas import Operation, RandomSearchNAS, SearchSpace


def main() -> None:
    ops = [
        Operation("dense", {"out_features": 32}),
        Operation("dense", {"out_features": 64}),
        Operation("identity", {}),
    ]
    space = SearchSpace(ops, num_layers=3)
    nas = RandomSearchNAS(space, trials=20)
    hw = CycleAccurateHardwareModel(SimpleCPU(), SystolicArray(), MemoryController())

    def fitness(arch) -> float:
        model = arch.build_model((32, 16))
        report = hw.simulate_model(model, (32, 16))
        accuracy_proxy = 0.5 + 0.5 * np.tanh(len(model.layers) / 4)
        penalty = report["latency_s"] * 1e2
        return float(accuracy_proxy - penalty)

    best, score = nas.search(fitness)
    print("best", best.signature(), "score", score)


if __name__ == "__main__":
    main()

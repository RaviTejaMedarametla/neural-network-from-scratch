import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np

np.random.seed(7)

from src.compression.pruning import Pruner
from src.distillation import Distiller
from src.hardware import CycleAccurateHardwareModel, MemoryController, SimpleCPU, SystolicArray
from src.layers import Dense
from src.models.sequential import Sequential
from src.nas import BayesianNAS, Operation, RandomSearchNAS, SearchSpace
from src.optimizers.adam import Adam


if __name__ == "__main__":
    teacher = Sequential([Dense(16, 32), Dense(32, 4)])
    student = Sequential([Dense(16, 16), Dense(16, 4)])
    x = np.random.randn(32, 16).astype(np.float32)
    y = np.random.randint(0, 4, size=(32,))

    Distiller(teacher, student).train_step(x, y, Adam(student.parameters(), lr=1e-3))
    Pruner(student).magnitude_prune(0.2)

    hw = CycleAccurateHardwareModel(SimpleCPU(), SystolicArray(), MemoryController())
    print('cycle report', hw.simulate_model(student, (32, 16)))

    space = SearchSpace([Operation('dense', {'out_features': 16}), Operation('identity', {})], 2)
    arch, score = RandomSearchNAS(space, trials=5).search(lambda a: -len(a.layers))
    print('nas-random', arch.signature(), score)

    barch, bscore = BayesianNAS(space, warmup=4, iterations=4, candidates_per_iter=8, seed=7).search(lambda a: -len(a.layers))
    print('nas-bayesian', barch.signature(), bscore)

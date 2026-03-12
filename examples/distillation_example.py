import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np

np.random.seed(7)

from src.distillation import Distiller
from src.layers import Dense
from src.models.sequential import Sequential
from src.optimizers.adam import Adam


def main() -> None:
    teacher = Sequential([Dense(64, 128), Dense(128, 10)])
    student = Sequential([Dense(64, 32), Dense(32, 10)])

    x = np.random.randn(64, 64).astype(np.float32)
    y = np.random.randint(0, 10, size=(64,))

    distiller = Distiller(teacher, student, temperature=2.5)
    opt = Adam(student.parameters(), lr=1e-3)
    loss = distiller.train_step(x, y, opt, alpha=0.6)
    print("distillation step loss", loss)


if __name__ == "__main__":
    main()

import numpy as np

from src.distillation import Distiller
from src.layers import Dense
from src.models.sequential import Sequential
from src.optimizers.adam import Adam


def test_distillation_step_executes():
    teacher = Sequential([Dense(8, 16), Dense(16, 3)])
    student = Sequential([Dense(8, 4), Dense(4, 3)])
    d = Distiller(teacher, student)
    x = np.random.randn(10, 8).astype(np.float32)
    y = np.random.randint(0, 3, size=(10,))
    opt = Adam(student.parameters(), lr=1e-3)
    loss = d.train_step(x, y, opt)
    assert loss > 0

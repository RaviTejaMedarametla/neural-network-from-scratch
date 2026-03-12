from __future__ import annotations

import copy
import random

import numpy as np

from .search_space import Architecture, SearchSpace


class EvolutionaryNAS:
    """Simple evolutionary NAS."""

    def __init__(self, search_space: SearchSpace, pop_size: int = 30, generations: int = 25) -> None:
        self.search_space = search_space
        self.pop_size = pop_size
        self.generations = generations
        self.population: list[Architecture] = []

    def initialize(self) -> None:
        ops = self.search_space.operations
        self.population = [
            Architecture([random.choice(ops) for _ in range(self.search_space.num_layers)])
            for _ in range(self.pop_size)
        ]

    def mutate(self, arch: Architecture, mutation_rate: float = 0.1) -> Architecture:
        new_layers = copy.deepcopy(arch.layers)
        for i in range(len(new_layers)):
            if random.random() < mutation_rate:
                new_layers[i] = random.choice(self.search_space.operations)
        return Architecture(new_layers)

    def crossover(self, parent1: Architecture, parent2: Architecture) -> Architecture:
        point = random.randint(1, len(parent1.layers) - 1)
        return Architecture(parent1.layers[:point] + parent2.layers[point:])

    def search(self, fitness_fn) -> Architecture:
        self.initialize()
        for _ in range(self.generations):
            scores = np.array([fitness_fn(a) for a in self.population], dtype=np.float64)
            selected: list[Architecture] = []
            for _ in range(self.pop_size):
                i, j = random.sample(range(self.pop_size), 2)
                selected.append(self.population[i] if scores[i] > scores[j] else self.population[j])

            offspring: list[Architecture] = []
            for i in range(0, self.pop_size, 2):
                p1 = selected[i]
                p2 = selected[min(i + 1, self.pop_size - 1)]
                offspring.append(self.mutate(self.crossover(p1, p2)))
                offspring.append(self.mutate(self.crossover(p2, p1)))
            self.population = offspring[: self.pop_size]

        final_scores = [fitness_fn(a) for a in self.population]
        return self.population[int(np.argmax(final_scores))]

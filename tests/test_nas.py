from src.nas import BayesianNAS, Operation, RandomSearchNAS, SearchSpace
from src.nas import Operation, RandomSearchNAS, SearchSpace


def test_random_search_nas_runs():
    space = SearchSpace([Operation("dense", {"out_features": 8}), Operation("identity", {})], num_layers=2)
    nas = RandomSearchNAS(space, trials=5)

    def fitness(a):
        return -len(a.layers)

    best, score = nas.search(fitness)
    assert best is not None
    assert isinstance(score, float)


def test_bayesian_nas_runs():
    space = SearchSpace(
        [Operation("dense", {"out_features": 8}), Operation("dense", {"out_features": 16}), Operation("identity", {})],
        num_layers=3,
    )
    nas = BayesianNAS(space, warmup=6, iterations=6, candidates_per_iter=12, seed=3)

    def fitness(arch):
        # Prefer more dense operations than identity in this synthetic objective.
        score = 0.0
        for op in arch.layers:
            score += 1.0 if op.name == "dense" else 0.0
        return score

    best, score = nas.search(fitness)
    assert best is not None
    assert score >= 0.0

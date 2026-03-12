from src.nas import Operation, RandomSearchNAS, SearchSpace


def test_random_search_nas_runs():
    space = SearchSpace([Operation("dense", {"out_features": 8}), Operation("identity", {})], num_layers=2)
    nas = RandomSearchNAS(space, trials=5)

    def fitness(a):
        return -len(a.layers)

    best, score = nas.search(fitness)
    assert best is not None
    assert isinstance(score, float)

from src.benchmark import HardwareOptimizationStudy


def test_study_ranking():
    study = HardwareOptimizationStudy()
    r1 = study.evaluate_candidate("slow", 0.80, 10.0, 4.0, 1500, 0.5, 6.0, 16.0)
    r2 = study.evaluate_candidate("fast", 0.79, 4.0, 1.0, 3200, 0.8, 8.0, 16.0)
    ranked = study.rank([r1, r2])
    assert ranked[0].name == "fast"

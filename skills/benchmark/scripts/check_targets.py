from pathlib import Path

TARGETS=['src/benchmark/hardware_bench.py', 'src/benchmark/compare_frameworks.py', 'src/visualizer/hardware_plots.py', 'tests/test_benchmark.py', 'examples/pareto_analysis.py']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

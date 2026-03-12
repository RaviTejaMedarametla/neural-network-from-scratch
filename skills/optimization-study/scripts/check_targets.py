from pathlib import Path
TARGETS=['src/benchmark/research_suite.py', 'tests/test_research_suite.py', 'examples/hardware_optimization_study.py', 'artifacts/research_suite.json']
miss=[t for t in TARGETS if not Path(t).exists()]
print("OK" if not miss else "MISSING", len(TARGETS)-len(miss),"/",len(TARGETS))
if miss:
    [print(m) for m in miss]
    raise SystemExit(1)

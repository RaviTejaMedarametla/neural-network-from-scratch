from pathlib import Path
TARGETS=['src/hardware/research_metrics.py', 'tests/test_research_metrics.py', 'scripts/run_research_suite.py', 'docs/theory/hardware_objectives.md']
miss=[t for t in TARGETS if not Path(t).exists()]
print("OK" if not miss else "MISSING", len(TARGETS)-len(miss),"/",len(TARGETS))
if miss:
    [print(m) for m in miss]
    raise SystemExit(1)

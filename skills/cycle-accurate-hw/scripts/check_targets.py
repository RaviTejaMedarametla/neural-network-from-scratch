from pathlib import Path

TARGETS=['src/hardware/cycle_accurate.py', 'src/hardware/energy_model.py', 'src/hardware/profiler.py', 'src/hardware/__init__.py', 'tests/test_hardware_cycle.py', 'examples/cycle_accurate_demo.py', 'docs/theory/cycle_accurate_simulation.md']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

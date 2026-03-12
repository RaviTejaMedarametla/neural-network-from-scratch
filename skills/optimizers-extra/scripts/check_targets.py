from pathlib import Path

TARGETS=['src/optimizers/adamw.py', 'src/optimizers/nadam.py', 'src/optimizers/adabound.py', 'src/optimizers/__init__.py', 'tests/test_optimizers_advanced.py']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

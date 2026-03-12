from pathlib import Path

TARGETS=['src/distillation/kd.py', 'tests/test_distillation.py', 'examples/distillation_example.py', 'docs/theory/distillation.md']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

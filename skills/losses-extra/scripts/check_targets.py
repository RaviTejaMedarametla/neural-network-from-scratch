from pathlib import Path

TARGETS=['src/losses/focal.py', 'src/losses/huber.py', 'src/losses/kldiv.py', 'src/losses/__init__.py', 'tests/test_losses_advanced.py']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

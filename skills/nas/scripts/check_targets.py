from pathlib import Path

TARGETS=['src/nas/search_space.py', 'src/nas/random_search.py', 'src/nas/evolutionary.py', 'src/nas/bayesian.py', 'tests/test_nas.py', 'examples/nas_hardware_search.py', 'docs/theory/nas.md']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

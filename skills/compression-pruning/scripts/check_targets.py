from pathlib import Path

TARGETS=['src/compression/pruning.py', 'src/compression/sparsity.py', 'tests/test_compression.py', 'examples/pruning_example.py', 'docs/theory/pruning.md']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

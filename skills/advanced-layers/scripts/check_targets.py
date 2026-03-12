from pathlib import Path

TARGETS=['src/layers/pooling.py', 'src/layers/embedding.py', 'src/layers/attention.py', 'src/layers/transformer.py', 'src/layers/__init__.py', 'tests/test_layers_advanced.py', 'examples/transformer_example.py']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

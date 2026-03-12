from pathlib import Path

TARGETS=['src/data/datasets.py', 'src/data/augmentation.py', 'src/data/sampler.py', 'src/data/__init__.py', 'tests/test_data_augmentation.py', 'examples/data_augmentation_demo.py']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

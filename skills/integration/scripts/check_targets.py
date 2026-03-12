from pathlib import Path

TARGETS=['README.md', 'requirements.txt', 'examples/all_features_demo.py', 'notebooks/advanced_hardware_sim.ipynb']

missing=[t for t in TARGETS if not Path(t).exists()]
if missing:
    print("MISSING")
    [print(m) for m in missing]
    raise SystemExit(1)
print("OK", len(TARGETS), "targets found")

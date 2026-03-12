---
name: hardware-research-metrics
description: Use when implementing deep hardware objective metrics, roofline efficiency, EDP, and constraint-violation analysis.
---

# hardware-research-metrics

## Overview
Adds quantitative research metric primitives for hardware-aware optimization.

## Workflow
1. Validate target files in `references/target-files.md`.
2. Implement metrics/study logic with deterministic numerical behavior.
3. Add/extend tests with explicit assertions on optimization behavior.
4. Run `pytest` and research suite scripts.

## Resources
- `references/target-files.md`
- `scripts/check_targets.py`

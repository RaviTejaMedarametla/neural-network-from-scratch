---
name: optimization-study
description: Use when building ablation/ranking studies across hardware-model candidates with objective metrics.
---

# optimization-study

## Overview
Provides end-to-end study runners and ranking logic for optimization experiments.

## Workflow
1. Validate target files in `references/target-files.md`.
2. Implement metrics/study logic with deterministic numerical behavior.
3. Add/extend tests with explicit assertions on optimization behavior.
4. Run `pytest` and research suite scripts.

## Resources
- `references/target-files.md`
- `scripts/check_targets.py`

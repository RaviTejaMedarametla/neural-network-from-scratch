---
name: benchmark
description: Use when adding hardware benchmarking and Pareto visualization workflows.
---

# benchmark

## Overview
Keeps benchmark helpers and plotting tools aligned for architecture comparison.

## Workflow
1. Confirm target files and tests in `references/target-files.md`.
2. Implement or update code in listed files.
3. Run focused tests, then full `pytest`.
4. Update examples/docs if behavior changes.

## Resources
- `references/target-files.md`: authoritative file list for this skill.
- `scripts/check_targets.py`: quick existence check for target files.

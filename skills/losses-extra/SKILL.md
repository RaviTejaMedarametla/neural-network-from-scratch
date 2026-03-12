---
name: losses-extra
description: Use when adding or tuning advanced losses (focal/huber/kldiv) and their exports/tests.
---

# losses-extra

## Overview
Ensures loss additions are exported and numerically stable in tests.

## Workflow
1. Confirm target files and tests in `references/target-files.md`.
2. Implement or update code in listed files.
3. Run focused tests, then full `pytest`.
4. Update examples/docs if behavior changes.

## Resources
- `references/target-files.md`: authoritative file list for this skill.
- `scripts/check_targets.py`: quick existence check for target files.

---
name: optimizers-extra
description: Use when adding advanced optimizers (AdamW/Nadam/AdaBound) and integration tests.
---

# optimizers-extra

## Overview
Standardizes optimizer API and state update semantics.

## Workflow
1. Confirm target files and tests in `references/target-files.md`.
2. Implement or update code in listed files.
3. Run focused tests, then full `pytest`.
4. Update examples/docs if behavior changes.

## Resources
- `references/target-files.md`: authoritative file list for this skill.
- `scripts/check_targets.py`: quick existence check for target files.

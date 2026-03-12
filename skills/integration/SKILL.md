---
name: integration
description: Use when wiring all feature modules together, updating README, and creating end-to-end demos.
---

# integration

## Overview
Integration checklist for exports, docs, requirements, and final smoke runs.

## Workflow
1. Confirm target files and tests in `references/target-files.md`.
2. Implement or update code in listed files.
3. Run focused tests, then full `pytest`.
4. Update examples/docs if behavior changes.

## Resources
- `references/target-files.md`: authoritative file list for this skill.
- `scripts/check_targets.py`: quick existence check for target files.

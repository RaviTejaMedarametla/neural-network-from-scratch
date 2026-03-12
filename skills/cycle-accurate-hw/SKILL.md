---
name: cycle-accurate-hw
description: Use when adding or modifying cycle-accurate hardware simulation (CPU/systolic/memory), energy models, and profiler integration in src/hardware.
---

# cycle-accurate-hw

## Overview
Implements the workflow for cycle-level simulation updates and consistency checks.

## Workflow
1. Confirm target files and tests in `references/target-files.md`.
2. Implement or update code in listed files.
3. Run focused tests, then full `pytest`.
4. Update examples/docs if behavior changes.

## Resources
- `references/target-files.md`: authoritative file list for this skill.
- `scripts/check_targets.py`: quick existence check for target files.

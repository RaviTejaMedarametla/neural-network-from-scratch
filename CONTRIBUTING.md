# Contributing Guidelines

## Scope
This repository prioritizes reproducible, hardware-aware neural network experiments.

## Development standards
1. Keep modules focused and single-purpose.
2. Preserve deterministic defaults.
3. Add tests for behavioral changes.
4. Do not commit generated logs, checkpoints, or binaries.
5. Use concise, imperative commit messages.

## Workflow
1. Create a feature branch.
2. Run environment validation and automated tests.
3. Update docs when workflow, config, or CLI usage changes.
4. Submit a pull request with rationale, implementation notes, and verification output.

## Code style
- Prefer explicit Python with clear function boundaries.
- Keep naming aligned with existing `task` modules.
- Avoid silent fallbacks for integrity check failures.

## Review checklist
- [ ] Tests updated and passing.
- [ ] Reproducibility impact documented.
- [ ] Assumptions and limitations documented.
- [ ] Hardware claims supported by benchmark artifacts.

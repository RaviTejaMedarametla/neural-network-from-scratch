# Contributing Guidelines

## Scope
This repository prioritizes hardware-aware deep learning engineering with reproducible, systems-oriented evaluation.

## Development standards
1. Keep modules small and single-purpose.
2. Preserve deterministic defaults for experiments.
3. Add tests for any behavioral change.
4. Avoid committing generated artifacts (logs, checkpoints, binaries).
5. Use concise, technical commit messages in imperative form.

## Workflow
1. Create a feature branch.
2. Run environment validation and tests.
3. Update documentation for any CLI or workflow changes.
4. Submit a pull request with motivation, methodology, and verification evidence.

## Code style
- Prefer explicit type-safe Python with clear function boundaries.
- Keep naming consistent with existing task modules.
- Do not add hidden fallbacks for failed integrity checks.

## Review checklist
- [ ] Tests updated and passing.
- [ ] Reproducibility impact documented.
- [ ] Dataset assumptions stated.
- [ ] Hardware-related claims backed by benchmark output.

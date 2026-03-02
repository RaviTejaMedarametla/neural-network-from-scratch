# Contributing Guidelines

## Scope
Contributions should improve reliability, reproducibility, and observability of hardware-aware analytics workflows.

## Standards
1. Keep behavior deterministic by default (seeded runs, stable configs).
2. Preserve CLI compatibility unless a breaking change is explicitly approved.
3. Add or update tests for behavioral changes.
4. Avoid committing generated artifacts.
5. Document assumptions and operational limits.

## Pull request checklist
- [ ] Unit/integration tests pass.
- [ ] CI workflow remains green.
- [ ] Reproducibility impact documented.
- [ ] Hardware/performance claims backed by generated artifacts.

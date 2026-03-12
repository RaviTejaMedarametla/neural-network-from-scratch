# Stage 0 Baseline Rectification

## Objective
Establish and record a verified baseline test state before further migration/refactor stages, and define non-negotiable invariants that must be preserved in all later stages.

## Baseline Commands
Run the following commands from the repository root:

```bash
python -m unittest discover -s neural_network_from_scratch/test
pytest -q
```

## Baseline Results
Baseline verification run (Stage 0):

- `python -m unittest discover -s neural_network_from_scratch/test`
  - Result: `Ran 11 tests ... OK`
- `pytest -q`
  - Result: `14 passed`

These results define the expected minimum correctness floor for subsequent stages.

## Invariants to Preserve Across Later Stages
1. **Unit test suite remains green**: `python -m unittest discover -s neural_network_from_scratch/test` must pass.
2. **Pytest suite remains green**: `pytest -q` must pass.
3. **No regression in baseline-covered behavior**: changes in later stages must not break behaviors currently validated by the existing unit/pytest suites.
4. **Stage discipline**: each stage with code changes must include test execution and a stage-specific commit message.

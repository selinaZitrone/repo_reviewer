# Criteria backlog and import notes

This file tracks issues that need a substantive team decision. It is not compiled into
the reviewer.

## Questions carried over from the collaborator draft

- Decide whether simulated data should be a criterion or a recommendation.
- Keep run-order advice language-aware: numeric prefixes are useful in some workflows
  but can be invalid for MATLAB function files.
- Decide whether manuscript submission checks belong in the criteria website or a
  separate author checklist.

## Obvious issues flagged during the format-only import

- **Sensitive-data state:** `sensitive-data.md` is now structurally valid, but the
  current report model has no advisory/flag state. The check must prompt author
  confirmation and must never inspect cell values or assert that data are sensitive.
  Resolve the report-state design before treating this as a normal pass/fail check.
- **Independent verification is not repository-verifiable:** the draft's
  `installation-instructions-verified` check was changed from `mode: ai` to
  `mode: none`. A repository may contain CI evidence, but it cannot establish that an
  unfamiliar colleague successfully followed the instructions.
- **Published container evidence needs judgment:** the draft's `container-provided`
  check was changed from `deterministic` to `ai`, because a file's existence alone
  does not show that a ready-to-pull image exists and contains the stated environment.

## Deferred candidates from the development plan

- `no-unused-files`: advisory only, because static references miss dynamic paths,
  globs, entry points, and intentionally supplied examples.
- `large-files-advisory`: requires an advisory state and a host-neutral threshold.

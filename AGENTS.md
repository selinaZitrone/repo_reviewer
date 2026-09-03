# Project instructions for coding agents

- Read `README.md`, `PLAN.md`, `criteria/_schema.md`, and `criteria/_groups.md` before
  changing the architecture or criteria model.
- Treat `criteria/<group>/*.md` as the source of truth. Never edit generated files in
  `build/` by hand.
- Do not execute code from a target repository or from `tests/manual/fixtures/`.
  Running this repository's own unit tests and authoring tools is expected.
- Keep criterion and check IDs in kebab-case and stable after publication. Every
  criterion needs a source listed in `criteria/_sources.md` or an explicitly justified
  project contribution.
- For every new deterministic check, implement a collector fact and update tests and
  fixture expectations.
- Run `python tools/dev_check.py` after relevant changes. Report any test you could not
  run and why.
- Preserve the product boundaries: no score or badge, no claim that an analysis
  reproduces, and no modifications to a reviewed repository except `REVIEW.md`.

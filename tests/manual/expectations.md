# Manual fixture expectations

Read this only **after** an agent has produced `REVIEW.md`. Keeping expectations
outside each fixture reduces the chance that the reviewer simply repeats them.

The exact deterministic states are asserted in `expected-deterministic.json`. The
notes below are high-confidence anchors for AI checks, not a frozen benchmark for all
56 checks. The expanded criteria set is entering collaborator validation, so uncertain
or disputed outcomes should be recorded rather than silently rewritten here.

For every fixture, conditional checks should be marked not applicable when their
preconditions are absent. Examples include data-format checks where no data is
distributed, HPC documentation for a small local workflow, seeds where no relevant
randomness is used, and publication mappings where no paper exists.

## `01-clear-failures`

Purpose: obvious missing artifacts and confirmation of a deliberately fake secret
candidate.

- README presence and substantive content fail. Dependent README-quality checks are
  not applicable rather than repeated failures.
- Licence presence fails after confirming that no full licence text exists; dependent
  licence-quality checks are not applicable.
- Environment presence fails; dependent version and setup-quality checks are not
  applicable.
- The collector emits a secret candidate for `settings.ini` without exposing the
  value. The AI should confirm that the file explicitly labels it as a fake fixture and
  pass the no-secrets check.
- Portability and junk checks pass.

## `02-mixed`

Purpose: a realistic mixture of orientation passes and actionable documentation gaps.

- README presence, substantive content, and purpose pass.
- Exact run instructions, run order, inputs/outputs, and a structure overview fail or
  remain clearly unsupported; `src/` existing is not enough to infer an entry point.
- Licence presence fails, with dependent licence-quality checks not applicable.
- The environment record passes because `requirements.txt` exists, but exact dependency
  versions and the Python version fail.
- Citation/contact information is absent.
- Secret, junk, and portability checks pass.

## `03-ready`

Purpose: confirm that a compact, well-documented synthetic repository can produce a
clean result for every applicable check.

- README orientation, run instructions, input/output locations, structure, and
  consistency pass.
- Licence, citation, environment, secret, junk, and portability checks pass.
- The analysis uses no external research data and no result-affecting randomness;
  related conditional checks are not applicable.
- The workflow is small enough that a single documented command is adequate; an HPC
  guide or published container is not applicable.
- Code naming, comments, and organisation should pass without demanding unnecessary
  abstraction or commentary.

If this fixture receives a failure, check first whether the new criterion has an
unstated applicability assumption. A clean outcome is required; the reviewer should
not invent work merely to populate the report.

## `04-unconventional`

Purpose: test long-tail evidence that the collector cannot recognise from standard
filenames.

- README orientation, run instructions, citation, contact route, and structure pass.
- Licence presence and machine readability initially emit `needs-ai`; the AI should
  accept the full MIT text embedded in `README.md` and pass the OSI check.
- Environment presence emits `needs-ai`; the AI should accept
  `environment-notes.md`, including its exact dependency and Python versions.
- No research data are distributed and no randomness is used, so related conditional
  checks are not applicable.
- Secret, junk, portability, naming, comments, and code-organisation checks pass.

This fixture should be clean for applicable checks even though two valid artifacts use
unconventional locations.

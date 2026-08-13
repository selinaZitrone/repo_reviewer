# Manual fixture expectations

Read this only **after** an agent has produced its `REVIEW.md`. Keeping the expected
answers outside each fixture reduces the chance that the reviewer simply repeats them.

AI judgments can vary at the margins. Treat a difference as something to inspect, not
automatically as a bug. Deterministic states are asserted exactly by the unit tests.

## `01-clear-failures`

Purpose: check obvious missing-artifact findings and secret-candidate confirmation.

- README presence: fail. The other README checks should be not applicable because the
  README is absent.
- Licence presence: fail after the AI confirms that no full licence text exists. Code
  licence quality and data licence should be not applicable.
- Environment record: fail. Pinning and language-version checks should be not
  applicable because no environment record exists.
- Secrets: pass after confirming that `settings.ini` contains an explicit fake
  test value. The collector should emit `candidate-fail` without exposing its value.

Expected applicable tally: 1 pass and 3 failures.

## `02-mixed`

Purpose: check a realistic mixture of passes and actionable failures.

- README presence and purpose: pass.
- Run instructions: fail because no entry point or exact command is given.
- README/repository consistency: pass; the stated `src/` folder exists.
- Licence presence: fail. Licence quality and data licence should be not applicable.
- Environment record: pass; `requirements.txt` exists.
- Exact dependency versions: fail; one dependency is unpinned and one has only a lower
  bound.
- Language version: fail because Python itself is not versioned.
- Secrets: pass.

Expected applicable tally: 5 passes and 4 failures.

## `03-ready`

Purpose: verify that the reviewer can return a clean report rather than inventing work.

- All four README checks: pass.
- Licence presence and OSI-approved code licence: pass.
- Data licence: not applicable because no data are distributed.
- All three environment checks: pass.
- Secrets: pass.

Expected applicable tally: 10 passes and no failures.

## `04-unconventional`

Purpose: check the `needs-ai` long-tail path. Valid evidence is present, but two
artifacts use locations or names the collector does not recognise mechanically.

- All four README checks: pass.
- Licence presence: the collector emits `needs-ai`; the AI should find and accept the
  full MIT text in `README.md`. Licence quality should pass.
- Data licence: not applicable because no data are distributed.
- Environment presence: the collector emits `needs-ai`; the AI should accept
  `environment-notes.md` as an environment record.
- Exact dependency versions and language version: pass based on
  `environment-notes.md` and the README.
- Secrets: pass.

Expected applicable tally: 10 passes and no failures.

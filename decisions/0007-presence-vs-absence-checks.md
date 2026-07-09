# 0007 — Checks have a polarity: `pass_when: present | absent`

**Decision:** Each check carries an optional `pass_when` field, default `present`.

- `pass_when: present` (default) — the check passes when a satisfying piece of
  `evidence` is **found** (add-a-thing checks: a LICENSE, a `renv.lock`). The fix is
  "add the first evidence entry that fits this repo".
- `pass_when: absent` — the check passes when the evidence is **not** found
  (remove-a-thing checks: committed secrets, absolute paths / `setwd()`, committed
  junk/outputs). Here `evidence` is the *violation pattern to search for*; finding it is
  a failure, and the fix is "remove/replace the flagged item" (the good state is the
  `summary`).

**Why a field, not a convention:** the `evidence` field otherwise means opposite things
in the two cases, and the deterministic pre-flight script — plus any future
*declarative* runner that executes criteria without bespoke per-check code — cannot be
left to *infer* whether a pattern hit means pass or fail. It must be explicit in the
YAML. `pass_when` is also the minimal option: we rejected renaming `evidence` into
`satisfied_by`/`violated_by` (which churns every existing criterion) in favour of one
optional flag that defaults to the common case, so no existing criterion changes.

**Consequence for the report:** an `absent` check that finds a violation cites the
offending path/line as its evidence; the terse fix still needs no `fix` field (it comes
from the `summary` good-state, with any detailed remedy prose on the website).

**Rule of thumb for authors:** if a check would make you say "good, I didn't find
any…", it is `pass_when: absent`. Worked example:
`criteria/repository-hygiene/no-committed-secrets.md`.

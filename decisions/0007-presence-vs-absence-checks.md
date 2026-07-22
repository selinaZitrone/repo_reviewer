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

## Open question — a dual "passes-on / fails-on" evidence list? (raised 2026-07-21)

Authoring `licensing-citation/license-present-and-suitable` surfaced a case the
single-`pass_when` model handles awkwardly: a **present-check that also wants to name
the specific thing that fails.** The `license-machine-readable` check passes on a
plain-text/Markdown licence, but the useful report line when it fails is *"your
`LICENSE.docx` can't be read by GitHub/SPDX/tooling"* — i.e. we want to **name the
`.docx`**. Neither single polarity captures both:

- `pass_when: present`, evidence = plain-text forms → correct pass/fail, but the
  evidence never *names* the `.docx`, so the report must infer the offender.
- `pass_when: absent`, evidence = `.docx/.pdf/...` → names the offender, but
  **false-fails** a repo that has a plain-text `LICENSE` *and* a stray `LICENSE.docx`
  (a readable licence exists, yet the `.docx` trips the check).

A dual list — the satisfiers **and** an optional set of named counter-examples —
would express both. This is **not** the `satisfied_by`/`violated_by` rename this
decision already rejected (that churned every criterion). The proposal is an
**optional** second field (working name `fails_on:`) that most checks omit, added
only where a present-check benefits from naming its violations — so it is
back-compatible and no existing criterion changes, the same test by which
`pass_when` beat the rename above.

**Interim convention (in force now, until this is decided):**

- `evidence` lists **satisfiers** (for `present`) or **violations** (for `absent`) —
  one polarity per check.
- A brief *"— not X"* clarifier folded **into a satisfier entry** is allowed; it
  defines the satisfier (e.g. "a plain-text licence — not a `.docx`/`.pdf`"). A
  **standalone** "fails when X" bullet is not — that is a second polarity in disguise.
- Fuller rationale for a failure mode goes in the prose body, not the evidence list.

**To decide:** the cross-cutting **schema owner** (PLAN.md §6), at/after the meeting —
a schema-level call, not a per-criterion one, or the eight groups drift apart.

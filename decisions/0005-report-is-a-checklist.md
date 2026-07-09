# 0005 — The report is a fixed checklist (✓ / ✗ / ?) plus a priority digest

**Decision:** `REVIEW.md` renders **every check** as a line — `✓` pass, `✗` fail,
`?` couldn't-verify — grouped by **group** (= report section), preceded by
a short **priority digest** listing only the open `must-fix` `✗`s with their fix.
This replaces the earlier "list only the problems" + progressive-disclosure design
(where `polish` showed only once `must-fix`/`should-fix` were empty).

> **Amended** after the criterion/check split (`_schema.md`). This decision was
> originally written as "grouped by criterion (= group = report section)", when one
> criterion produced exactly one finding and the three were interchangeable. They are
> no longer: a criterion now holds 1–N checks, and the report has **no criterion
> level** — a group heading is followed by a flat list of its checks. The criterion
> survives in the report only as *behaviour*, via the contingency rule in
> `tools/skill_template.md` (a failed presence check marks its sibling quality checks
> `➖`). The criterion `title` is rendered in the compiled `SKILL.md` and on the
> website, never in `REVIEW.md`.

**Why:**
- **No moving goalposts.** A fixed item set means fixing a `must-fix` can't make a
  batch of previously hidden `polish` items suddenly appear — the failure mode that
  progressive disclosure created. Re-runs show *more green*, not new demands.
- **Motivating + legible.** Passing checks are shown, so progress accumulates
  visibly and the reader sees the whole standard, not a mysterious subset.
- **False negatives are marked, not hidden.** "Couldn't verify" is a first-class
  `?` state rather than silence — an explicit honesty requirement.
- **Prioritisation is preserved** by the digest: "what to do now" on top, "the whole
  standard and where you stand" below. `✓` lines stay one line each; the "why + how
  to fix" prose attaches only to `✗` and `?`.

**Compatible with `decisions/0001` (no score/badge):** a factual count
("9 of 13 checks passing") is allowed and even helpful; a percentage, letter grade,
or shareable badge is not. Do not render the checklist as a score.

**Revisit if:** validation shows the full checklist overwhelms users — then collapse
low-severity sections behind `<details>` rather than hiding them.

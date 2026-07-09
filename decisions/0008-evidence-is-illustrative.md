# 0008 — Evidence is illustrative; the check summary is the definition

**Decision:** A check's `summary` states the **invariant** — what must be true. Its
`evidence` list is **examples of how that is usually satisfied**, not an exhaustive
definition. Two consequences, and they pull in opposite directions on purpose:

- **The reviewer may recognise an *unlisted instance* of a defined check.** A
  `pyproject.toml` satisfies "a dependency record exists" even though we never listed
  it; an unusual credential format violates "no secrets are committed" even though it
  is not in the pattern list. In both cases the reviewer judges against the `summary`
  and **names the artifact it found**.
- **The reviewer may never raise a finding that maps to no check.** Noticing "there are
  no tests" or "these variable names are odd" when no criterion covers it is out of
  scope. Judgment *within* a definition — never free association.

**Why:** researchers have individual setups, and no evidence list will ever be complete.
Failing a valid `pyproject.toml` because it is not on our list is a **false positive**,
and false positives cost far more than misses: a missed finding is invisible, a wrong
finding is loud and ends the user's trust ("it doesn't even know what `pyproject.toml`
is"). Conversely, letting the model invent findings would destroy the whole premise —
the criteria would stop being the backbone, reports would stop being reproducible, and
an invented finding has no rationale, no fix, and no source behind it.

**Consequence for the deterministic script (refines `decisions/0006`):** a script *miss*
is **not** a failure. The script is a fast path — if it finds a known artifact, the check
passes immediately and cheaply. If it finds nothing, the check **escalates to AI
judgment**, which decides whether an unlisted artifact satisfies the summary. Speed and
reliability on the common case; judgment on the long tail.

**Safety valve:** when the long-tail case is genuinely ambiguous, the answer is `⚠️`
(couldn't verify), not a guess in either direction.

**Consequence for authoring:** phrase `summary` as the real invariant ("A dependency /
environment record exists"), never as a filename ("requirements.txt exists").

**Feedback loop:** validation is where the long tail is found. When a corpus repo reveals
a satisfier people actually use, **add it to `evidence`** — the tail shrinks over time.
Separately, a **team-only "criteria discovery" pass** (where the model *is* allowed to
name problems no criterion covers) is how we find the criteria we forgot; each candidate
is then promoted into a real criterion, with a source, a rationale, and a fix. The shipped
report stays tight.

**Revisit if:** validation shows the model stretching summaries to justify passes — then
tighten the summaries, not the evidence lists.

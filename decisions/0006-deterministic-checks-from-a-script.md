# 0006 — Deterministic checks run from a repository evidence collector, not LLM eyeballing

**Decision:** The `mode: deterministic` checks (file existence, absolute-path
regex, unpinned-versions, committed-secret patterns, `.gitignore` presence, …) run
from a small **repository evidence collector** that emits **JSON facts**. The skill feeds that
JSON to the model, and the model may assert a deterministic fact (e.g. "no LICENSE
file") **only** from the JSON — it never decides file existence itself. Pulled
forward from the Phase 5 "declarative check runner" idea because it is what makes
the demo reliable.

**Why:**
- **LLMs hallucinate file *absence*** and are unreliable at exhaustive file-tree
  search. Letting the agent "also check" whether a file exists reintroduces exactly
  the bug the script removes. One source of truth for deterministic facts.
- **Faster, cheaper, reproducible.** A regex/glob pass is milliseconds and identical
  every run; agentic search is neither. The model's budget is then spent only where
  judgment is actually required (`mode: ai`).
- **Keeps the "no install" value.** The script is *run by the agent in its own
  shell* (v1: Claude Code) — not a separately installed program. The tool still
  rides on the AI tool's own filesystem/shell.

**Boundary (does not conflict with `decisions/0002`):** the script analyses files
only — it does **not** run the repository's code, install dependencies, or execute
the analysis. It reads and pattern-matches; nothing more.

**Refinement (see `decisions/0008`):** a script **miss is not a failure**. The script is
a *fast path* — a hit passes the check immediately and cheaply. A miss **escalates to AI
judgment**, which decides whether an unlisted artifact satisfies the check's summary
(e.g. a `pyproject.toml` where the list only named `requirements.txt`). The model still
may not assert a deterministic fact the script contradicts.

**Revisit if:** other delivery contexts are added (the script becomes a small
standalone CLI reused across them), or the check set grows enough to warrant the
declarative runner originally imagined for Phase 5.

## Open question — precision of a deterministic HIT (raised 2026-07-22)

Authoring `code-quality/paths-are-relative` (`no-absolute-paths`, now
`mode: deterministic`, severity **must-fix**) surfaced a gap. A regex has high recall
but imperfect precision: an absolute-path pattern also matches URLs, paths inside
comments, and placeholders like `"path/to/your/data"` — none of which are real
violations. For a **must-fix**, a false-positive hit is the worst case.

So: **does a deterministic hit get AI-confirmed before it is reported, or is the
script's verdict final?**

- The `decisions/0008` refinement only covers a script **miss** (→ escalate to AI). It
  does not say what happens to a **hit** on an `absent`/violation check — whether the
  AI filters it, or it is reported as-is.
- Two ways to close it: (a) the Phase 3 script pre-filters obvious non-violations
  (strip `http(s)://`, `s3://`; skip comment lines) and the AI report step reviews the
  rest; or (b) `mode` gains an explicit "deterministic-recall + AI-precision" shape for
  checks like this.

**To resolve at Phase 3 (deterministic-script build) and/or with the schema owner.**
Affects every `pass_when: absent` deterministic check whose pattern can match benign
text — absolute paths, and likely the committed-secrets regexes too.

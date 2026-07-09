# 0006 — Deterministic checks run from a pre-flight script, not LLM eyeballing

**Decision:** The `mode: deterministic` checks (file existence, absolute-path
regex, unpinned-versions, committed-secret patterns, `.gitignore` presence, …) run
from a **small pre-flight script** that emits **JSON facts**. The skill feeds that
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

**Revisit if:** other delivery contexts are added (the script becomes a small
standalone CLI reused across them), or the check set grows enough to warrant the
declarative runner originally imagined for Phase 5.

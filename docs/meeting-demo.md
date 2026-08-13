# Meeting demo and feedback guide

This demo is about the **pipeline**, not agreement on the final criteria. The current
4 criteria / 11 checks are deliberately a small vertical slice.

Use the [presentation walkthrough](presentation-walkthrough.md) as the main meeting
narrative. This document contains the shorter demo timings and feedback checklist.

## Before the meeting

```text
python -m pip install -r requirements-dev.txt
python tools/dev_check.py --version 0.1.0-demo --fixture all
```

For first-time setup and the shared fixture expectations, follow
[How to test repo-reviewer](how-to-test.md).

Zip `build/repo-reviewer/` if colleagues should test without cloning the development
repository.

## Suggested 25-minute walkthrough

1. **3 minutes — product boundary:** publication-readiness; no code execution, score,
   badge, or automatic fixes.
2. **5 minutes — source of truth:** open one file in `criteria/`, rebuild, and show
   where its checks appear in the generated `SKILL.md`.
3. **7 minutes — agentic run:** review a small repository through Claude Code, Codex,
   or Copilot and inspect `REVIEW.md`.
4. **5 minutes — optional second agent:** run the same review through another agentic
   tool and compare check states and evidence rather than prose style.
5. **5 minutes — decide what to learn next:** collect false positives, false negatives,
   unclear applicability, and missing evidence patterns. Do not spend meeting time on
   differences in prose style.

## What each tester should record

| Field | Example |
|---|---|
| Repository | `owner/name` or local fixture name |
| Expected quality | good / mixed / intentionally incomplete |
| Tool and model | Claude Code / model ID |
| Access mode | filesystem + shell |
| Criteria version | `0.1.0-demo` |
| Unexpected pass | criterion/check and why |
| Unexpected failure | criterion/check and why |
| Unclear or unstable result | criterion/check and what varied |
| Missing criterion | problem the reviewer was not allowed to report |

Write expected problems down **before** running the reviewer. This prevents the team
from retrofitting expectations to whatever an AI happened to say.

## Questions worth deciding tomorrow

- Which checks are genuinely `must-fix`, and can the team give one boundary example
  for each severity?
- Which checks apply only to analysis repositories, packages, repositories containing
  data, or repositories with restricted data?
- Which checks can be decided mechanically, which produce only candidates for AI
  confirmation, and which require AI judgment from the start?
- Does the repository evidence collector give the AI enough reliable facts without
  duplicating judgment-based checks?

Defer upload-only web-chat support, website design, scores, badges, CI integration,
and broad criterion expansion until this small pipeline has been run against several
real repositories.

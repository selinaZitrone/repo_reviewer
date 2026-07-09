# 0004 — The report is a single REVIEW.md; nothing else is changed

**Decision:** The tool writes one file, `REVIEW.md`, at the repository root,
overwritten each run. It makes **no other change** to the repository — it does
not fix issues or generate files (no CITATION.cff, no .gitignore) in v1.

**Guards:**
- The first line of `REVIEW.md` is a delete-before-publishing notice — otherwise
  it risks being committed and archived to Zenodo, so the published compendium
  would ship a document listing its own defects.
- The tool offers to add `REVIEW.md` to `.gitignore`.

**Why:** Writing into the repo is the least surprising place a scientist looks,
and it matches the team's instinct. Auto-remediation is deferred: generating
files is a bigger surface (correctness, overwriting user content) and v1 is about
proving the *criteria*, not fixing repos.

**Deliberately deferred:** a JSON sidecar report. Instead, give `REVIEW.md`
stable headings and stable finding ids so a JSON emitter is a small later addition
(needed when the GitHub Action wants machine-readable output).

**Revisit if:** users ask for auto-fix (opt-in, per-finding), or the Action needs
JSON.

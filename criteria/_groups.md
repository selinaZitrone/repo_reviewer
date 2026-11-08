# Criterion groups

Eight groups. Each is simultaneously a **report section**, a **website nav
entry**, and a **unit of authoring work** (one owner per group → no merge
conflicts, no overlap arguments).

Groups are named for **artifacts**, not virtues. (The old "Professionality"
group is dissolved — a group named for a virtue attracts junk criteria. Typos and
markdown usage fold into README quality under `structure`.)

## Tie-breaker rule: what is the reader *doing* when they notice it?

When a criterion could plausibly sit in two groups, place it by the **reader
activity that surfaces it** — because a group is a report section, and the
question is really "under which heading would a reader expect this finding?"

- noticed by **looking at the file tree** (no file opened) → `structure`
- noticed by **reading the code for style/clarity** → `code-quality`
- noticed by **asking "would this re-run and give the same result?"** →
  `reproducibility`
- noticed by **looking at data files** → `data`

Worked example — "structure" is two different concerns, and the rule splits them:

- **File & folder structure** (conventional layout, navigable folders, filenames
  that reveal what's where) — seen from the tree → **`structure`**.
- **Code structure** (modularity, functions vs. copy-paste, organisation within
  and between scripts) — seen by reading code → **`code-quality`**.

## The eight groups

Numbered in **working order**: the order in which an author typically prepares a
repository for publication (change content first, document it last, licence and
archive right before release). This order sets the report sections and the website
nav; it is mirrored by `GROUP_ORDER` in `tools/compile_skill.py`. Urgent blockers from
any group are surfaced separately in the report's "Do this first" digest.

| # | Group (`group:` value) | Covers | Reconciles from old notes |
|---|---|---|---|
| 1 | `data` | availability statement; codebook/data dictionary; formats; **raw vs. derived separation**; **sensitive-data flag** | Example Data, (parts of Reproducibility) |
| 2 | `code-quality` | **code structure** (modularity, functions vs. copy-paste, organisation within & between scripts); meaningful **variable/function** names; comments explain *why* | Code Quality, Naming/Structure (code level); formerly `code-analysis`, minus the run-it-again items now in `reproducibility` |
| 3 | `reproducibility` | no absolute paths / `setwd()` (runs from a fresh clone); **seeds set** (reproducible randomness); **run order** documented/discoverable; deterministic outputs | (new) — the run-it-again items pulled out of old `code-analysis` |
| 4 | `environment` | dependencies recorded with **versions**; container; language version; OS notes | Environment/System/Installation |
| 5 | `repository-hygiene` | no generated junk/outputs; **no secrets present**; sensible size | (new — thin in old notes) |
| 6 | `structure` | README exists + is informative; states what/why/how; entry point; how to run; contact; **file & folder structure** (conventional layout, navigable); **file/folder names reveal content & flow**; typos & markdown quality | README, Professionality, Naming/Structure (file level); formerly `orientation` |
| 7 | `licensing-citation` | code LICENSE (present + suitable); data licence; CITATION.cff / how to cite | Licence |
| 8 | `archive-release` | deposit on Zenodo/domain repo; DOI; tagged/versioned release; "ask a colleague to run it" | (new) — mostly `mode: none` checks; formerly `archiving-release` |

## Notes for authors

- **`data`** and **`repository-hygiene`** are the thinnest in our
  existing notes and the richest in the sources — prioritise them.
- **`data` cross-discipline rule:** the criterion is "the data situation is
  **unambiguous**" (present, OR a statement of where/how to get it and under what
  access terms, OR synthetic data + regeneration code) — never "data is present."
  Psychology/medicine data often cannot be shared; a naive "no data → fail" makes
  the tool useless to them.
- **`data` sensitive-data flag:** inspect filenames, directory listings, and
  column headers only — never cell values. Emit a *flag* ("verify this is
  intended for publication"), never a verdict.
- **`code-quality` vs `reproducibility` boundary:** code-quality
  is "is the code *well-written* — readable, modular, well-named?"; reproducibility
  is "would it *re-run and give the same result* — relative paths, seeds, run
  order?". A reader notices the first by judging style and the second by asking
  whether they could reproduce the output. This split is **provisional** — confirm
  it (and who owns `reproducibility`) at the meeting.
- **`reproducibility` name vs positioning (`decisions/0003`):** the group is
  reproducibility-*supporting practices* the tool can see statically (seeds,
  relative paths, run order) — **not** "does it reproduce when executed", which we
  deliberately do not check. Keep the report wording careful so the group name does
  not overclaim.
- **`archive-release` is almost entirely `mode: none` checks.** These render on the website
  and in the report's "Before you publish" list (right after "Do this first"). Do **not** write AI-checkable
  checks here — the tool cannot see a Zenodo deposit. "Ask a colleague unfamiliar
  with the tool to run it" is Nature's own recommendation (cite
  `nature-code-guidelines`).
- **Each criterion carries 1–N `checks`** (see `_schema.md`); a group's report
  section lists all its checks as `✓`/`✗`/`?` lines. `mode` and `severity` live on
  the check, not the criterion.

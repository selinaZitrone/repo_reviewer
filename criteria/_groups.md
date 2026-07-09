# Criterion groups

Seven groups. Each is simultaneously a **report section**, a **website nav
entry**, and a **unit of authoring work** (one owner per group → no merge
conflicts, no overlap arguments).

Groups are named for **artifacts**, not virtues. (The old "Professionality"
group is dissolved — a group named for a virtue attracts junk criteria. Typos and
markdown usage fold into README quality under `orientation`.)

## Tie-breaker rule: what is the reader *doing* when they notice it?

When a criterion could plausibly sit in two groups, place it by the **reader
activity that surfaces it** — because a group is a report section, and the
question is really "under which heading would a reader expect this finding?"

- noticed by **looking at the file tree** (no file opened) → `orientation`
- noticed by **reading the code** → `code-analysis`
- noticed by **looking at data files** → `data`

Worked example — "structure" is two different criteria, and the rule splits them:

- **File & folder structure** (conventional layout, navigable folders, filenames
  that reveal what's where) — seen from the tree → **`orientation`**.
- **Code structure** (modularity, functions vs. copy-paste, organisation within
  and between scripts) — seen by reading code → **`code-analysis`**.

| # | Group (`group:` value) | Covers | Reconciles from old notes |
|---|---|---|---|
| 1 | `orientation` | README exists + is informative; states what/why/how; entry point; how to run; contact; **file & folder structure** (conventional layout, navigable); **file/folder names reveal content & flow**; typos & markdown quality | README, Professionality, Naming/Structure (file level) |
| 2 | `licensing-citation` | code LICENSE (present + suitable); data licence; CITATION.cff / how to cite | Licence |
| 3 | `data` | availability statement; codebook/data dictionary; formats; **raw vs. derived separation**; **sensitive-data flag** | Example Data, (parts of Reproducibility) |
| 4 | `code-analysis` | **code structure** (modularity, functions vs. copy-paste, organisation within & between scripts); meaningful **variable/function** names; no absolute paths / `setwd()`; seeds set; comments explain *why*; run order documented/discoverable | Code Quality, Naming/Structure (code level), Reproducibility (non-execution parts) |
| 5 | `environment` | dependencies recorded with **versions**; container; language version; OS notes | Environment/System/Installation |
| 6 | `repository-hygiene` | `.gitignore`; no committed junk/outputs; **no committed secrets**; sensible size | (new — thin in old notes) |
| 7 | `archiving-release` | deposit on Zenodo/domain repo; DOI; tagged/versioned release; "ask a colleague to run it" | (new) — mostly `mode: none` checks |

## Notes for authors

- **Group 3 (data)** and **group 6 (repository-hygiene)** are the thinnest in our
  existing notes and the richest in the sources — prioritise them.
- **Group 3 cross-discipline rule:** the criterion is "the data situation is
  **unambiguous**" (present, OR a statement of where/how to get it and under what
  access terms, OR synthetic data + regeneration code) — never "data is present."
  Psychology/medicine data often cannot be shared; a naive "no data → fail" makes
  the tool useless to them.
- **Group 3 sensitive-data flag:** inspect filenames, directory listings, and
  column headers only — never cell values. Emit a *flag* ("verify this is
  intended for publication"), never a verdict.
- **Group 7 is almost entirely `mode: none` checks.** These render on the website
  and in the report's closing post-review checklist. Do **not** write AI-checkable
  checks here — the tool cannot see a Zenodo deposit. "Ask a colleague unfamiliar
  with the tool to run it" is Nature's own recommendation (cite
  `nature-code-guidelines`).
- **Each criterion carries 1–N `checks`** (see `_schema.md`); a group's report
  section lists all its checks as `✓`/`✗`/`?` lines. `mode` and `severity` live on
  the check, not the criterion.

> ⚠️ Delete this file before publishing / archiving the repository — it lists the
> repo's own open issues and is not meant to ship. (Add REVIEW.md to .gitignore.)
>
> _(Prototype run: written into the repo-reviewer repo for review, not into
> `sDiv/scales_3d`, at your request.)_

# Repository review — `sDiv/scales_3d`

_Context: Claude Code (agentic, filesystem)._ _Checks reviewability and completeness —
it does NOT run the code and does NOT verify the analysis reproduces._

**What I understood this repo to be:** an R research compendium — a staged analysis
pipeline (`R/01_prepare` → `R/05_analysis`, driven by `R/make.R`) that computes
taxonomic, phylogenetic and functional plant-diversity metrics across spatial scales,
including trait gap-filling and Bayesian models, and produces the manuscript figures.

_Reviewed against the prototype criteria set — 4 criteria / 11 checks (orientation,
licensing, environment, hygiene); other groups are not authored yet._

_Legend: ✅ pass · ❌ needs fixing · ⚠️ couldn't verify · ➖ not applicable_

## Do this first

1. **Add a LICENSE file** with the full licence text at the repo root — an OSI-approved
   licence (e.g. MIT or Apache-2.0). Without it the code is all-rights-reserved and
   nobody may legally reuse it.

2. **Record the environment:** run `renv::snapshot()` and commit `renv.lock`. The
   pipeline uses many R packages (BHPMF, a Bayesian modelling stack, …) but nothing
   records them or their versions.

## Checklist

### Orientation & README

❌ The README explains how to run or reproduce the analysis (should-fix) — the README describes what each script does but never says how to run the pipeline; point it at the entry point (`R/make.R` exists and is the runner, but the README doesn't mention it).

❌ The README's description of files and folders matches the actual repository (should-fix) — the README is out of date: it describes `R/02_cookie_cutting/` (the folder is `R/02_calculate_diversity/`), `01_add_different_taxonomies.R` (the script is `01_prepare_database.R`), and figures `Figure1_all_scales.R` / `Figure2_alpha_gamma.R` / `Figure3_ranks.R` (the scripts are `Fig1_all_scales_models.R` / `Fig2_slopes.R` / `Fig3_alpha_gamma.R`). Update it to match, or describe folders rather than individual files.

✅ A README exists at the repository root

✅ The README says what the project is and why it exists

### Licensing & citation

❌ A licence file (or full licence text) exists (must-fix) — add a `LICENSE` file with the full text at the repo root.

❌ Included data carries its own licence (should-fix) — add a data licence (e.g. `LICENSE-data`, CC-BY-4.0); also check the redistribution terms of the bundled third-party datasets (TRY, GRooT, EIVE), which may restrict re-sharing.

➖ The code licence is a recognised (OSI-approved) licence — not applicable: no licence present to assess.

### Environment & dependencies

❌ A dependency/environment record exists (must-fix) — run `renv::snapshot()` and commit `renv.lock`.

❌ The language version itself is recorded (should-fix) — record the R version (`renv.lock` captures it, or note it in the README).

➖ Dependencies are pinned to exact versions — not applicable: no dependency record to assess.

### Repository hygiene

✅ No secrets or credentials are committed

## Before you publish (we can't check these)

_No such checks in the prototype set yet — the `archiving-release` group (Zenodo/DOI,
tagged release, "ask a colleague unfamiliar with the tool to run it") is not authored._

---
_Checks passing: 3 of 9 applicable._  <!-- factual count only; never a score, grade, or badge -->
_criteria 0.1.0 (compiled 2026-07-09) · model: claude-opus-4-8 · date: 2026-07-09_

# Sources

The criteria are **adopted and reconciled** from established community standards,
not invented. Every criterion cites at least one source id from this table in its
`sources:` field. A criterion with no upstream source is our own contribution and
must be marked as such and justified in its body.

Use the **id** (left column) in frontmatter.

| id | Source | What it feeds | Notes |
|---|---|---|---|
| `fair4rs` | FAIR Principles for Research Software (Chue Hong et al., 2022, RDA) | licensing-citation, environment, archiving-release | The FAIR-for-software backbone. |
| `fair-software-eu` | fair-software.eu five recommendations (NL eScience Center & DANS); tool: `howfairis` | licensing-citation, archiving-release, orientation | Repository, License, Registry, Citation, Checklist. Deterministic & badge-based — note we deliberately don't badge (`decisions/0001`). |
| `turing-way-compendia` | The Turing Way — "Research Compendia" | data, code-analysis, environment | 3 principles + read-only / human-generated / project-generated file trichotomy → the raw/derived separation criterion. |
| `marwick-2018` | Marwick, Boettiger & Mullen (2018), "Packaging Data Analytical Work Reproducibly Using R (and Friends)", *Am. Statistician* 72(1) | code-analysis, environment, data | Conventional folder structure; data/methods/output separated; environment specified. |
| `wilson-2017` | Wilson et al. (2017), "Good Enough Practices in Scientific Computing", *PLOS Comp Biol* | code-analysis, data, repository-hygiene | Pragmatic, discipline-neutral baseline. |
| `nature-code-guidelines` | Nature, "Guidelines for authors submitting code & software" | orientation, environment, licensing-citation, archiving-release | 6 items incl. install instructions (OS/lang/deps/hardware/time), demo on sample data + runtime, DOI, OSI licence, **"ask an unfamiliar colleague to test it"** → post-review checklist. Screenshot to be added to `research/`. |
| `ropensci-devguide` | rOpenSci Packages: Development, Maintenance, and Peer Review | code-analysis, orientation | Code-quality & documentation vocabulary. |
| `acm-ctuning` | ACM / cTuning Artifact Review & Badging checklist | archiving-release, severity calibration | Available / Evaluated / Reusable tiers help calibrate must-fix vs should-fix. |
| `codecheck` | Nüst & Eglen (2021), CODECHECK, *F1000Research* | (scope boundary) | Cite as what we deliberately are **not** doing (execution). Sharpens positioning — `decisions/0003`. |
| `cookiecutter-ds` | Cookiecutter Data Science (DrivenData) | code-analysis | Concrete folder-structure reference. |
| `nature-s44271` | Nature Comms Psychology, code-structure article (`s44271-025-00236-3`) | code-analysis, orientation | Team-sourced structure reference. |

## Coverage sanity check (each group has upstream backing)

- **orientation** → nature-code-guidelines, ropensci-devguide, fair-software-eu
- **licensing-citation** → fair4rs, fair-software-eu, nature-code-guidelines
- **data** → turing-way-compendia, wilson-2017, marwick-2018 (+ our own sensitive-data flag)
- **code-analysis** → marwick-2018, wilson-2017, ropensci-devguide, cookiecutter-ds, nature-s44271
- **environment** → fair4rs, turing-way-compendia, marwick-2018, nature-code-guidelines
- **repository-hygiene** → wilson-2017 (+ largely our own; secrets scanning is not in the FAIR checklists — a genuine contribution)
- **archiving-release** → fair4rs, fair-software-eu, acm-ctuning, nature-code-guidelines

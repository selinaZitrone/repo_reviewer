# repo-reviewer development plan

`repo-reviewer` reviews scientific data-analysis repositories before publication and
returns a prioritised, evidence-backed checklist of what to improve.

Status: **ready for collaborator testing**. The co-author worksheet has been imported
into 27 criterion files containing 58 checks. These criteria are still proposals and
need validation and team review before a public release.

## 1. Product boundary

The tool is an author-facing publication-readiness and reviewability reviewer. It asks
whether a competent stranger could understand, trust, and reuse the repository.

Version 1 deliberately does not:

- execute a reviewed repository's code or claim the analysis reproduces;
- assign a score, grade, or badge;
- modify the reviewed repository except to write `REVIEW.md`;
- require Git or assume that the repository will be shared through GitHub;
- support upload-only web chats without filesystem and shell access.

The rationale for these boundaries is recorded in `decisions/`.

## 2. Architecture

Criteria are the source of truth. Each `criteria/<group>/<id>.md` file contains YAML
frontmatter for the generated reviewer and prose for a future website.

Each criterion contains one or more independently reported checks. A check defines:

- a stable kebab-case ID;
- a mode: `deterministic`, `ai`, or `none`;
- a severity: `must-fix`, `should-fix`, or `polish`;
- a one-line summary of the good state;
- ordered evidence examples when applicable.

The pipeline is:

```text
criteria/ ──> compiler ──> generated Agent Skill
                              │
target repository ──> evidence collector + AI judgment ──> REVIEW.md
```

`tools/compile_skill.py` validates the criterion schema and generates the shared skill.
`tools/collect_repository_evidence.py` produces facts for every deterministic check.
The compiler test enforces that these two sets remain aligned.

The generated bundle uses the open Agent Skills format and is tested through Claude
Code, Codex, and GitHub Copilot. Tool-specific folders are installation adapters; the
criteria and review logic are not maintained separately.

## 3. Current repository structure

| Path | Responsibility |
|---|---|
| `criteria/` | Criterion source files, schema, taxonomy, sources, template, and backlog |
| `tools/` | Compiler, collector, development check, and local skill-link helper |
| `tests/` | Unit tests and controlled manual-review fixtures |
| `decisions/` | Stable product and architecture decisions |
| `CONTRIBUTING.md` | Contributor, IDE, AI-agent, and testing setup |
| `AGENTS.md` / `CLAUDE.md` | Shared instructions for coding agents |
| `build/` | Generated disposable output; ignored by Git |

## 4. Completed work

- [x] Define the checks-based schema, group taxonomy, severity model, and report shape.
- [x] Establish a source registry and initial decision records.
- [x] Implement the compiler, read-only evidence collector, development command, and
  controlled fixture suite.
- [x] Generate one skill that can be installed in Claude Code, Codex, and GitHub
  Copilot.
- [x] Convert the collaborator worksheet into canonical criterion files.
- [x] Add schema validation and require collector coverage for all deterministic
  checks.
- [x] Consolidate setup and test instructions for co-authors.

## 5. Next phase: collaborator testing

### First pass

1. Each contributor follows `CONTRIBUTING.md` from a fresh clone.
2. Run all controlled fixtures with at least two AI tools where practical.
3. Record expected findings before each run.
4. Compare states, evidence, severity, and applicability; ignore harmless prose
   differences.
5. File false positives, false negatives, unstable judgments, and missing evidence
   patterns by criterion/check ID.

### Development corpus

Split real repositories into a development set and a held-out set. Iterate freely on
the development set; use the held-out set only after the criteria and prompt have
stabilised enough for an honest final check.

The candidate corpus from the initial planning work includes:

- intentionally difficult: `NSBLab/DiCER`, `bernardng/codeSync`;
- stronger examples: `PriorLabs/TabPFN`, `lciernik/attentive-layer-fusion`,
  `lciernik/similarity_consistency`, `MICA-MNI/micaflow`,
  `rasbt/LLMs-from-scratch`, `neuropsychology/psycho.R`,
  `corneliushennch/prethod_data_wrangling`, and `moritzknolle/leakoscope`.

Expand this to roughly 15–20 labelled repositories and include R, Python, MATLAB or
other languages, restricted-data cases, no-data software packages, and repositories
with synthetic data.

### What to learn

- Is every finding true and supported by a path, line, or named missing artifact?
- Are must-fix items genuinely blocking reuse?
- Do conditional checks become not-applicable in the right repositories?
- Does a genuinely strong repository receive a clean result without invented issues?
- Which valid artifacts are missing from the evidence lists or collector patterns?
- Which real problems cannot map to an existing criterion?

Add common unlisted evidence to the relevant criterion. A useful problem outside the
set becomes a proposed criterion with a source and rationale; the shipped reviewer must
not invent findings outside the defined set.

## 6. Decisions to make during testing

The detailed list lives in `criteria/_backlog.md`. The most important current issue is
the lack of an advisory state for possible sensitive data and large or unused files.
Sensitive-data inspection must remain limited to filenames, directory listings, and
column headers; it must never read or reproduce cell values or issue an unsupported
verdict.

The team should also review:

- severities and conditional applicability across all imported checks;
- overlap between README orientation, rerun instructions, and folder documentation;
- whether simulated data is a criterion or guidance;
- whether manuscript and archive tasks belong in the website checklist;
- one owner for schema/compiler/report consistency and one reviewer for consistent
  interpretation of AI checks.

## 7. Later work

After validation, build the Quarto website directly from criterion files and prepare a
versioned release. Only then consider upload-only workflows, CI/GitHub Action support,
a JSON report format, broader deterministic checks, or plugin packaging.

The website is intentionally deferred: validation will change the criteria, and their
prose should be polished once rather than rewritten around an untested set.

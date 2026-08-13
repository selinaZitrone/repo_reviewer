# repo-reviewer — Development Plan

> A tool that reviews a scientific data-analysis repository **before publication**
> and returns an actionable, prioritised report of what to improve.
> Author-facing, pre-publication, language-agnostic, runs inside the researcher's
> own agentic coding tool (Claude Code, Codex, GitHub Copilot, …).

Status: **working prototype**. The agentic pipeline is implemented with four
criteria / 11 checks. The criteria and report model remain proposals for the
team to review.

---

## 1. What it is (and is not)

**Is:** a *publication-readiness / reviewability* reviewer. It reads a repository
and reports, by priority, what a scientist should improve so that a competent
stranger could understand, trust, and reuse the work.

**Is not** (v1 non-goals — see `decisions/`):

- **Not a reproducibility checker.** It does **not execute code** and does not
  claim the analysis runs or reproduces. In the literature "reproducibility
  assessment" means execution (CODECHECK, Reproscreener, ARA); we deliberately
  do something else and must not use that word for it. → `decisions/0003`
- **No score or badge.** Severity-tiered, evidence-backed findings only.
  → `decisions/0001`
- **Does not modify the repository** beyond writing one `REVIEW.md`.
  It does not fix or generate files for the user in v1. → `decisions/0004`
- **Not a package to install.** v1 rides on the AI tool's own filesystem/shell.

### The prior-art gap we fill

The prior-art sweep found **no
author-facing, pre-publication, whole-repository, LLM-based reviewer.**
Everything LLM-based faces *reviewers* or *meta-scientists* and reviews *papers*
(ARA, Reproscreener, RECAP). Everything author-facing is deterministic-only and
either R-specific or metadata-shallow (`howfairis`, `pkgcheck`, `goodpractice`).
Our closest predecessor, `ropenscilabs/checkers`, was deterministic + R-only and
was **abandoned in 2022** — evidence that mechanical checks alone have a low
ceiling. The LLM judgment layer is what makes this worth doing. **The value we
lead with is not the LLM but the curated, citable criteria set that constrains it
into a rigorous auditor** — the skill's system prompt says, in effect, "you may
only flag a violation that maps to a defined criterion, and every finding must
cite its check id and file-path evidence."

---

## 2. The core architectural idea

**Criteria are the single source of truth.** Everything else — the AI skill, the
Quarto website, any future CLI or GitHub Action — is *generated or projected*
from one criteria set. Hand-maintaining the website and the skill separately
guarantees drift; deriving both from one record guarantees they agree.

Every criterion is one markdown file with a small YAML frontmatter (structured,
machine-facing) and a prose body (human-facing). The **planned website is a superset**
that renders every field; the **AI adapter** renders only the checkable subset.
Neither audience reads text written for the other.

### The three-way split (drives what runs where)

Each **check** carries a `mode` (not each criterion — see §3 and
`criteria/_schema.md`):

| Mode | Verified by | Example |
|---|---|---|
| **deterministic** | file/glob/regex checks, run from a script | Root README or licence present? Dependency/environment record present? Possible secret indicators? |
| **ai** | LLM judgment over content | Is the README actually informative? Can a stranger tell which script makes Fig. 3? |
| **none** | not verifiable from the repo | Deposit on Zenodo, get a DOI, ask a colleague to run it |

`mode: none` checks live on the **website** and in the report's **closing
post-review checklist** — the tool never nags about them.

### Delivery: one skill for agentic tools

v1 targets the open **Agent Skills** format rather than one vendor. The same generated
skill can be packaged for Claude Code, Codex, and supported GitHub Copilot agent
surfaces. Tool-specific folders are installation adapters only; criteria and review
rules are never maintained separately. → `decisions/0010`

v1 requires an **agentic/filesystem** context in which the AI can run the read-only
repository evidence collector, inspect files, and write `REVIEW.md`. Upload-only web
chats and CI / GitHub Action integration are deferred until the core review pipeline
and criteria have been validated.

**Deterministic checks run from a small script, not the LLM's own eyeballing.**
The current repository evidence collector emits JSON facts for four prototype
checks: a root README, a root licence, a dependency/environment record, and
possible secret indicators. The model may assert a deterministic fact
(e.g. "no LICENSE file") **only** from this JSON — it never decides file existence
itself, because LLMs hallucinate file *absence*. The script analyses files only;
it does **not** run the repository's code (`decisions/0002`, `decisions/0006`).
Pulled forward from Phase 5 because it is what makes the demo reliable.

---

## 3. Criteria model (summary — full spec in `criteria/_schema.md`)

- **One criterion = one checklist item, made of 1–N checks.** A criterion is a
  container; each *check* under it is an independently reportable pass/fail with
  its own `mode` and `severity`. So "a LICENSE is present" and "the licence is
  suitable" are **two checks of one criterion** — reported as two lines, not two
  criteria. Keeps the set from exploding while giving per-finding traceability.
  (Replaces the old "one criterion = one finding".)
- **`mode` and `severity` live on the check.** `mode`: `deterministic` (a script
  decides) / `ai` (judgment) / `none` (not checkable from the repo). This retires
  the "is the whole criterion hybrid?" question: a criterion isn't hybrid, it just
  has a deterministic "present?" check and an `ai` "suitable?" check.
- **Severity:** `must-fix` / `should-fix` / `polish` (replaces the old
  `minimal`/`advanced`). "The minimal standard" = the set of `must-fix` checks,
  rendered as a website section — derived, not stored.
- **Every finding carries evidence** (a path, a line, or a named missing
  artifact). No evidence → no finding — the anti-confabulation rule. For
  `mode: deterministic` checks the evidence is the script's JSON; the model may
  assert such a fact **only** from that JSON, never from its own file-reading.
- **The report is a fixed checklist, not a list of complaints.** Every check
  renders as `✓` pass / `✗` fail / `?` couldn't-verify, grouped by criterion,
  behind a short **priority digest** of the open `must-fix` `✗`s at the top. A
  fixed item set means re-runs can't "move the goalposts", green accumulates
  visibly, and false negatives are *marked* (`?`) rather than hidden. A factual
  count ("9 of 13 checks passing") is allowed; a score/grade/badge is not
  (`decisions/0001`, `decisions/0005`). Replaces progressive disclosure.
- **Language-agnostic criteria, language-specific evidence.** "The environment is
  captured" is one criterion; `renv.lock` / `requirements.txt` / `environment.yml`
  / `Dockerfile` are its checks' evidence packs (R / Python / any). MATLAB gets a
  thin pack (toolbox list, version) only where it differs; README-type criteria
  are language-neutral already.

---

## 4. Phases and ordering

Ordering rationale: **validation reshapes the criteria, so the website prose is
written after validation, not before** — otherwise you write it twice.

### Phase 0 — Prior-art sweep ✅
Landscape confirmed, gap confirmed, seven citable sources identified, closest
predecessor (and its failure mode) found. → feeds `criteria/_sources.md`.

### Phase 1 — Foundations ✅ (subject to team ratification)
- [x] Draft criterion file **schema** (checks-based), encoded and exemplified.
- [x] **Group taxonomy** (8 groups) = report sections = website nav = division of labour.
- [x] **Source table** — raw material, each criterion cites its provenance.
- [x] Four prototype **criteria** to test and revise.
- [x] `decisions/` records.

### Phase 2 — Criteria review and authoring (next, collaborative)
- One group per person; schema frozen *before* they start (no merge conflicts).
- Target a **tight, solid v1 set** — the essential criteria from the seven
  sources, not everything. Well-argued criteria beat exhaustive ones; no fixed
  count. The set grows later; the capped digest means set size never bloats the
  output.
- Fill `data` and `repository-hygiene` first — these are the thinnest in our
  existing notes and richest in the sources (codebook, data licence, raw/derived
  separation, sensitive-data flag, `.gitignore`, secrets).

### Phase 3 — Minimal testable pipeline ✅ (prototype complete)
- [x] A compiler validates criterion files and generates the shared skill.
- [x] A **repository evidence collector** emits JSON facts for the four current
  deterministic checks. It analyses files only and never runs repository code.
  → `decisions/0006`.
- [x] The **report instructions** encode the fixed `✓`/`✗`/`?` checklist, priority
  digest, evidence-required rule, version/model/date footer, and not-a-repro
  disclaimer. → `decisions/0005`.
- [x] The generated bundle can be installed in Claude Code, Codex, and supported
  GitHub Copilot agent surfaces.
- [x] Automated tests cover compilation, collection, and report instructions.

### Phase 4 — Validation on the development corpus
- Split the corpus: **dev set (~⅔, iterate freely)** vs **held-out set (touch
  once, at the end)**. Prevents overfitting the prompt to the corpus — the same
  error the tool exists to prevent. The split can be informal; just don't tune the
  prompt against the repos you'll demo live.
- **Lightweight, honest validation:** for each repo, write down the findings you
  *expect* **before** running the tool (a few bullets in `validation/<repo>.md`),
  then run and compare. Writing expectations first is the one discipline that
  matters — it stops you rationalising whatever the report happens to say. No
  automated assertion harness or per-criterion benchmark in v1 (defer to "if it
  catches on").
- Check findings are true, evidence-backed, and correctly severity-ranked; confirm
  a genuinely good repo comes back clean (all `✓`).
- **Harvest the long tail** (`decisions/0008`). Validation is where you learn what real
  repos actually do:
  - When a repo satisfies a check with an artifact we never listed (`pyproject.toml`,
    `setup.py`, …), **add it to that check's `evidence`**.
  - Run a **team-only "criteria discovery" pass** where the model *is* allowed to name
    problems no criterion covers. Promote each worthwhile candidate into a real
    criterion (source + rationale + fix). The shipped report never does this.
- **Iterate the criteria** here. Expect the criteria to change.

**Deferred criterion candidates** (agreed useful, held out of v1 pending validation):

- `no-unused-files` (**repository-hygiene** / code-quality / data) — flag data files
  that are read nowhere and code files that are never called. **Highest
  false-positive risk in the hygiene group:** usage detection needs whole-repo
  dataflow/call-graph reasoning, and legitimate cases break it (paths built at
  runtime, globs, entry-point scripts, example data provided for users). If shipped:
  `mode: ai`, severity `polish`, output as a **flag** ("these files don't appear to
  be referenced — confirm they're needed"), **⚠️ when unsure**, never a hard `✗`.
  Decide group placement (unused *code* → code-quality; stray *data* → data) at the
  meeting. Validate against real repos before committing it.
- `large-files-advisory` (**repository-hygiene**) — surface unusually large files
  (individual files over ~50 MB; large binaries, datasets, checkpoints) for the author
  to confirm. **Advisory only — a flag, never a `✗`**: large data is normal in science,
  so a hard "too big → fail" is a false positive. Deferred because it needs the report
  model to grow a dedicated **advisory/flag state** — the same gap the data group's
  sensitive-data flag hits (`decisions/0005` has only ✓/✗/⚠️/➖). When included, keep the
  host-limit hint (e.g. GitHub rejects files >100 MB) *without* assuming a specific host.

### Phase 5 — Website (Quarto) + release tooling (after validation)
- Quarto renders the criteria bodies directly; superset incl. `mode: none` checks.
- The website comes later, with prose written after Phase 4.
- Then, opportunistically: harden/expand the deterministic script, other delivery
  contexts (chat, GitHub Action / Tier C), JSON report emitter, other tool adapters.

---

## 5. Near-term milestones

### Collaborator meeting

- Ratify or revise the checks-based schema, taxonomy, severities, and report model.
- Demonstrate the current four-criterion pipeline on contrasting repositories.
- Agree group ownership and the contribution workflow.
- Expand and label the development corpus.

### After the meeting

- Incorporate the team's decisions into the schema and decision records.
- Author the first agreed criteria set collaboratively.
- Validate it on the development corpus before building the website.

Reality check: prototype-fast, short-duration, not-high-priority, four PhDs.
The plan is deliberately staged so the *criteria* (the durable, citable asset)
come first and the elegant machinery (runner, Action, adapters) is deferred until
it's earned.

---

## 6. Division of labour (Phase 2)

One group owner each; schema is frozen before authoring starts.

| Group | Owner | Notes |
|---|---|---|
| structure | | README, purpose, entry point, contact, file & folder structure/names |
| licensing-citation | Selina | LICENSE, data licence, CITATION.cff |
| data | | availability statement, codebook, raw/derived, **sensitive-data flag** |
| code-quality | Selina | code structure, modularity, naming, comments |
| environment | | dependencies + versions, container, language version |
| repository-hygiene | Selina | `.gitignore`, junk, **secrets**, size |
| archive-release | | Zenodo/DOI/tag — mostly `mode: none` checks, website + post-review only |
| reproducibility | | absolute paths / `setwd()`, seeds, run order, deterministic outputs |

Plus two **cross-cutting roles** (to prevent style/severity drift across groups —
the main risk of a per-group split): one owner for **schema + compile + report
template**; one for **`ai`-check consistency**, who reviews every `mode: ai` check
so "informative", "suitable", "unambiguous" mean the same thing everywhere.

---

## 7. Development corpus (from the team's good/bad list)

Most "good" repos are ML/methods repos or R packages, **not** classic research
compendia — valuable, because it forces scope detection rather than overfitting.

**Bad:** `NSBLab/DiCER` (usable code, poor for reuse) · `bernardng/codeSync`
(no README at all).
**Good:** `PriorLabs/TabPFN` (complex, good structure) · `lciernik/attentive-layer-fusion`
· `lciernik/similarity_consistency` · `MICA-MNI/micaflow` (rich: sys reqs, formats,
container) · `rasbt/LLMs-from-scratch` · `neuropsychology/psycho.R` (R package) ·
`corneliushennch/prethod_data_wrangling` · `moritzknolle/leakoscope`.

**To do at the meeting:** expand toward ~15–20; label each; note R/Python/other
and any restricted/no-data cases (critical for the data-availability criterion).

Reference structure sources: Cookiecutter Data Science; Nature Comms Psychology
code-structure article (`s44271-025-00236-3`).

---

## 8. Principles carried into implementation

- **Cross-discipline data rule.** Psychology/medicine data often *can't* be
  shared. The criterion is "the data situation is unambiguous" (present / stated
  where-and-how / synthetic + regeneration code), never "data is present."
  Baked into the `data` group from the start.
- **Sensitive-data flag, not finding (planned).** Read filenames + directory listings +
  column headers only — never cell values. Output: "verify this is intended for
  publication," never a verdict. Works in any file-reading tier.
- **Dogfooding as a scope test.** repo-reviewer reviews itself. Correct behaviour
  is to detect "this is a tool, not a compendium" and check only what applies —
  not to grind an inapplicable checklist. Passing report → README / lecture slide.
- **Self-describing reports.** Every report footer stamps criteria version
  (semver, just a string), model ID, and date. Cheap; non-negotiable for a tool
  about rigor.
- **Report can come back clean.** The skill explicitly permits all checks to pass;
  it does not require the model to invent findings.
- **Uncertain is visible, never silent.** A check the tool cannot decide renders
  as `?` ("couldn't verify"), never as a pass and never as an omission — false
  negatives are marked, not hidden.

---

## 9. Open questions to resolve at/after the meeting

1. **Ratify the checks-based schema** (§3, `criteria/_schema.md`) and the
   `✓`/`✗`/`?` checklist report model (`decisions/0005`) — both are proposals
   until the team agrees.
2. Expand + label the corpus to ~15–20; capture restricted-data cases.
3. Agree the two cross-cutting roles (schema/report owner, `ai`-check consistency
   owner) alongside the per-group owners (§6).
4. Decide the contribution path (issue template, criterion proposal format) —
   likely "if it catches on," not v1.
5. Add the Nature code checklist screenshot to `research/` for citation.

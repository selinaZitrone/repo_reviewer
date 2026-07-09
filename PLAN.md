# repo-reviewer — Development Plan

> A tool that reviews a scientific data-analysis repository **before publication**
> and returns an actionable, prioritised report of what to improve.
> Author-facing, pre-publication, language-agnostic, runs inside the researcher's
> own AI IDE (Claude Code, GitHub Copilot, Cursor, …).

Status: **planning**. This document is the shared plan for the team. It will be
sent for external AI review before implementation begins.

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

The prior-art sweep (see `research/sweep-notes.md` once written) found **no
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
machine-facing) and a prose body (human-facing). The **website is a superset**
that renders every field; the **AI adapter** renders only the checkable subset.
Neither audience reads text written for the other.

### The three-way split (drives what runs where)

Each **check** carries a `mode` (not each criterion — see §3 and
`criteria/_schema.md`):

| Mode | Verified by | Example |
|---|---|---|
| **deterministic** | file/glob/regex checks, run from a script | LICENSE exists? `renv.lock` present? absolute paths in scripts? committed secrets? |
| **ai** | LLM judgment over content | Is the README actually informative? Can a stranger tell which script makes Fig. 3? |
| **none** | not verifiable from the repo | Deposit on Zenodo, get a DOI, ask a colleague to run it |

`mode: none` checks live on the **website** and in the report's **closing
post-review checklist** — the tool never nags about them.

### Delivery: v1 is Claude Code only

v1 targets **one context: Claude Code** (agentic — filesystem + shell). Other
contexts are deferred until the skill is good; the criteria set is the portable
asset and the skill is a thin adapter, so porting later is cheap. The later ladder
(sketched, not built): plain chat / uploaded zip (LLM-only, degraded); CI / GitHub
Action (deterministic always, LLM optional). The report states which context it
ran in.

**Deterministic checks run from a small script, not the LLM's own eyeballing.**
A ~5-check pre-flight script (file-exists globs, absolute-path regex,
unpinned-versions, committed-secret patterns, `.gitignore` presence) emits JSON
*facts* the skill feeds to the model. The model may assert a deterministic fact
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

### Phase 0 — Prior-art sweep ✅ (done this session)
Landscape confirmed, gap confirmed, seven citable sources identified, closest
predecessor (and its failure mode) found. → feeds `criteria/_sources.md`.

### Phase 1 — Foundations (now → tomorrow's meeting)
The output of *this* planning session.
- [x] Criterion file **schema** (checks-based), frozen and exemplified.
- [x] **Group taxonomy** (7 groups) = report sections = website nav = division of labour.
- [x] **Source table** — raw material, each criterion cites its provenance.
- [x] Two complete **exemplar criteria** to copy, not a spec to interpret.
- [x] `decisions/` records.

### Phase 2 — Criteria authoring (collaborative, starts at/after meeting)
- One group per person; schema frozen *before* they start (no merge conflicts).
- Target a **tight, solid v1 set** — the essential criteria from the seven
  sources, not everything. Well-argued criteria beat exhaustive ones; no fixed
  count. The set grows later; the capped digest means set size never bloats the
  output.
- Fill `data` and `repository-hygiene` first — these are the thinnest in our
  existing notes and richest in the sources (codebook, data licence, raw/derived
  separation, sensitive-data flag, `.gitignore`, secrets).

### Phase 3 — Skill + report template + deterministic script (after criteria are roughed in)
- A compile step (~40-line script) concatenates AI-facing check fields → the skill.
- A small **deterministic pre-flight script** runs the ~5 mechanical checks and
  emits JSON *facts* the skill feeds to the model (pulled forward from Phase 5
  because it is what makes the demo reliable). Analyses files only; never runs the
  repo's code. → `decisions/0006`.
- The **report template** encodes: the fixed `✓`/`✗`/`?` checklist, the priority
  digest, the evidence-required rule, a **worked clean-report example** (all `✓`),
  the version/model/date footer, and the not-a-repro disclaimer. → `decisions/0005`.
- **Crude demo** can be assembled early (even for the meeting) to show
  collaborators what they're writing criteria *for* — the single most socially
  valuable artifact. Full skill waits for the criteria to exist.

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
- **Iterate the criteria** here. Expect the criteria to change.

### Phase 5 — Website (Quarto) + release tooling (after validation, post-lecture)
- Quarto renders the criteria bodies directly; superset incl. `mode: none` checks.
- **Not a lecture deliverable** — the lecture ships the README only; the website
  comes later, with prose written after Phase 4.
- Then, opportunistically: harden/expand the deterministic script, other delivery
  contexts (chat, GitHub Action / Tier C), JSON report emitter, other tool adapters.

---

## 5. Timeline anchors

- **T+16h — collaborator meeting.** Bring: schema (now checks-based — a proposal
  to ratify), taxonomy + division of labour, source table, exemplars, and (ideally)
  a crude demo run live against a no-README repo (dramatic) and one good repo.
  Website not needed.
- **T+7d — lecture.** Bring: working skill on the v1 criteria set, validated on the
  corpus, a live demo, dogfood result, and the tool's **README**. No website, no
  paper.

Reality check: prototype-fast, short-duration, not-high-priority, four PhDs.
The plan is deliberately staged so the *criteria* (the durable, citable asset)
come first and the elegant machinery (runner, Action, adapters) is deferred until
it's earned.

---

## 6. Division of labour (Phase 2)

One group owner each; schema is frozen before authoring starts.

| Group | Owner | Notes |
|---|---|---|
| orientation | | README, purpose, entry point, contact |
| licensing-citation | | LICENSE, data licence, CITATION.cff |
| data | | availability statement, codebook, raw/derived, **sensitive-data flag** |
| code-analysis | | structure, naming, absolute paths, seeds, comments, run order |
| environment | | dependencies + versions, container, language version |
| repository-hygiene | | `.gitignore`, junk, **secrets**, size |
| archiving-release | | Zenodo/DOI/tag — mostly `mode: none` checks, website + post-review only |

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
- **Sensitive-data flag, not finding.** Read filenames + directory listings +
  column headers only — never cell values. Output: "verify this is intended for
  publication," never a verdict. Works in any file-reading tier.
- **Dogfooding as a scope test.** repo-reviewer reviews itself. Correct behaviour
  is to detect "this is a tool, not a compendium" and check only what applies —
  not to grind an inapplicable checklist. Passing report → README / lecture slide.
- **Self-describing reports.** Every report footer stamps criteria version
  (semver, just a string), model ID, and date. Cheap; non-negotiable for a tool
  about rigor.
- **Report can come back clean.** The template shows the model a full clean
  example (all `✓`) so it doesn't infer that findings are expected.
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

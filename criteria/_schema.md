# Criterion file schema

One criterion = one markdown file. Frontmatter is structured and machine-facing;
the body is prose and human-facing. The website renders the body; the AI skill is
compiled from the frontmatter (the `checks`). **Neither audience reads the other's
text.**

## The one rule that governs everything

> **One criterion = one checklist item, made of 1–N checks.**
> A criterion is a *container*. Each **check** under it is an independently
> reportable pass/fail with its own `mode` and `severity`. "A LICENSE is present"
> and "the licence is suitable" are **two checks of one criterion** — reported as
> two lines, never two criteria.

This keeps the criteria set from exploding *and* gives per-finding traceability
(the old "one criterion = one finding" gave the first but not the second).

Rule of thumb for splitting into criteria vs checks:

- Different **artifact / section of the report** → different **criterion**.
- Same artifact, different **question about it** (present? suitable? pinned?) →
  different **check** of the same criterion.

## File location & id

```
criteria/<group>/<id>.md
```

- `<group>` is one of the seven groups in `_groups.md`.
- `<id>` is short, kebab-case, unique across all groups, and stable (it appears in
  reports and URLs — treat it as an API). e.g. `environment-captured`.
- Each **check** also has an `id`, unique *within its criterion* and likewise
  stable — it is the finding id in the report and in any later JSON. e.g.
  `env-file-present`.

## Frontmatter fields

```yaml
id: environment-captured          # required. kebab-case, unique, stable.
title: The computational environment is recorded   # required. human sentence.
group: environment                # required. one of the seven groups.
sources:                          # required. ids from _sources.md. >=1.
  - fair4rs
  - turing-way-compendia
checks:                           # required. one or more.
  - id: env-file-present          # required. kebab-case, unique within criterion.
    mode: deterministic           # required. deterministic | ai | none
    severity: must-fix            # required. must-fix | should-fix | polish
    summary: A dependency/environment record exists   # required. one line, human.
    # pass_when: present          # optional. present (default) | absent. See field notes.
    evidence:                     # required for deterministic; optional for ai; omit for none.
      r:      [renv.lock, "DESCRIPTION with Imports/Depends"]
      python: [requirements.txt, environment.yml]
      any:    [Dockerfile]
  - id: env-versions-pinned
    mode: deterministic
    severity: should-fix
    summary: Dependencies are pinned to exact versions, not just named
    evidence:
      python: ["requirements.txt using == (not >= or unpinned)"]
      r:      [renv.lock]
```

**Field notes**

- `mode` — how the check is verified. `deterministic` = a script decides
  (file/glob/regex), and its result is the JSON the skill trusts (the model may
  not contradict it or decide file existence itself — see `decisions/0006`).
  `ai` = needs judgment over content. `none` = not decidable from the repo
  (website + post-review checklist only, never a nagging finding). A criterion
  whose checks are all `mode: none` (most of `archiving-release`) omits `evidence`.
- `severity` — **per check**. Anchor definitions (use these when authoring):
  - **must-fix** — without this, a competent stranger cannot reuse the repo.
  - **should-fix** — reuse is possible but materially harder than necessary.
  - **polish** — everything else.
  All three render in the checklist; the report's priority **digest** leads with
  the open `must-fix` failures. There is no progressive hiding — see
  `decisions/0005`.
- `summary` — the one-line label the check shows as a `✅`/`❌`/`⚠️` line. Phrase it
  as the *good* state ("A licence file exists") so `✅` reads naturally — and, for
  `pass_when: absent` checks, so it names the target to fix toward.
- `pass_when` — **optional, default `present`.** `present` = the check passes when a
  satisfying piece of `evidence` is **found** (add-a-thing checks, the majority).
  `absent` = the check passes when the evidence is **not** found (remove-a-thing
  checks: committed secrets, absolute paths, committed junk). For `absent` checks the
  `evidence` list is the *violation patterns to search for*, and the fix is
  "remove/replace the flagged item" (the good state is the `summary`). Rule of thumb:
  if a check would make you say "good, I didn't find any…", it is `pass_when: absent`.
  Worked example: `criteria/repository-hygiene/no-committed-secrets.md`. → `decisions/0007`.
- `evidence` — machine-facing, terse. Keys: `r`, `python`, `any`, and other
  languages as needed (`matlab` only where it genuinely differs). Each entry is a
  concrete artifact or pattern the script/agent looks for. **Required for
  `deterministic` checks** (they decide purely from named artifacts). **Optional
  for `ai` checks** — a judgment like "is the licence OSI-approved?" reads content
  and cites its evidence (a path/line) at review time, so it often has none to
  pre-list. **Omit for `none`.**
  - **Order `evidence` best-first.** The list does double duty: it decides pass/fail
    *and* it is the source of the report's fix ("add/adopt the first entry that fits
    this repo"). Putting the recommended artifact first (e.g. `renv.lock` before
    `DESCRIPTION`) is how you get consistent, opinionated fixes across reports
    **without** a separate `fix` field. There is no `fix` field — the fix is derived
    from ordered evidence; detailed how-to prose lives in the body's *How to satisfy
    it* (rendered on the website), not in the report.
- Deliberately **excluded** (keep it lean): no `report_hint` (the report template
  handles phrasing globally), no `applies_to`/profiles (a v2 concern — conditional
  cases like "data licence only when data is present" go in the check's `summary`
  prose instead).

## Body headings (fixed order)

```markdown
## Why it matters
## How to satisfy it
## Examples        <!-- optional: include only when a concrete example helps -->
```

- **Why it matters** — the rationale a scientist reads on the website. Hand-written
  prose, no jargon. This is a credibility artifact; write it well.
- **How to satisfy it** — concrete, tool-specific instructions. Where relevant,
  give the R way and the Python way explicitly.
- **Examples** — "sufficient" vs "not sufficient", when it clarifies. Skip when it
  would be filler.

## Worked reference

`criteria/environment/environment-captured.md` and
`criteria/licensing-citation/license-present-and-suitable.md` are the two canonical
examples — each carries multiple checks across modes. **Copy one and adapt** — do
not write from this schema alone.

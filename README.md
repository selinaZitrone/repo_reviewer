# repo-reviewer

`repo-reviewer` is a publication-readiness reviewer for scientific data-analysis
repositories. It generates an evidence-backed `REVIEW.md` checklist that helps authors
improve a repository before publishing or archiving it.

The project is ready for collaborator testing. Its criteria remain a working draft:
testers should report false positives, false negatives, unclear applicability, and
missing criteria before the first release.

The reviewer reads repository files but never executes the repository's code. It does
not claim that an analysis reproduces, assign a score or badge, or modify the reviewed
repository beyond writing `REVIEW.md`.

## How it works

```text
criteria/<group>/<criterion>.md
                │
                ├── tools/compile_skill.py
                ▼
       build/repo-reviewer/          target repository
       ├── SKILL.md                         │
       ├── README.md                        ├── deterministic evidence
       └── scripts/collector                ├── AI judgments
                                            ▼
                                         REVIEW.md
```

The Markdown files under `criteria/` are the source of truth. The compiler validates
their schema and generates one tool-neutral [Agent Skills](https://agentskills.io/)
bundle. That bundle can be tested with Claude Code, Codex, and GitHub Copilot.

## Quick start for contributors

Requirements: Python 3.10 or newer.

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
python tools/dev_check.py
```

Activate `.venv` before the install on systems where `python` does not automatically
use it. The full Windows, macOS/Linux, VS Code, Claude Code, Codex, and GitHub Copilot
instructions are in [CONTRIBUTING.md](CONTRIBUTING.md).

`dev_check.py` runs the unit and deterministic fixture tests, validates all criterion
files, and builds the distributable skill under `build/repo-reviewer/`. The `build/`
directory is generated and ignored; never edit it by hand.

## Repository map

| Path | Purpose |
|---|---|
| `criteria/` | Canonical criteria plus schema, groups, sources, template, and backlog |
| `tools/` | Compiler, read-only evidence collector, development checks, and setup helper |
| `tests/` | Unit tests and safe manual-review fixtures |
| `decisions/` | Short records explaining settled product and architecture choices |
| `AGENTS.md` | Shared project instructions for Codex and supported Copilot surfaces |
| `CLAUDE.md` | Claude Code adapter importing the shared project instructions |
| `PLAN.md` | Current scope, milestones, and unresolved product decisions |

## Build and install the development skill

Build it:

```bash
python tools/dev_check.py
```

Preview and then create a user-level development link for one or more tools:

```bash
python tools/setup_dev_skill.py --dry-run codex
python tools/setup_dev_skill.py codex
```

Replace `codex` with `claude` or `copilot`, or pass several names. The helper refuses
to overwrite an existing installation. Open a fixture or target repository in the
chosen agent and ask:

```text
Use the repo-reviewer skill to review this repository before publication.
```

Explicit invocations are `$repo-reviewer` in Codex and `/repo-reviewer` in Claude Code
and GitHub Copilot. See [CONTRIBUTING.md](CONTRIBUTING.md) for tool-specific locations,
manual test procedure, and the feedback template.

## Add or edit criteria

Start with:

- [criterion schema](criteria/_schema.md);
- [group definitions](criteria/_groups.md);
- [authoring template](criteria/_authoring-template.md);
- [source registry](criteria/_sources.md);
- [open criteria questions](criteria/_backlog.md).

After changing a criterion, run `python tools/dev_check.py` and inspect its generated
section in `build/repo-reviewer/SKILL.md`. A deterministic check also requires a fact
in `tools/collect_repository_evidence.py`; the test suite checks this contract.

## Current testing focus

Use the controlled fixtures first, then a labelled development corpus of real
repositories. Write expected findings before each run and compare check states and
evidence rather than prose style. Keep held-out repositories untouched until the
criteria and instructions have stabilised.

The import from the collaborator worksheet is complete. The small set of obvious
issues intentionally deferred for team discussion is recorded in
`criteria/_backlog.md`.

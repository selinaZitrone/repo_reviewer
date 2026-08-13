# repo-reviewer

A publication-readiness reviewer for scientific data-analysis repositories. It
produces an evidence-backed `REVIEW.md` checklist of what to improve before a
repository is published or archived.

> **Prototype:** the pipeline currently contains 4 criteria / 11 checks. The
> criteria are intentionally incomplete while the team reviews them.

The tool reviews files without executing the repository's code. It does not claim
that an analysis reproduces, does not assign a score or badge, and does not modify
the repository except for writing `REVIEW.md` in an agentic run.

## How the prototype works

```text
criteria/*.md
     │
     ├── compile_skill.py ──> shared SKILL.md + evidence collector
     │
target repository
     │
     ├── collect_repository_evidence.py ──> deterministic facts (JSON)
     │                            │
     │                            ▼
     └──────────────────────> AI judgments ──> REVIEW.md
```

`criteria/` is the source of truth. The compiler projects those criteria into one
[open Agent Skills](https://agentskills.io/) bundle. The same `SKILL.md` format is
supported by [Claude Code](https://code.claude.com/docs/en/skills),
[Codex](https://learn.chatgpt.com/docs/build-skills), and current
[GitHub Copilot agent surfaces](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills).

This v1 requires an agentic tool with filesystem and shell access. The bundled
collector creates JSON facts; the AI reads those facts, inspects the repository for
judgment-based checks, and writes `REVIEW.md`. Upload-only web chats are deferred.

## Build and test

Requirements: Python 3.10+; PyYAML is needed only to compile criteria during
development.

```text
python -m pip install -r requirements-dev.txt
python tools/compile_skill.py --version 0.1.0
python -m unittest discover -s tests -v
```

The self-contained skill is generated at:

```text
build/repo-reviewer/
├── README.md
├── SKILL.md
└── scripts/
    └── collect_repository_evidence.py
```

`build/` is generated and ignored by git. For a release or meeting handout, zip the
`build/repo-reviewer/` directory after compiling it.

## Try it with an agentic tool

Copy the generated `repo-reviewer` directory into a skill location recognized by
your tool:

| Tool | User-level location | Project-level location |
|---|---|---|
| Claude Code | `~/.claude/skills/repo-reviewer/` | `.claude/skills/repo-reviewer/` |
| Codex | `~/.agents/skills/repo-reviewer/` | `.agents/skills/repo-reviewer/` |
| GitHub Copilot | `~/.agents/skills/repo-reviewer/` | `.github/skills/repo-reviewer/` or `.agents/skills/repo-reviewer/` |

Then open the repository to review and ask:

```text
Use the repo-reviewer skill to review this repository before publication.
```

Claude Code can also be invoked with `/repo-reviewer`, Codex with
`$repo-reviewer`, and Copilot CLI with `/repo-reviewer`. Exact invocation UI varies
by product; natural-language invocation works through the skill description.

Project-level installation adds skill files to the target working tree. Use a
user-level installation if the target repository must remain untouched apart from
the generated `REVIEW.md`.

## Modify a criterion

1. Copy one of the worked criteria under `criteria/`.
2. Keep its criterion and check IDs stable once published.
3. Recompile the skill.
4. Run the tests.
5. Inspect `build/repo-reviewer/SKILL.md` to confirm the check appears under the
   intended section.

See [criteria/_schema.md](criteria/_schema.md),
[criteria/_groups.md](criteria/_groups.md), and the
[criterion author template](docs/criterion-template-for-authors.md).

## Meeting demo

For a useful comparison, run the same compiled criteria against:

1. this repository (dogfooding);
2. a small repository with no README or licence;
3. one repository the team considers publication-ready;
4. optionally, two different agentic tools using the same compiled skill.

Compare individual check states and evidence, not writing style. Record the tool,
model, access mode, date, and criteria version for every run.

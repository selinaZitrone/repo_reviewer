# How to test repo-reviewer during development

This guide is for fast local iteration by contributors. It separates tests that
must be exact from AI reviews that require human judgment.

## What the test setup contains

```text
tests/
├── test_*.py                         automated unit and fixture tests
└── manual/
    ├── fixtures/                    small repositories given to the AI
    │   ├── 01-clear-failures/
    │   ├── 02-mixed/
    │   ├── 03-ready/
    │   └── 04-unconventional/
    ├── expected-deterministic.json  exact collector outcomes
    └── expectations.md              expected full-review behavior
```

The expectations are deliberately outside the fixture repositories. Do not show
them to the reviewing agent before it runs.

The fixtures are repository-shaped directories, not nested Git repositories. This
keeps the shared project simple while still giving the collector and AI realistic
files to inspect. Never place real credentials or sensitive research data in them.

## One-time contributor setup

From the `repo_reviewer` repository root:

```text
python -m pip install -r requirements-dev.txt
python tools/dev_check.py
```

`dev_check.py` runs the complete unit suite and compiles a development skill into
`build/repo-reviewer/`.

### Link the generated skill to an agent

First preview the user-level link for the tools you use:

```text
python tools/setup_dev_skill.py --dry-run codex
python tools/setup_dev_skill.py --dry-run claude
python tools/setup_dev_skill.py --dry-run copilot
```

Then create the required link, for example:

```text
python tools/setup_dev_skill.py codex
```

Multiple tools can be named in one command:

```text
python tools/setup_dev_skill.py codex claude copilot
```

Codex and Copilot share the open user-level location
`~/.agents/skills/repo-reviewer`; Claude Code uses
`~/.claude/skills/repo-reviewer`. On Windows the helper creates a directory
junction; on macOS and Linux it creates a symbolic link. It refuses to overwrite
anything already at a destination. If that happens, inspect and rename the old
folder yourself before retrying.

The link points at `build/repo-reviewer/`, so later compilations are immediately
visible without copying. Codex officially supports linked skill folders and detects
changes automatically; restart the agent if a change does not appear. See the
[Codex skill documentation](https://learn.chatgpt.com/docs/build-skills),
[Claude Code skill documentation](https://code.claude.com/docs/en/skills), and
[GitHub Copilot skill documentation](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills).

## Fast loop while editing

After changing criteria, the collector, compiler, or skill instructions, run:

```text
python tools/dev_check.py
```

This is the default inner loop:

```text
edit → unit tests and fixture assertions → compile → inspect the relevant output
```

The automated fixture test checks the exact four deterministic states for every
fixture. Most edits therefore do not need an AI run.

Use a full agent review when you change:

- criterion summaries, evidence, severity, or applicability;
- AI-review rules or report instructions;
- interactions between deterministic facts and AI judgment;
- anything intended for a demo or release.

## Run a manual agent review

Generate readable evidence snapshots if desired:

```text
python tools/dev_check.py --fixture all
```

They are written under `build/manual-evidence/` and are safe to discard.

Next, open exactly one fixture directory as the agent's workspace—for example:

```text
tests/manual/fixtures/02-mixed
```

Start a new agent conversation there and use the same prompt for every run:

```text
Use the repo-reviewer skill to review this repository before publication.
```

The agent should create only `REVIEW.md`. That filename is ignored by Git. Once the
run finishes, compare it with `tests/manual/expectations.md`. Check states and
evidence first; writing style is secondary.

To preserve a result for comparison, copy it to an ignored local directory such as:

```text
build/manual-results/02-mixed-codex.md
```

Then remove the fixture's `REVIEW.md` before the next run so the tools start from
the same state.

## Which fixture to use

| Fixture | Use it to test |
|---|---|
| `01-clear-failures` | Missing artifacts, contingent checks, and fake secret-candidate confirmation |
| `02-mixed` | A useful mix of passes, must-fix failures, and should-fix failures |
| `03-ready` | A clean report without invented findings |
| `04-unconventional` | AI resolution of valid evidence that the collector cannot recognise |

During a narrow edit, run only the fixture most likely to expose the change. Before
a meeting or release, run all four and, where useful, repeat them with a second AI
tool using the same compiled version and prompt.

## Interpreting differences

- A deterministic state mismatch is a regression: update the collector or the
  explicit expected JSON only when the behavior change is intentional.
- An AI-state mismatch needs review: decide whether the criterion, evidence, or
  instruction is ambiguous before changing it.
- Prose differences between tools are usually unimportant if check states, evidence,
  severity, and recommended fixes agree.
- A problem outside the current criteria is a criterion candidate, not permission for
  the reviewer to add an untraceable finding.

When adding a fixture, also add its four deterministic states to
`tests/manual/expected-deterministic.json` and document the intended AI behavior in
`tests/manual/expectations.md`.

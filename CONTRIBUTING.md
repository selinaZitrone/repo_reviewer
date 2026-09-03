# Contributing to repo-reviewer

This guide is for co-authors who want to edit criteria, run the automated checks, or
test the generated skill with an AI coding agent. The commands are the same on every
IDE; tool-specific sections below cover the initial setup.

## 1. Clone and create a Python environment

Requirements: Git and Python 3.10 or newer.

```bash
git clone https://github.com/selinaZitrone/repo_reviewer.git
cd repo_reviewer
python -m venv .venv
```

Activate the environment:

```text
Windows PowerShell:  .\.venv\Scripts\Activate.ps1
macOS/Linux:         source .venv/bin/activate
```

After activation, install the one development dependency and run the full local check:

```bash
python -m pip install -r requirements-dev.txt
python tools/dev_check.py
```

The command validates and tests the authoring tools, checks the controlled fixtures,
and generates `build/repo-reviewer/`. It never executes code from a repository being
reviewed.

## 2. Open the project in VS Code

1. Open the repository root, not an individual subfolder.
2. Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).
3. Run **Python: Select Interpreter** and select `.venv`.
4. Open a new integrated terminal and run `python tools/dev_check.py`.
5. Install whichever agent extension you want to test: [Claude
   Code](https://code.claude.com/docs/en/ide-integrations), [Codex](https://learn.chatgpt.com/docs/codex/ide),
   or [GitHub Copilot](https://code.visualstudio.com/docs/copilot/overview).

VS Code's [Python environment guide](https://code.visualstudio.com/docs/python/environments)
covers interpreter discovery and activation problems.

## 3. Connect the development build to an AI agent

Run the build first, then preview the user-level links:

```bash
python tools/setup_dev_skill.py --dry-run claude
python tools/setup_dev_skill.py --dry-run codex
python tools/setup_dev_skill.py --dry-run copilot
```

Create one or more links after checking the destinations:

```bash
python tools/setup_dev_skill.py claude codex copilot
```

On Windows the helper creates directory junctions; on macOS and Linux it creates
symbolic links. It refuses to replace an existing destination. Codex and Copilot share
the user-level `.agents/skills/repo-reviewer` destination, so naming both is safe.

### Claude Code

- Install and sign in to Claude Code or its VS Code extension.
- The helper links the build to `~/.claude/skills/repo-reviewer/`.
- Start Claude Code from this repository for development, or from one fixture/target
  repository for an isolated review.
- Invoke the generated skill with `/repo-reviewer`, or ask for it by name.

Claude Code documents personal and project skill locations in its [skills
guide](https://code.claude.com/docs/en/slash-commands).

### Codex

- Install and sign in to the Codex CLI or IDE extension.
- The helper links the build to `~/.agents/skills/repo-reviewer/`.
- Start Codex in one fixture/target repository and invoke `$repo-reviewer`.
- Run `/skills` or type `$` to confirm the skill is discoverable. Restart Codex if a
  newly created top-level skill folder does not appear.

See the official OpenAI documentation for [building and loading
skills](https://learn.chatgpt.com/docs/build-skills).

### GitHub Copilot

- Use Copilot CLI or agent mode in VS Code.
- The helper links the build to `~/.agents/skills/repo-reviewer/`; Copilot also supports
  a personal `~/.copilot/skills/` location.
- Invoke the generated skill as `/repo-reviewer`. In Copilot CLI, use `/skills reload`
  after adding it during an existing session.

See GitHub's [agent-skills overview](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
and [Copilot CLI setup guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).

## 4. Edit a criterion

1. Read `criteria/_schema.md` and `criteria/_groups.md`.
2. Copy `criteria/_authoring-template.md` or a nearby criterion in the same group.
3. Put the new file at `criteria/<group>/<criterion-id>.md`.
4. Use kebab-case IDs, keep published IDs stable, and cite at least one source from
   `criteria/_sources.md`.
5. Run `python tools/dev_check.py`.
6. Inspect the relevant section of `build/repo-reviewer/SKILL.md`.

If a check is `mode: deterministic`, add the corresponding fact to
`tools/collect_repository_evidence.py` and update the deterministic unit and fixture
expectations. The test suite enforces that every deterministic check has a collector
fact.

## 5. Test the generated reviewer

For deterministic evidence snapshots from all fixtures:

```bash
python tools/dev_check.py --fixture all
```

Then open exactly one directory under `tests/manual/fixtures/` as the agent workspace
and ask:

```text
Use the repo-reviewer skill to review this repository before publication.
```

Compare the result with `tests/manual/expectations.md`. Check states and evidence
before comparing prose. Do not show the expectation file to the reviewing agent in
advance. Save any local reports under `build/manual-results/`; `build/` and
`REVIEW.md` are ignored.

## 6. Report a test result

Record the following in an issue or shared document:

- repository or fixture name and expected quality;
- AI tool, model, access mode, date, and criteria version;
- unexpected passes or failures, including the criterion/check and why;
- unclear or unstable results;
- a missing criterion the reviewer was not permitted to report.

Write expected problems down before running the reviewer. This makes comparisons
between tools and revisions more meaningful.

## Project rules for AI assistants

`AGENTS.md` contains the shared project instructions used by Codex and supported
Copilot surfaces. `CLAUDE.md` imports those same instructions for Claude Code. Keep the
substantive rules in `AGENTS.md` so they do not drift.

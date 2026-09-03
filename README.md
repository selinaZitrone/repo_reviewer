# repo-reviewer

`repo-reviewer` is an AI skill for reviewing scientific repositories before publication. It asks an AI coding assistant to inspect a repository and write a prioritised `REVIEW.md` checklist.

The criteria are still being developed. Collaborator testing should help us find unclear checks, incorrect findings, and differences between AI tools.

The reviewer reads repository files but does not run the scientific code, assign a quality score, or claim that an analysis reproduces.

## Quick start

You need Git and Python 3.10 or newer. Clone this repository, open its folder in VS Code or another editor, and run:

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

Then install the development dependency and build the reviewer:

```bash
python -m pip install -r requirements-dev.txt
python tools/dev_check.py
```

`dev_check.py` validates the criteria, runs this project's tests, and creates the usable skill in `build/repo-reviewer/`. Do not edit that generated folder directly.

## Test it on another repository

The simplest method is to copy the complete `build/repo-reviewer/` folder into the repository you want to review:

| AI tool | Copy it to |
|---|---|
| Codex | `.agents/skills/repo-reviewer/` |
| Claude Code | `.claude/skills/repo-reviewer/` |
| GitHub Copilot | `.github/skills/repo-reviewer/` |

The folder structure matters. For example, a repository tested with Codex must look like this:

```text
repository-to-review/
|-- .agents/
|   `-- skills/
|       `-- repo-reviewer/
|           |-- SKILL.md
|           |-- README.md
|           `-- scripts/
`-- ...the repository's existing files
```

For Claude Code, replace `.agents/` with `.claude/`. For GitHub Copilot, replace it with `.github/`. Create the parent folders if they do not exist, and copy the `repo-reviewer` folder itself rather than placing its contents directly in `skills/`.

Open the target repository in the relevant AI tool and ask:

```text
Use the repo-reviewer skill to review this repository and create REVIEW.md.
```

You can also invoke it explicitly as `$repo-reviewer` in Codex or `/repo-reviewer` in Claude Code and GitHub Copilot.

The AI should write `REVIEW.md` in the target repository. If the copied skill is only for local testing, do not commit its folder to that repository. Copy it again whenever this project is rebuilt.

## Optional: link the skill for repeated testing

Instead of copying the build after every change, the setup helper can create a link from your AI tool's personal skills folder to `build/repo-reviewer/`:

```bash
python tools/setup_dev_skill.py --dry-run codex
python tools/setup_dev_skill.py codex
```

Replace `codex` with `claude` or `copilot`. The first command only shows what would happen. The second creates a Windows directory junction or a macOS/Linux symbolic link.

The helper does not download anything, contact a network service, or run code from repositories being reviewed. It refuses to replace an existing destination. Outside this repository, it only creates the necessary personal skill directories and the final link. Restart the AI tool if it does not detect the skill immediately.

Copying is easier to understand and isolates each test. Linking is more convenient while repeatedly editing and rebuilding the reviewer.

## Test fixtures

Small example repositories are available under `tests/manual/fixtures/`. Open one fixture directory as the AI tool's working folder, run the reviewer, and then compare its findings with `tests/manual/expectations.md`.

## Change the reviewer

See [CONTRIBUTING.md](CONTRIBUTING.md) for the concise development workflow. It explains how to:

- edit criteria;
- edit `tools/skill_template.md` to change the review instructions or report format;
- rebuild the skill; and
- test it on a repository.

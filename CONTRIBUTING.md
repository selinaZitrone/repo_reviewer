# Contributing

For first-time setup, IDE instructions, and an explanation of what the helper script does, see [README.md](README.md).

The normal contributor workflow is:

1. Edit the criteria or reviewer instructions.
2. Rebuild and test the skill.
3. Install the generated skill in a target repository.
4. Ask an AI assistant to review that repository and inspect the resulting `REVIEW.md`.

## 1. Edit the skill sources

### Change a criterion

Criteria live in `criteria/<group>/<criterion-id>.md`. Copy `criteria/_authoring-template.md` when adding a criterion, then fill in all required fields.

If a check can be automated reliably, update `tools/collect_repository_evidence.py` and add a test. Otherwise, leave it for the AI reviewer to assess from the repository context.

### Change the reviewer or report

Edit `tools/skill_template.md` to change:

- how the reviewer evaluates a repository;
- how findings are prioritised;
- the structure and wording of the generated `REVIEW.md`.

Do not edit `build/repo-reviewer/SKILL.md` directly. It is generated from the template and criteria and will be overwritten during the next build.

## 2. Rebuild and test

The first time, install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Then run:

```bash
python tools/dev_check.py
```

This validates the criteria, runs the tests, and rebuilds the complete skill in `build/repo-reviewer/`.

## 3. Install the generated skill in a test repository

Copy the whole `build/repo-reviewer/` folder into the repository you want to review:

- Codex: `.agents/skills/repo-reviewer/`
- Claude Code: `.claude/skills/repo-reviewer/`
- GitHub Copilot: `.github/skills/repo-reviewer/`

The final path must therefore contain `repo-reviewer/SKILL.md`, for example `repository-to-review/.agents/skills/repo-reviewer/SKILL.md` for Codex. Create the parent folders if necessary; do not copy the contents of `repo-reviewer/` directly into `skills/`.

For repeated testing, you can instead create a development link with `tools/setup_dev_skill.py`; the README explains the command and its safety properties.

## 4. Review the test repository

Open the target repository in your AI tool and ask it to use the reviewer, for example:

```text
Use the repo-reviewer skill to review this repository and create REVIEW.md.
```

Depending on the tool, you can also invoke it explicitly as `$repo-reviewer` or `/repo-reviewer`.

Check whether `REVIEW.md` is clear, correctly prioritised, and supported by evidence from the repository. If not, adjust the relevant criterion or `tools/skill_template.md`, rebuild, and repeat.

Before sharing a change, run `python tools/dev_check.py` once more and briefly report what you tested.

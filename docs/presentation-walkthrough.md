# repo-reviewer: architecture, development, and use

Presenter-oriented walkthrough for the collaborator meeting. The aim is to explain
what we build, how its parts fit together, and what an end user receives.

Suggested duration: 10–15 minutes plus discussion.

---

## 1. Two perspectives

```text
DEVELOPMENT SIDE                         USER SIDE

Author and test criteria                Install one generated skill
Build a tool-neutral skill              Open a repository
Validate deterministic behavior         Ask an agent to review it
Compare AI judgments                    Receive REVIEW.md
```

The development repository contains all authoring, build, testing, and planning
material. End users receive only a small generated bundle.

---

## 2. Development architecture

```text
AUTHORING
criteria/<group>/<criterion>.md
            │
            │  source of truth for criterion and check definitions
            ▼
BUILD
tools/compile_skill.py
            │
            ├── validates criterion fields
            ├── inserts checks into tools/skill_template.md
            ├── stamps the criteria version
            └── bundles the evidence collector
            │
            ▼
DISTRIBUTION
build/repo-reviewer/
├── SKILL.md
├── README.md
└── scripts/
    └── collect_repository_evidence.py
            │
            ▼
RUNTIME IN A TARGET REPOSITORY
deterministic facts → AI judgments → REVIEW.md
```

### Main development elements

| Element | Responsibility |
|---|---|
| `criteria/` | Source of truth for the criteria and their checks |
| `criteria/_schema.md` | Contract that every criterion file follows |
| `tools/skill_template.md` | Stable review procedure and report instructions |
| `tools/collect_repository_evidence.py` | Read-only mechanical inspection of a target repository |
| `tools/compile_skill.py` | Validates and assembles the distributable skill |
| `tests/` | Unit tests and controlled repository fixtures |
| `build/repo-reviewer/` | Generated end-user product; never edited by hand |

The criteria are maintained once. Claude Code, Codex, and GitHub Copilot do not
have separate criterion implementations.

---

## 3. From criterion to report

One criterion is a conceptual checklist item containing one or more independently
reportable checks.

Example:

```text
Criterion: The README orients a newcomer

├── A README exists at the root                 deterministic / must-fix
├── It says what the project is and why         AI / must-fix
├── It explains how to run the analysis         AI / should-fix
└── Its description matches the repository      AI / should-fix
```

Each check defines:

- a stable ID;
- its mode: `deterministic`, `ai`, or `none`;
- its severity: `must-fix`, `should-fix`, or `polish`;
- a summary of the good state;
- evidence examples used to judge it and suggest a fix.

### Why checks have different modes

| Mode | How it is handled |
|---|---|
| `deterministic` | The collector emits a fact such as `pass`, `fail`, `needs-ai`, or `candidate-fail` |
| `ai` | The agent reads relevant content and makes an evidence-backed judgment |
| `none` | The repository cannot establish it; it becomes a pre-publication to-do item |

The current collector covers four deterministic checks: root README, root licence,
dependency/environment record, and possible secret indicators. It never runs the
target repository's code.

---

## 4. What happens during a review

```text
1. The agent loads SKILL.md
2. The agent runs collect_repository_evidence.py
3. The collector returns JSON facts
4. The agent inspects files needed for AI checks and long-tail cases
5. The agent assigns one state to every check
6. The agent writes REVIEW.md at the repository root
```

The four report states are:

- ✅ pass;
- ❌ fail;
- ⚠️ could not verify;
- ➖ not applicable.

Every failure must map to a defined check and cite concrete repository evidence.
The report also records the criteria version, model, and date.

---

## 5. Development workflow

### One-time setup

```text
python -m pip install -r requirements-dev.txt
python tools/dev_check.py
python tools/setup_dev_skill.py codex
```

Replace or extend `codex` with `claude` or `copilot` as needed. The setup command
links the generated build into the selected tool's personal skill directory. It
does not overwrite an existing installation.

### Normal edit cycle

```text
edit criterion or tool
        ↓
python tools/dev_check.py
        ↓
automated tests + fixture assertions
        ↓
development skill rebuilt
        ↓
linked installation sees the new build
```

There is no repeated manual copying after the link has been created.

### When to run an AI review

| Change | Appropriate test |
|---|---|
| Collector implementation | Unit tests and deterministic fixture assertions |
| Compiler or schema | Unit tests, compile, inspect generated `SKILL.md` |
| Criterion wording, evidence, severity, or applicability | Build and review a relevant fixture with an agent |
| Report instructions | Build and compare full reports |
| Meeting or release candidate | Run all four fixtures and optionally compare two AI tools |

For all deterministic snapshots:

```text
python tools/dev_check.py --fixture all
```

Detailed instructions and expected fixture outcomes are in
[How to test repo-reviewer](how-to-test.md).

---

## 6. What an end user receives

```text
repo-reviewer/
├── SKILL.md
├── README.md
└── scripts/
    └── collect_repository_evidence.py
```

This generated directory is the complete v1 product. End users do not need the
development repository, criteria source files, compiler, tests, PyYAML, plan, or
decision records.

The bundle contains:

- the compiled criteria;
- the AI review procedure;
- the fixed report format;
- the read-only evidence collector;
- brief installation and invocation instructions.

---

## 7. User-level and project-level installation

### User-level installation

The user copies the bundle to a personal skill directory.

| Tool | Location |
|---|---|
| Codex | `~/.agents/skills/repo-reviewer/` |
| Claude Code | `~/.claude/skills/repo-reviewer/` |
| GitHub Copilot | `~/.agents/skills/repo-reviewer/` |

Use this when one researcher wants to review several repositories. The reviewer is
available across projects, and its files are not added to the repository being
reviewed. This is the recommended default for end users.

### Project-level installation

The team adds the bundle to the repository that should use it.

| Tool | Location |
|---|---|
| Codex | `.agents/skills/repo-reviewer/` |
| Claude Code | `.claude/skills/repo-reviewer/` |
| GitHub Copilot | `.github/skills/repo-reviewer/` or `.agents/skills/repo-reviewer/` |

Use this when a team wants the same reviewer version committed alongside a project.
It makes the configuration explicit and shareable, but adds the skill files to that
repository.

These are installation adapters around the same generated bundle. We do not maintain
different skills for different AI tools.

---

## 8. End-user workflow

```text
Install the generated skill once
        ↓
Open the repository in an agentic tool
        ↓
Ask: "Use repo-reviewer to review this repository before publication."
        ↓
Inspect REVIEW.md
        ↓
Fix the repository and run the review again
```

Explicit invocation examples:

- Codex: `Use $repo-reviewer to review this repository before publication.`
- Claude Code: `/repo-reviewer`
- GitHub Copilot CLI: `/repo-reviewer`

Natural-language invocation can also work through the skill description.

---

## 9. Live demonstration

Use the shared `02-mixed` fixture:

```text
tests/manual/fixtures/02-mixed
```

1. Show its small file tree.
2. Open it as a fresh Codex workspace.
3. Ask: `Use $repo-reviewer to review this repository before publication.`
4. Open the generated `REVIEW.md`.
5. Trace one deterministic result and one AI judgment back to their evidence.
6. Compare the result with `tests/manual/expectations.md`.

Points to highlight in the report:

- all defined checks are visible;
- failures cite repository evidence;
- severities determine the priority digest;
- contingent checks avoid reporting the same underlying absence repeatedly;
- the footer identifies the build and model used.

---

## 10. What exists and what the team should decide

### Working now

- Four prototype criteria containing 11 checks
- Shared schema and group taxonomy
- Tool-neutral generated Agent Skill
- Deterministic repository evidence collector
- Fixed `REVIEW.md` instructions
- Automated tests and four manual fixtures
- Development build and linked-install workflow

### Decisions for the team

- Ratify or revise the criterion schema
- Agree which criteria belong in the first real set
- Review severity and applicability boundaries
- Assign criterion-group and cross-cutting ownership
- Select and label the development and held-out repositories
- Decide how collaborators propose and review criterion changes

The website, upload-only chat workflow, CI integration, and broader distribution can
follow after the criteria and agentic pipeline have been validated.

---

## Reference documents

- [README](../README.md): product build, installation, and basic use
- [How to test](how-to-test.md): contributor setup and testing workflow
- [Meeting demo guide](meeting-demo.md): timing and feedback capture
- [Criterion schema](../criteria/_schema.md): authoring contract
- [Development plan](../PLAN.md): phases, principles, and open decisions

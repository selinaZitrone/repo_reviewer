# repo-reviewer

This folder is a self-contained Agent Skill containing {{CRITERIA_COUNT}} criteria and
{{CHECK_COUNT}} checks. It reviews repository files but never executes their code.

Install this entire `repo-reviewer` folder in a supported skill location:

- Claude Code: `~/.claude/skills/repo-reviewer/`
- Codex: `~/.agents/skills/repo-reviewer/`
- GitHub Copilot: `~/.agents/skills/repo-reviewer/`

Open the repository you want to review and ask:

```text
Use the repo-reviewer skill to review this repository before publication.
```

This version requires an agentic tool with filesystem and shell access. Support for
ordinary upload-based web chats is deferred.

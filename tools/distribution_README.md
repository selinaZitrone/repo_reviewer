# repo-reviewer prototype

This folder is a self-contained Agent Skill containing the current prototype
(4 criteria / 11 checks). It reviews repository files but never executes their code.

Install this entire `repo-reviewer` folder in a supported skill location:

- Claude Code: `~/.claude/skills/repo-reviewer/`
- Codex: `~/.agents/skills/repo-reviewer/`
- GitHub Copilot: `~/.agents/skills/repo-reviewer/`

Open the repository you want to review and ask:

```text
Use the repo-reviewer skill to review this repository before publication.
```

This v1 prototype requires an agentic tool with filesystem and shell access. Support
for ordinary upload-based web chats is deferred.

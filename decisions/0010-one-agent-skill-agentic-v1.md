# 0010 — One open-standard skill; v1 requires an agentic tool

**Decision:** The reviewer has one canonical, generated `SKILL.md` bundle using the
open Agent Skills format. It is not forked into independently maintained Claude,
Codex, and Copilot prompts. Tool-specific packaging may copy the same built bundle
into a host's discovery directory, but it may not redefine criteria or review rules.

v1 requires an **agentic tool with filesystem and shell access**. The AI runs the
bundled read-only repository evidence collector, inspects repository files for the
AI-judgment checks, and writes `REVIEW.md`.

Upload-only web chats, prepared repository bundles, CI, and GitHub Actions are
deferred until the core review pipeline and criteria have been validated.

**Why:**

- Claude Code, Codex, and supported GitHub Copilot agent surfaces understand the
  open `SKILL.md` shape, so three handwritten prompts would create avoidable drift.
- Filesystem and shell access provide the evidence needed for both deterministic and
  judgment-based checks without designing a second, reduced-coverage ingestion path.
- The first version should validate the review method and criteria before expanding
  the number of delivery contexts.
- The criteria remain the durable product. Delivery adapters stay thin.

**Safety:** The repository evidence collector analyses files but never executes the
reviewed repository's code or reads tabular cell values. Possible secret values are
never emitted; only redacted candidate locations are passed to the AI for confirmation.

**Current host references:**

- Claude Code skills: <https://code.claude.com/docs/en/skills>
- Codex skills: <https://learn.chatgpt.com/docs/build-skills>
- GitHub Copilot agent skills:
  <https://docs.github.com/en/copilot/concepts/agents/about-agent-skills>

**Revisit if:** the agentic v1 is validated and there is clear demand for an
upload-only workflow, a host diverges from the open skill format, or host-specific
packaging materially improves installation without duplicating policy.

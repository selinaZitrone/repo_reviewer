# 0009 — The tool is version-control-agnostic: it reviews the files present, not git state

**Decision:** The reviewer audits the **files present in the repository directory** —
what the author will actually publish (a folder zipped to Zenodo/OSF/figshare, or a
push to a host) — **not** a git repository's history or metadata. It does **not**
assume the project uses git. No criterion may depend on `git` being installed, on a
`.git/` directory existing, or on commit history.

**Why:**

- **Many scientists publish a folder, not a git repo.** They zip a directory to
  Zenodo/OSF, or upload to a journal. Assuming git makes the tool wrong or useless
  for them — the same "make the tool useless to a whole discipline" failure the data
  group guards against.
- **What we actually care about is a property of the published files.** Secrets,
  junk, and stray files are visible by reading the file tree. Git is one way those
  files got there, not a precondition for reviewing them.
- Consistent with `decisions/0002` (reads files, does not execute) and keeps the tool
  usable in every delivery tier (agentic IDE, uploaded zip, pasted prompt).

**Consequences:**

- Hygiene criteria are phrased as "no X is **present**", not "no X is **committed**".
  The naming follows: `no-committed-secrets` → `no-secrets-present`;
  `no-committed-junk` → `no-junk-files`. (The existing committed exemplar under
  `criteria/repository-hygiene/` is to be reconciled to this when formalised.)
- git-specific remediation (purge a leaked secret from history with `git filter-repo`;
  add a `.gitignore`) is **advice for git users** in the body's *How to satisfy it* —
  never the core check.
- A dedicated **`.gitignore` criterion is dropped**: it assumes git and is redundant
  with checking for junk files directly (the *effect*), which works for any repo.
- Where git *is* present, the deterministic pre-flight script may use it as a fast
  path (e.g. `git ls-files`), but must fall back to a plain directory walk and must
  never require it.

**Revisit if:** we add a git-history-specific tier (e.g. scanning history for secrets
that were committed and later deleted). That would be an explicit, opt-in, git-only
check, clearly marked as such — not a default assumption.

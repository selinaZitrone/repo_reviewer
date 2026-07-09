---
id: no-committed-secrets
title: No secrets or credentials are committed
group: repository-hygiene
sources:
  - wilson-2017
checks:
  - id: no-committed-secrets
    mode: deterministic
    pass_when: absent
    severity: must-fix
    summary: No secrets or credentials are committed
    evidence:
      any:
        - ".env / .Renviron committed to the repo"
        - "private key files (id_rsa, *.pem, *.ppk)"
        - "hard-coded API keys, tokens or passwords (e.g. api_key=, secret=, token=, password=)"
        - "cloud credentials (aws credentials file, .httr-oauth, service-account .json)"
---

## Why it matters

A secret committed to a repository is not fixed by deleting it later: it stays in the
git history forever, and anyone who clones the repository can read it. Publishing a
repository with a live API key, database password, or private key means publishing the
key — often to a permanent public archive. This is one of the few review findings that
is a genuine security incident, not just a reusability problem, which is why it is
`must-fix`.

This check passes by **absence**: a clean repository is one where none of these appear.

## How to satisfy it

- Never commit `.env` / `.Renviron`, key files, or credential files. Add them to
  `.gitignore` **before** the first commit.
- Load secrets from environment variables (R: `Sys.getenv()`; Python: `os.environ`) or
  a secrets manager — never hard-code them in a script.
- Scan before publishing with a tool such as `gitleaks` or `git-secrets`.
- **If a secret was already committed:** rotate/revoke it immediately (assume it is
  compromised), then purge it from history (`git filter-repo`) — removing the file in a
  new commit is not enough.

## Examples

Not sufficient (fails):

    .Renviron committed with MY_API_KEY=...      # secret is now in history forever
    scripts/fetch.R:  key <- "sk-live-abc123"    # hard-coded credential

Sufficient (passes):

    .gitignore  ->  .Renviron, *.pem, .httr-oauth
    scripts/fetch.R:  key <- Sys.getenv("MY_API_KEY")

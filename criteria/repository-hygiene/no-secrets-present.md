---
id: no-secrets-present
title: No secrets or credentials are present
group: repository-hygiene
sources:
  - project-contribution
checks:
  - id: no-secrets-present
    mode: deterministic
    pass_when: absent
    severity: must-fix
    summary: No secrets or credentials are present
    evidence:
      any:
        - ".env or .Renviron files"
        - "private key files such as id_rsa, *.pem, *.ppk, or *.key"
        - "hard-coded API keys, tokens, client secrets, or passwords"
        - "cloud credential or service-account files"
---

## Why it matters

A live API key, password, or private key in a shared repository is a security incident,
not merely a documentation problem. Removing it from the latest copy may not remove it
from version-control history or earlier archives.

This check is version-control agnostic: it examines what is present in the directory
being reviewed. Potential indicators require confirmation and secret values must never
be reproduced in the report.

## How to satisfy it

- Store secrets in environment variables or a secrets manager, never in source files.
- Exclude local credential files before sharing or archiving the project.
- If a real secret was exposed, rotate or revoke it immediately. Git users should also
  purge it from history because deleting the current file is not enough.

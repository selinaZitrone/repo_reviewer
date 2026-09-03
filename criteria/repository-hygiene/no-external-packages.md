---
id: no-external-packages
title: Installable third-party packages are not copied into the repository
group: repository-hygiene
sources:
  - wilson-2017
checks:
  - id: no-external-packages
    mode: ai
    pass_when: absent
    severity: should-fix
    summary: Third-party dependencies are not bundled when they can be installed and cited separately
    evidence:
      any:
        - "Toolboxes, external, third-party, lib, packages, or library folders containing copied dependencies"
        - "complete MATLAB toolboxes, Python packages, R libraries, or external distributions"
        - "large groups of files unrelated to the project's own source code"
---

## Why it matters

Bundled dependencies obscure their origin, complicate licensing, enlarge the project,
and make updates and version tracking harder.

## How to satisfy it

Use the language's package manager when possible. Otherwise document the dependency's
source, citation, and exact version, and explain why it must be included.

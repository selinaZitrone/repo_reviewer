---
id: no-junk-files
title: No machine-generated or throwaway files are present
group: repository-hygiene
sources:
  - wilson-2017
checks:
  - id: no-junk-files
    mode: deterministic
    pass_when: absent
    severity: should-fix
    summary: No machine-generated, operating-system, or editor junk files are present
    evidence:
      python:
        - "__pycache__/, *.pyc, .ipynb_checkpoints/, .pytest_cache/, or *.egg-info/"
      r:
        - ".Rhistory, .RData, .Ruserdata, or .Rproj.user/"
      any:
        - ".DS_Store, Thumbs.db, node_modules/, unneeded build/ or dist/ output"
        - "editor backup files such as *.bak, *~, or *.orig"
        - "user-specific editor metadata; intentionally shared editor configuration is not junk"
  - id: no-hand-versioned-duplicates
    mode: ai
    pass_when: absent
    severity: polish
    summary: No ambiguous hand-versioned or final-copy duplicates are present
    evidence:
      any:
        - "neighbouring files such as analysis.R, analysis-v2.R, and analysis-FINAL.R"
        - "files named Copy of ... or ... copy"
        - "near-identical files whose canonical version is unclear"
---

## Why it matters

Throwaway files and ambiguous manual copies clutter a shared project and make it hard
to tell which artifacts are authoritative.

## How to satisfy it

- Remove generated caches, operating-system files, editor backups, and obsolete build
  outputs before sharing.
- Configure the relevant ignore mechanism when using version control.
- Use version control or clearly labelled releases instead of filenames such as
  `FINAL-v2`.
- Keep editor configuration only when it is intentionally shared and documented.

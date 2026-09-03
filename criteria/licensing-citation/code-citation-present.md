---
id: code-citation-present
title: The repository explains how to cite the code
group: licensing-citation
sources:
  - fair4rs
  - fair-software-eu
checks:
  - id: code-citation-present
    mode: deterministic
    severity: should-fix
    summary: The repository states how to cite the code
    evidence:
      any:
        - CITATION.cff
        - codemeta.json
        - CITATION
        - CITATION.txt
        - "a How to cite or Citation section in the README"
  - id: code-citation-complete
    mode: ai
    severity: should-fix
    summary: The software citation contains authors, title, year, version, and an archive DOI when available
---

## Why it matters

A repository is a research output in its own right. Its contributors may differ from
the paper's authors, and users need enough information to credit the software itself.

## How to satisfy it

- Add a `How to cite` section to the README or, preferably, a root `CITATION.cff`.
- Include authors, title, year, and version. Add the software DOI after the repository
  is archived, and update it with each release.
- The [Citation File Format initializer](https://citation-file-format.github.io/cff-initializer-javascript/)
  can generate a `CITATION.cff`, including ORCID identifiers.

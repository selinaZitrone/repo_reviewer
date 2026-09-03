---
id: linked-to-publication
title: The repository is linked to its accompanying publication
group: licensing-citation
sources:
  - fair4rs
  - nature-code-guidelines
checks:
  - id: publication-linked
    mode: ai
    severity: should-fix
    summary: The repository links to the accompanying paper with its DOI when a paper exists
    evidence:
      any:
        - "a paper reference and DOI in the README"
        - "a CITATION.cff preferred-citation entry for the paper"
        - "a Publication section naming the paper and DOI"
---

## Why it matters

Readers of the paper need to find the code, and readers of the code need to find the
paper. The software and paper are separate research outputs and may require separate
citations.

## How to satisfy it

Name the paper and DOI in the README or use the `preferred-citation` field in
`CITATION.cff`. The manuscript should separately cite the archived repository version.

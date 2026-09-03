---
id: folder-structure-documented
title: The folder structure required to rerun the analysis is documented
group: reproducibility
sources:
  - marwick-2018
  - nature-code-guidelines
checks:
  - id: folder-structure-documented
    mode: ai
    severity: must-fix
    summary: The rerun instructions specify the required folder structure
    evidence:
      any:
        - "a directory tree in the main README or reproduction guide"
        - "instructions identifying where externally obtained inputs must be placed"
  - id: inputs-outputs-documented
    mode: ai
    severity: must-fix
    summary: The rerun instructions specify where inputs come from and where outputs go
    evidence:
      any:
        - "the source and expected location of input data"
        - "the destination of generated results"
        - "input and output documentation for each major script"
        - "a data-flow diagram"
---

## Why it matters

Commands alone are insufficient when the analysis expects files in particular places.
A newcomer also needs to know which inputs are supplied or downloaded and where the
workflow writes its results.

## How to satisfy it

Document the relevant directory tree and identify the source and location of each major
input and output. Keep this description aligned with the actual code paths.

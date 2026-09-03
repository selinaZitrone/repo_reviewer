---
id: data-separation
title: Raw data is separated from processed or derived data
group: data
sources:
  - turing-way-compendia
  - marwick-2018
checks:
  - id: data-separation-by-folder
    mode: ai
    severity: must-fix
    summary: Raw and processed data are stored separately when the workflow creates derived data
    evidence:
      any:
        - "separate locations such as data/raw and data/processed"
        - "preprocessing scripts write outputs outside the raw-data location"
  - id: raw-data-read-only
    mode: ai
    pass_when: absent
    severity: must-fix
    summary: Scripts do not overwrite raw input data
    evidence:
      any:
        - "a script reads a raw input and writes changes back to the same file"
---

## Why it matters

Keeping raw inputs unchanged preserves the starting point of the analysis and makes
processing steps auditable and reversible.

## How to satisfy it

Store raw and derived data in separate, clearly named locations. Treat raw inputs as
read-only and write every cleaned, transformed, or aggregated result to the processed
or derived-data location.

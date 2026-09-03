---
id: data-naming
title: Data files and variables are named consistently and machine-readably
group: data
sources:
  - wilson-2017
checks:
  - id: data-naming-consistent
    mode: ai
    severity: should-fix
    summary: Included data files follow a consistent naming scheme
    evidence:
      any:
        - "consistent sample, date, or version identifiers"
        - "consistent delimiter and casing conventions"
  - id: domain-naming-standard-used
    mode: ai
    severity: polish
    summary: Established domain-specific data standards are used where applicable
    evidence:
      any:
        - "BIDS for neuroimaging"
        - "CDISC for clinical trials"
        - "Darwin Core for biodiversity data"
        - "NetCDF conventions or GenBank formats where relevant"
  - id: data-machine-readable
    mode: ai
    pass_when: absent
    severity: should-fix
    summary: Column and variable names avoid characters that hinder automated processing
    evidence:
      any:
        - "whitespace or special characters in column names"
        - "duplicate column names"
---

## Why it matters

Consistent names make batches of files predictable and reduce special-case parsing.
Domain standards add interoperability where a community already shares conventions.

## How to satisfy it

- Choose one convention for casing, delimiters, dates, versions, and sample IDs.
- Use unique, machine-readable column names without whitespace or avoidable special
  characters.
- Follow an established domain standard when one applies.

See the [UBC Research Data Management file-naming
guide](https://ubc-library-rc.github.io/rdm/content/01_file_naming.html).

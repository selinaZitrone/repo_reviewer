---
id: sensitive-data
title: Obvious indicators of sensitive data are surfaced for author confirmation
group: data
sources:
  - project-contribution
checks:
  - id: sensitive-data-check
    mode: ai
    pass_when: absent
    severity: must-fix
    summary: No obvious indicators of unintentionally shared sensitive data are present
    evidence:
      any:
        - "filenames or column headers suggesting names, personal email addresses, medical records, or government identifiers"
        - "notebook outputs that may expose personal information"
---

## Why it matters

Accidentally sharing personal or confidential data can harm participants and breach
legal or ethical obligations. An automated review cannot decide whether a suspicious
field is genuinely sensitive or whether publication is authorised, so this criterion
must prompt author confirmation rather than make that determination.

## How to satisfy it

- Inspect filenames, directory listings, and column headers before sharing.
- Review notebook outputs and clear them when they could contain sensitive material.
- Do not inspect or reproduce cell values during the automated review.
- If a possible indicator is found, verify the intended publication status with the
  responsible author or data steward.

---
id: code-is-commented
title: Comments help a reader understand non-obvious code
group: code-quality
sources:
  - wilson-2017
  - ropensci-devguide
checks:
  - id: comments-explain-why
    mode: ai
    severity: should-fix
    summary: Comments explain the reasons for non-obvious choices rather than restating code
    evidence:
      any:
        - "reasoning behind a threshold, transformation, workaround, or domain-specific choice"
        - "do not reward comments that merely narrate a self-evident operation"
  - id: comments-sufficient
    mode: ai
    severity: polish
    summary: Non-obvious parts of the analysis are explained well enough to follow
    evidence:
      any:
        - "complex stretches, magic numbers, or unusual choices have enough context"
        - "do not require a comment on every line or a fixed comment density"
---

## Why it matters

Code shows what happened but often cannot show why a threshold, exclusion, or unusual
step was chosen. Useful comments preserve that reasoning; comments that merely restate
the code add noise and become stale.

## How to satisfy it

Use clear names first, then comment the non-obvious decisions, magic numbers,
domain-specific assumptions, and workarounds. Section headings can help readers follow
the major stages without demanding comments on self-explanatory lines.

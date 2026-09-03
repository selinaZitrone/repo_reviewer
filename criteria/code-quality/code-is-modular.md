---
id: code-is-modular
title: Code is organised into manageable pieces without large duplicated blocks
group: code-quality
sources:
  - wilson-2017
  - marwick-2018
  - ropensci-devguide
checks:
  - id: no-duplicated-code
    mode: ai
    pass_when: absent
    severity: should-fix
    summary: No large blocks of logic are copied and repeated
    evidence:
      any:
        - "near-identical logic whose bug fixes would have to be repeated in several places"
        - "do not treat plotting layers, data-wrangling pipelines, or configuration blocks as duplication merely because they look similar"
  - id: code-in-manageable-pieces
    mode: ai
    severity: polish
    summary: The analysis is divided into readable stages rather than one monolithic script
---

## Why it matters

Copy-pasted logic is difficult to maintain because every fix must be repeated. Very
long scripts are also harder to navigate and understand. This criterion concerns
readability and practical reuse, not whether the results reproduce.

## How to satisfy it

Split long workflows into clearly named stages or sections. Extract a function when a
substantial block is repeated with only a few values changed. Do not force naturally
repetitive plotting or configuration code into abstractions that make it less clear.

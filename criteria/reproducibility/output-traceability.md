---
id: output-traceability
title: Published outputs are traceable to the code that generated them
group: reproducibility
sources:
  - nature-code-guidelines
checks:
  - id: outputs-mapped-to-code
    mode: ai
    severity: polish
    summary: Published figures, tables, and reported numbers are mapped to their generating code
    evidence:
      any:
        - "a README mapping such as Figure 1 -> scripts/create-figure-1.R"
        - "script headers or workflow comments naming the publication outputs they generate"
---

## Why it matters

A reader should be able to move from a published result to the exact code responsible
for it without reverse-engineering the entire workflow.

## How to satisfy it

Add a compact table to the README or comments in the workflow that map each published
figure, table, or other major result to the script or target that generates it.

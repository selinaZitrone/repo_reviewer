---
id: reproduction-instructions
title: Instructions for reproducing the analysis are provided
group: reproducibility
sources:
  - nature-code-guidelines
  - wilson-2017
checks:
  - id: code-execution-documented
    mode: ai
    severity: must-fix
    summary: The main README explains how to run or reproduce the analysis
    evidence:
      any:
        - "execution steps, commands, or a workflow description in the root README"
        - "a root README link to a dedicated reproduction guide"
  - id: run-order-clear
    mode: ai
    severity: must-fix
    summary: The order in which code must run is apparent or documented
    evidence:
      any:
        - "numbered scripts where the language permits them"
        - "ordered execution steps or a workflow diagram in the README"
        - "a documented master script that calls the other scripts"
  - id: quick-start
    mode: ai
    severity: polish
    summary: Complex projects provide a quick start for running the main analysis with minimal setup
    evidence:
      any:
        - "a Quick start or Getting started section in the main README"
---

## Why it matters

An independent researcher should be able to rerun the analysis without asking the
authors for missing steps. Clear execution instructions reduce ambiguity and make the
workflow easier to inspect, verify, and reuse.

## How to satisfy it

- Add a `How to run`, `Reproduce`, or equivalent section to the main README.
- State the commands and their order, or point to one master script or workflow.
- Number scripts where that convention works for the language; do not rely on numeric
  prefixes for MATLAB function files.
- Add a short quick start when the full setup or workflow is complex.

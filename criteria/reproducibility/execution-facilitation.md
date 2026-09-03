---
id: execution-facilitation
title: Code execution is facilitated
group: reproducibility
sources:
  - wilson-2017
  - nature-code-guidelines
checks:
  - id: workflow-automation
    mode: ai
    severity: polish
    summary: The workflow can be run through a master script, workflow tool, or single command
    evidence:
      any:
        - "a main, master, run-all, or pipeline-controller script"
        - "a Makefile, Snakefile, targets or drake workflow, or Nextflow pipeline"
        - "single-command execution documented in the README"
---

## Why it matters

A single entry point reduces manual mistakes and makes the intended workflow explicit.

## How to satisfy it

Provide a master script, a workflow-management definition, or one documented command
that runs the complete workflow in the required order.

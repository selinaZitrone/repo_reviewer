---
id: randomness-is-reproducible
title: Randomness is controlled where it affects results
group: reproducibility
sources:
  - wilson-2017
checks:
  - id: seed-is-set
    mode: ai
    severity: should-fix
    summary: A fixed seed covers randomness that affects analysis results (only when such randomness is used)
    evidence:
      r:
        - "set.seed(...) before the relevant random operations"
      python:
        - "random.seed(...), numpy.random.seed(...), or numpy.random.default_rng(seed)"
        - "framework-specific seeds such as torch.manual_seed(...) or tf.random.set_seed(...)"
---

## Why it matters

Without a controlled seed, rerunning a stochastic analysis can produce different
results. This does not apply to repositories without result-affecting randomness or to
uses such as random temporary filenames, UUIDs, or cosmetic plot jitter.

## How to satisfy it

Set a fixed seed before random sampling, resampling, splitting, or stochastic model
fitting. Seed every random-number generator used by the workflow.

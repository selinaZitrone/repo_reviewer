---
id: meaningful-names
title: Variables and functions are named for what they hold or do
group: code-quality
sources:
  - wilson-2017
  - ropensci-devguide
checks:
  - id: meaningful-names
    mode: ai
    severity: should-fix
    summary: Variable and function names communicate what they hold or do
    evidence:
      any:
        - "flag names that hide meaning, such as df2, tmp, data_final, res, foo, or a1"
        - "allow conventional short names when their meaning is clear in context, such as loop counters and standard mathematical symbols"
---

## Why it matters

Names are part of the documentation. Clear names let readers follow data and decisions
through the workflow without constantly searching for definitions.

## How to satisfy it

Use names such as `patient_data` instead of `df2` and `standardise_data()` instead of
`f1()`. Function names often work well when they begin with a verb. Consistency and
meaning in context matter more than length.

For language conventions, see the [tidyverse style guide](https://style.tidyverse.org/syntax.html#object-names)
and [PEP 8 naming conventions](https://peps.python.org/pep-0008/#naming-conventions).

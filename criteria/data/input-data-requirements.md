---
id: input-data-requirements
title: Input-data requirements are documented
group: data
sources:
  - nature-code-guidelines
  - turing-way-compendia
checks:
  - id: input-data-format
    mode: ai
    severity: must-fix
    summary: The format required to run the analysis with new input data is documented
    evidence:
      any:
        - "supported file types, required variables, units, missing-value codes, and long or wide shape"
        - "an example input or visualisation plus any required transformation steps"
  - id: input-data-processing-level
    mode: ai
    severity: must-fix
    summary: The required preprocessing state of new input data is documented
    evidence:
      any:
        - "whether input must be raw, cleaned, normalised, aggregated, transformed, or feature-engineered"
---

## Why it matters

Code cannot be reused on new data if users must guess its expected variables, units,
shape, missing-value conventions, or preprocessing state.

## How to satisfy it

Provide a data dictionary, schema, or compact table describing the required inputs.
State the expected processing level and include a small synthetic example when that is
the clearest way to show the contract.

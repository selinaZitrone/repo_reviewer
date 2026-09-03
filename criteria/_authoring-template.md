# Criterion authoring template

Copy this file to `criteria/<group>/<criterion-id>.md`, remove this introductory text,
and replace every placeholder. Files beginning with `_` are documentation and are not
compiled.

```markdown
---
id: criterion-id
title: The criterion's good state in one sentence
group: structure
sources:
  - source-id-from-_sources.md
checks:
  - id: check-id
    mode: deterministic
    severity: must-fix
    summary: The check's good state in one line
    # pass_when: absent
    evidence:
      r:
        - best R evidence or fix first
      python:
        - best Python evidence or fix first
      any:
        - language-neutral evidence
---

## Why it matters

Explain the practical consequence for a researcher trying to understand or reuse the
repository.

## How to satisfy it

Give concrete actions, including language-specific instructions where useful.

## Examples

Include this optional section only when a boundary example makes the check clearer.
```

Check modes are `deterministic`, `ai`, and `none`. Severities are `must-fix`,
`should-fix`, and `polish`. `pass_when` defaults to `present`; use `absent` for checks
whose good state is that no violation is found. Deterministic checks require evidence;
`mode: none` checks omit it.

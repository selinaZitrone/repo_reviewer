---
id: repository-archived
title: A fixed release is deposited in a durable archive
group: archive-release
sources:
  - fair4rs
  - fair-software-eu
  - nature-code-guidelines
checks:
  - id: archive-doi-created
    mode: none
    severity: should-fix
    summary: Deposit the release in Zenodo, Dryad, Figshare, or a domain repository and record its DOI
---

## Why it matters

A mutable development repository is not a durable archive of the exact version behind
a publication. A repository DOI gives readers a stable, citable record.

## How to satisfy it

Create a versioned release and deposit it in Zenodo, Dryad, Figshare, or an appropriate
domain repository. Add the resulting DOI to the README and manuscript. Where useful,
connect the code host to the archive so future releases can be deposited consistently.

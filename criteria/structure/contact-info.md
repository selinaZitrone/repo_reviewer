---
id: contact-info
title: Contact information is provided
group: structure
sources:
  - nature-code-guidelines
  - ropensci-devguide
checks:
  - id: contact-info-present
    mode: ai
    severity: should-fix
    summary: The repository names a contact person or a way to ask questions
    evidence:
      any:
        - "a README contact section with an email address or account handle"
        - "maintainer details in CITATION.cff"
        - "the issue tracker identified as the place for questions"
---

## Why it matters

Even a well-documented project can leave a user with a question. A clear contact route
keeps those questions from being lost or sent to the wrong contributor.

## How to satisfy it

Name a maintainer and contact route in the README or `CITATION.cff`, or direct users to
the repository's issue tracker.

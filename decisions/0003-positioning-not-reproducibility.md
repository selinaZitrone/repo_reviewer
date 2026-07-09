# 0003 — Positioned as "publication-readiness", not "reproducibility"

**Decision:** We describe the tool as a **publication-readiness / reviewability**
reviewer. We avoid calling it a "reproducibility checker" or saying it
"validates" a repository.

**Why:** In the relevant literature, "reproducibility assessment" means
*executing* the artifact and checking the results come back — Reproscreener emits
a ReproScore, ARA scores reconstructability, recent work recovers effect sizes to
within ±0.05 Cohen's d. We deliberately do not execute (`decisions/0002`).
Presenting a non-executing tool as a reproducibility checker to an audience that
knows this literature invites exactly the objection we can't answer. "Validate"
is likewise too strong. Honest scope is more defensible and still valuable:
we help make a repository understandable, trustworthy, and reusable *before* it
is published.

**Revisit if:** an execution tier is ever added (then, and only then, does
"reproducibility" language become earned).

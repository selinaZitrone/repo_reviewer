# 0001 — No score or badge

**Decision:** The report gives severity-tiered, evidence-backed findings. No
letter grade, no percentage, no badge. At most a factual count ("meets 7 of 9
essential criteria").

**Why:** A score or badge is a trust signal, and trust signals get their value
from an *independent* verifier (ACM badges, JOSS, CODECHECK all rest on a human
other than the author checking). A badge the author mints by running a tool on
their own machine certifies nothing and dilutes the badge ecosystems that do rest
on review. `howfairis` badges defensibly *because all its checks are objective* —
the principled line is therefore: **a score is defensible only when every
underlying check is deterministic.** Ours deliberately mixes deterministic checks
with LLM judgment, so any score would be an unstable number about stability — the
exact failure we help people avoid. A number also becomes the target, displacing
the goal of a genuinely reusable repository.

**Revisit if:** the tool ever becomes deterministic-only, or an independent body
adopts it as a verifier.

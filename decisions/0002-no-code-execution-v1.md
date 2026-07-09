# 0002 — v1 does not execute code

**Decision:** The tool reads the repository; it never runs it. No installing
dependencies, no running scripts, no re-running the analysis. Execution-dependent
checks (does it install? does it re-run? does it reproduce?) are out of scope for
v1 and live only in the website + the report's post-review checklist.

**Why:** Executing an arbitrary repository is a whole project by itself
(containers, resources, safety) — it is what CODECHECK does, with human checkers.
It is far beyond a fast prototype. Not executing also keeps the tool usable in
non-agentic tiers (uploaded zip, pasted prompt). We check *reviewability and
completeness*, not that the code runs.

**Consequence:** the report must state plainly that it does **not** verify the
analysis runs or reproduces. Nature's "ask a colleague unfamiliar with the tool
to run it" becomes our post-review recommendation instead.

**Revisit if:** a later version adds an opt-in, sandboxed execution tier. Keep the
criteria schema able to grow an execution mode later, but do not build it now.

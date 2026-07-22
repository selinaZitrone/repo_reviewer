# Criteria backlog & open group placements

Two kinds of open item, tracked here (committed, cross-group) so nothing falls
between group owners.

## A. Provisional group placements — pending collaborator decision

Criteria that are being authored, but whose **group is not yet settled**.

| Criterion | Authored under (owner) | May move to | Note |
|---|---|---|---|
| `paths-are-relative` — no absolute paths / `setwd()`; runs from a fresh clone | code-quality (Selina) | **reproducibility** | Written in code-quality for now; flagged for colleagues that it may belong in reproducibility (`_groups.md` lists it in that scope). |
| `randomness-is-reproducible` — a seed is set wherever the analysis uses randomness | code-quality (Selina) | **reproducibility** | Same — in the reproducibility scope, authored in code-quality provisionally. |

## B. Missing / unwritten criteria

Agreed needed, nobody has written them yet. Distinct from PLAN.md's *"Deferred
criterion candidates"* (`no-unused-files`, `large-files-advisory`), which are held out
of v1 on purpose pending validation.

| Criterion | Group (owner) | Status | Surfaced |
|---|---|---|---|
| _(none currently)_ | | | |

**Note:** `run-order-discoverable` is not a gap — it already exists in reproducibility
as *"is the execution order clear?"*.

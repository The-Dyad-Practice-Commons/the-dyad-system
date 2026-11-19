# specs craft vocabulary (Tended terms; Rule-6 `check_craft`; d-work #723)

One row per term; `rule` names the craft rule (`../rules/<rule>.md`) that owns it. A craft term is referenced,
never defined, by the Agent vocabulary (Rule-6), as `specs:<term>`. The craft says "statement", never "claim", which the
Agent vocabulary defines (Rule-9).

| term | definition | rule |
|------|------------|------|
| specification | one file per subject, `<instance>/specs/<subject>.md`, answering five questions in three perspectives of one product: fifteen cells, every statement cited or marked | specs |
| perspective | one of the three views of the same product a specification is written from: PRD (the product's), Architecture (the system's), UX/UI (the user's) | specs |
| question | one of the five a specification answers in every perspective: WHAT, WHY, HOW, WHEN, WHO | specs |
| cell | one question in one perspective, a `###` subsection under a `##` section: one or more statements, or `n/a: <reason>` | specs |
| accepted | a specification's status once the done-`Y` of the row its `row:` line names is recorded; it records that `Y` and asks nothing | specs |
| statement | one bullet of a cell, ending in one citation or one mark | statements |
| citation | `[cite: <ref>]`: a path, a row, a provenance entry, a release tag, or `ext: <url>`; it resolves when its target exists | statements |
| assumption | the mark `[assumption]`: a statement taken as true without a source, listed for the operator at the row's Done | statements |

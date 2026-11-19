# specs — a product's specification in five questions and three perspectives (Tended craft, `crafts/specs/`, zone `craft`)

A specification answers five questions — WHAT, WHY, HOW, WHEN and WHO — in each of three perspectives of one product:
the product's (PRD), the system's (Architecture) and the user's (UX/UI). Every question is answered in every
perspective, so a specification has fifteen cells, and every statement in a cell is cited or marked as an assumption
or a proposal. The guard checks that the cells are there and the citations resolve; whether the statements are true,
and whether the product is the right one, stays the operator's to judge at the Done of the row that writes it.
Authored in dyad-system under d-work #723 (plan `agent-corpus/d-work/plans/723.md`, revisions 1–3). It requires the
core only (`MANIFEST.md`). Version `VERSION` (0.1.0). Not bundled with the core: no core Rule cites this craft by path,
and its purpose ground waits for its tree to serve every installing operator (Rule-11 property 2).

| path | holds |
|------|-------|
| `rules/specs.md` | the form: one file per subject, its header lines, the five questions by the three perspectives, `n/a: <reason>`, `status: accepted` |
| `rules/statements.md` | every bullet a statement, cited or marked; the citation kinds and what resolving one means; WHEN never an invented date |
| `vocabulary/CRAFT.md` | the craft's terms |
| `templates/spec.md` | a specification with all fifteen cells and one example statement each; it passes the guard |
| `guards/specs.py` | the guard (entity `specification`), over `<instance>/specs/*.md` and the template |
| `docs/writing.md` | the order a specification is written in, and each perspective's standard sections as prompts |
| `falsification/rules/specs.md` | the evaluation of #723 (the S1–S8 overlap map) and the attacks on both rules |
| `tests/` | the guard |

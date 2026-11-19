# Statements (specs craft, Tended rule)

Read by `../guards/specs.py` and by every writer of a specification. Terms: `../vocabulary/CRAFT.md`. Record:
`../falsification/rules/specs.md`. Source: dyad-system plan #723, revisions 1–3.

## 1. Every bullet is a statement
Inside a cell, every bullet (`- `) is a **statement**, and every statement ends with exactly one citation or one mark:
- `[cite: <ref>]` — the statement rests on what the reference holds;
- `[assumption]` — taken as true without a source, to be confirmed; the writer lists every one for the operator at the
  row's Done (`../docs/writing.md`);
- `[proposed]` — the writer's proposal, which the operator's `Y` to the row accepts or an amend corrects.

A line of a cell that is not a bullet is prose around the statements and carries nothing the guard reads; a cell's
`n/a: <reason>` line is its one statement and needs no citation.

## 2. What a citation may name
A `<ref>` is one of:
- a path in the repository, optionally followed by `#<heading>`;
- `#<id>`, a row of the ledger;
- `prov #<id> entry <n>`, one entry of a row's provenance record — the operator's own words;
- a release tag (`<craft>-vX.Y.Z`, `dyad-operator-vX.Y.Z`, or the bundle's `vX.Y.Z`);
- `ext: <url>`, anything outside the repository.

A citation **resolves** when its target exists: the path is in the tree, the row file exists, the provenance entry
exists, the tag is known to the clone. An `ext:` citation cannot be resolved by the guard and is read by inference,
stated, as every reference into the world is.

## 3. WHEN names a milestone, never an invented date
Every statement in a WHEN cell names at least one row (`#<id>`) or one release tag, in its text or its citation. A date
the operator gave is a statement cited to the operator's words (`[cite: prov #<id> entry <n>]`); the agent never writes
a date of its own.

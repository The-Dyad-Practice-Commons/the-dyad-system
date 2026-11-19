# Specification form (specs craft, Tended rule)

Read by `../guards/specs.py` and by every writer of a specification. Terms: `../vocabulary/CRAFT.md`. Record:
`../falsification/rules/specs.md`. Source: dyad-system plan #723, revisions 1–3.

## 1. One file per subject
A **specification** is one file per subject, `<instance>/specs/<subject>.md` (the instance location `DYAD_INSTANCE`,
default `agent-corpus`, Rule-11 property 3), `<subject>` lowercase words joined by `-`. It is written by one row of the
ledger and changed by later rows; its history is git's. The craft ships the form (`../templates/spec.md`), never a
specification: a system's specifications are its own instance.

## 2. Header
The file opens with `# Specification: <subject>`, then two `key: value` lines:
- `row: #<id>` — the row that wrote it, or that changes it now;
- `status: draft` or `status: accepted`.

## 3. Five questions in three perspectives
PRD, Architecture and UX/UI are three **perspectives** of the same product — the product's, the system's and the
user's — so every question is answered in every perspective. The file has five sections, in this order: `## WHAT`,
`## WHY`, `## HOW`, `## WHEN`, `## WHO`. Each has three subsections, in this order: `### PRD`, `### Architecture`,
`### UX/UI`. Each of the fifteen is a **cell**, and asks:

| | PRD (the product's perspective) | Architecture (the system's) | UX/UI (the user's) |
|---|---|---|---|
| **WHAT** | the requirements, each with its acceptance criterion | the components and the interfaces between them | the screens, steps and states the user meets |
| **WHY** | the problem and the value of solving it | the forces on the design and the choice made among them | the user's goal at each step |
| **HOW** | the approach: scope, non-goals, and how the product meets each requirement | the mechanism, citing the system's own engineering rules where they exist (in a dyad system, sysarch's) and never restating them | the interaction: what the user does and what the product answers |
| **WHEN** | the milestone each requirement is due at | the build and rollout sequence: what lands before what | the moment in the user's journey: what triggers each step |
| **WHO** | the users and segments | the owning unit, function or team | the personas |

## 4. A cell is never absent
A cell holds one or more statements (`statements.md`), or the one line `n/a: <reason>` when the subject truly lacks
it — a product with no user interface has no UX/UI screens. `n/a` is a statement about the subject, never about the
form: no cell is empty by design.

## 5. Accepted
`status: accepted` says that the operator verified the specification as it stands, by the done-`Y` of the row the
`row:` line names. It is written only in or after the commit that records that `Y`, and it records the `Y` already
given; it is never a question of its own. A later change returns the file to `status: draft` under the row making it,
until that row's done-`Y`.

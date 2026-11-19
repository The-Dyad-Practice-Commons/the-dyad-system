# Writing a specification (specs craft procedure)

A procedure, never a rule: the form is `../rules/specs.md` and `../rules/statements.md`, and the guard checks it. A
specification is written by one row, with the operator, in the unit the row runs in.

## Order
1. **WHY, then WHO**, in all three perspectives: the problem and the people before any answer. In a dyad system,
   cite the operator's own words (`prov #<id> entry <n>`) for the problem, and the instance's market records where they
   exist (the chronicle craft's lean canvas and segmentation) for the value and the segments.
2. **WHAT under PRD**, as requirements, each with its acceptance criterion. A requirement with no criterion is not
   yet a requirement.
3. **WHAT and HOW under Architecture**, then **under UX/UI**. Architecture cites the system's own engineering rules
   (sysarch in a dyad system) and restates none.
4. **HOW under PRD**: scope and non-goals, now that the other perspectives show what is in and out.
5. **WHEN last**, in all three perspectives, against the release plan (`dmc:release-plan` in a dyad system): each
   statement names the row or the release that delivers it.
6. **Cite as you write.** A statement written without its citation or mark is a guard failure, not a draft.

## Each perspective's standard sections, as prompts
The traditional documents' sections are prompts for the cells, never extra cells:
- **PRD:** problem, goals, non-goals, requirements, success metrics, open questions.
- **Architecture:** context, containers and components, interfaces, decisions and their alternatives, risks.
- **UX/UI:** journey, screens, states (empty, loading, error, success), errors and recovery, accessibility.

## At the Done
The writer's completion evidence lists every `[assumption]` statement by cell, so the operator confirms or corrects
each before the `Y`, and every `[proposed]` statement, which the `Y` accepts. After the `Y` is recorded the file may be
set `status: accepted` (`../rules/specs.md` §5).

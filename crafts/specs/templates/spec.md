# Specification: example

row: #<id>
status: draft

Copy this file to `<instance>/specs/<subject>.md`, set the subject and the row, and replace every statement. Each
statement ends with one citation or one mark (`../rules/statements.md`).

## WHAT

### PRD
- Requirement 1: what the product must do, with its acceptance criterion. [proposed]

### Architecture
- The components and the interfaces between them. [cite: crafts/specs/rules/specs.md]

### UX/UI
- The screens, steps and states the user meets. [assumption]

## WHY

### PRD
- The problem, and the value of solving it, in the operator's words. [cite: prov #<id> entry 1]

### Architecture
- The forces on the design, and the choice made among them. [proposed]

### UX/UI
- The user's goal at each step. [assumption]

## HOW

### PRD
- The approach: scope, non-goals, and how each requirement is met. [proposed]

### Architecture
- The mechanism, citing the system's own engineering rules rather than restating them. [cite: crafts/specs/docs/writing.md]

### UX/UI
- The interaction: what the user does and what the product answers. [assumption]

## WHEN

### PRD
- Requirement 1 is due at the row that builds it, #<id>. [proposed]

### Architecture
- The components land in the order of the rows that build them, starting at #<id>. [proposed]

### UX/UI
- The first step is triggered when the user starts the product, built by #<id>. [assumption]

## WHO

### PRD
- The users and segments the product serves. [assumption]

### Architecture
- The owning unit, function or team of each component. [proposed]

### UX/UI
- The personas, one per segment. [assumption]

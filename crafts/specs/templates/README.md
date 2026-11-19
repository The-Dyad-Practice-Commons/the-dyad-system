# specs templates

Seeds a writer copies (exempt from the instance-state scan).

| template | becomes |
|----------|---------|
| `spec.md` | `<instance>/specs/<subject>.md`, the subject and `row:` filled in; it passes `../guards/specs.py` as shipped, read as the form: its `#<id>` placeholders stand for rows and are not resolved |

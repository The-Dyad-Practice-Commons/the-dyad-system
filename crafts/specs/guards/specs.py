#!/usr/bin/env python3
"""Specification guard (entity `specification`, corpus `agent`; the specs craft's guard, its rules
`crafts/specs/rules/specs.md` and `crafts/specs/rules/statements.md`; placed per `crafts/sysarch/rules/guards.md` under
`crafts/specs/guards/`; d-work #723). Kernel: Python 3.12+.
Reads every `<instance>/specs/*.md` (`DYAD_INSTANCE`, default `agent-corpus`) and the craft's own template,
`crafts/specs/templates/spec.md`, and fails:
- a missing header: the title `# Specification: <subject>`, `row: #<id>`, or `status: draft|accepted`;
- a missing question (`## WHAT`, `## WHY`, `## HOW`, `## WHEN`, `## WHO`) or perspective (`### PRD`,
  `### Architecture`, `### UX/UI`) under it, or a cell (one question in one perspective, fifteen in all) holding
  neither a statement nor `n/a: <reason>`;
- a statement (a bullet of a cell) ending in no citation `[cite: <ref>]` and no mark, `[assumption]` or `[proposed]`;
- a citation that does not resolve: a repo path not in the tree (`<path>` or `<path>#<heading>`), a row with no row
  file (`#<id>`), a provenance entry its record lacks (`prov #<id> entry <n>`), or a release tag not held locally
  (`<craft>-vX.Y.Z`, `vX.Y.Z`); an `ext: <url>` citation gets one warning line, unresolvable as Rule-20 says of The
  World;
- a WHEN cell, in any perspective, whose statements name no row and no tag (a milestone is a release or a row, never a
  date the agent invents: plan #723 Q3, revision 3);
- `status: accepted` on a file whose row holds no `Y done`: acceptance is that done-`Y`, read from the row.
The template is read for shape alone — the title, both header lines present, the fifteen cells filled and every
statement ending in a citation or a mark — since its placeholders (`#<id>`, `<path>`) name nothing in any tree, and an
installing system holds none of this one's rows. An absent `<instance>/specs/` skips with one line (Rule-20 property 2's absent store); the template is checked
whatever the store holds. Left to inference, stated: whether a statement is true, and whether a citation supports it.
  specs.py [repo-root]
"""
import sys
if sys.version_info < (3, 12):
    sys.exit("specs.py: Python 3.12+ required")
import re, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "dyad" / "scripts"))   # crafts/specs/guards/ -> dyad/scripts
import dyadlib

ENTITY, CORPUS, TRANSACTION = "specification", "agent", False
CLERICAL_READS = ()   # d-work #564: no ledger or events path; on a clerical push the sweep (`--stores`) judges it, since it reads rows and tags
NAME, OWNER = "specification (one product subject in five questions and three perspectives)", "crafts/specs/rules/specs.md"
FIELDS = ("row", "status")                                          # the header's lines after the title
STATUSES = ("draft", "accepted")
QUESTIONS = ("WHAT", "WHY", "HOW", "WHEN", "WHO")                   # `## <question>`
LENSES = ("PRD", "Architecture", "UX/UI")                           # `### <perspective>` under each question
MARKS = ("assumption", "proposed")                                  # a statement's mark in place of a citation
STORE, TEMPLATE = "specs", Path(__file__).resolve().parents[1] / "templates" / "spec.md"
_TITLE = re.compile(r"# Specification: \S.*")
_ROW = re.compile(r"#(\d+)")
_TAG = re.compile(r"(?:[a-z0-9][a-z0-9-]*-)?v\d+\.\d+\.\d+")
_PROV = re.compile(r"prov #(\d+) entry (\d+)")
_END = re.compile(r"\[(?:cite: (?P<ref>[^\]]+)|(?P<mark>" + "|".join(MARKS) + r"))\]\s*$")
_NA = re.compile(r"n/a: \S")
_NAMES_MILESTONE = re.compile(r"(?<![\w&])#\d+\b|(?<![\w.-])(?:[a-z0-9][a-z0-9-]*-)?v\d+\.\d+\.\d+(?![\w.])")
INVARIANTS = [   # crafts/syseng/rules/invariants.md
    ("fifteen-cells", lambda: len(set(QUESTIONS)) * len(set(LENSES)) == 15),
    ("statuses-draft-and-accepted", lambda: STATUSES == ("draft", "accepted")),
    ("a-cite-and-a-mark-end-a-statement", lambda: bool(_END.search("- x [cite: #1]")) and bool(_END.search("- x [proposed]"))
     and not _END.search("- x [cite: #1] more")),
    ("a-tag-or-a-row-names-a-milestone", lambda: bool(_NAMES_MILESTONE.search("lands in v1.4.0"))
     and bool(_NAMES_MILESTONE.search("after #721")) and not _NAMES_MILESTONE.search("by 2026-12-01")),
]
dyadlib.enforce(INVARIANTS, __name__)

def parse(text: str) -> tuple[str, dict[str, str], dict[tuple[str, str], list[str]]]:
    """(title, header, cells): the first line, the `key: value` lines before the first `##`, and each
    (question, perspective) cell's non-blank lines, in order. A heading of neither kind is kept in no cell."""
    lines = text.splitlines()
    title = lines[0].strip() if lines else ""
    header, cells, q, lens = {}, {}, None, None
    for line in lines[1:]:
        s = line.rstrip()
        if s.startswith("## "):
            q, lens = s[3:].strip(), None
        elif s.startswith("### "):
            lens = s[4:].strip()
            if q is not None:
                cells.setdefault((q, lens), [])
        elif q is None:
            k, sep, v = s.partition(":")
            if sep and k.strip() in FIELDS:
                header[k.strip()] = v.strip()
        elif lens is not None and s.strip():
            cells[(q, lens)].append(s.strip())
    return title, header, cells

def statements(lines: list[str]) -> list[str]:
    """A cell's statements: its bullet lines (`- ` or `* `), the bullet dropped."""
    return [l[2:].strip() for l in lines if l.startswith(("- ", "* "))]

def tags(root: Path) -> set[str]:
    try:
        r = subprocess.run(["git", "tag", "--list"], cwd=root, capture_output=True, text=True, env=dyadlib.git_env(), timeout=60)
    except (OSError, subprocess.SubprocessError):
        return set()
    return set(r.stdout.split()) if r.returncode == 0 else set()

def resolve(ref: str, root: Path, held: set[str]) -> tuple[bool, str | None]:
    """(ok, note) for one citation: ok False is an unresolved citation; a note is a warning line's text."""
    ref = ref.strip()
    if ref.startswith("ext: "):
        return True, f"ext citation {ref[5:].strip()!r} unresolvable (The World), inference"
    if m := _PROV.fullmatch(ref):
        rec = dyadlib.instance(root) / "d-work" / "provenance" / f"{m[1]}.md"
        ok = rec.is_file() and re.search(rf"(?m)^## {m[2]} ", rec.read_text(errors="replace")) is not None
        return ok, None
    if m := _ROW.fullmatch(ref):
        return (dyadlib.rows_dir(root) / f"{m[1]}.md").is_file(), None
    if _TAG.fullmatch(ref):
        return ref in held, None
    path = ref.split("#", 1)[0].strip()
    return bool(path) and (root / path).exists() and not Path(path).is_absolute() and ".." not in Path(path).parts, None

def row_done(root: Path, rid: str) -> bool:
    p = dyadlib.rows_dir(root) / f"{rid}.md"
    if not p.is_file():
        return False
    rg = dyadlib.load_guard("agent", "rows")
    return any(rg.DONE_Y.search(e) for e in rg.entries(dyadlib.parse_row_file(p.read_text()).disposed))

def check_text(text: str, where: str, root: Path, held: set[str] | None = None, template: bool = False) -> list[str]:
    """Every problem of one specification's text, failures plain and warnings `warning: `-prefixed; under `template`
    its shape alone (the module's docstring)."""
    held = set() if template else (tags(root) if held is None else held)
    title, header, cells = parse(text)
    msgs = []
    if not _TITLE.fullmatch(title):
        msgs.append(f"{where}: does not open with `# Specification: <subject>` (rules/specs.md)")
    row = header.get("row", "")
    if template:
        msgs += [f"{where}: lacks the header line `{k}:` (rules/specs.md)" for k in FIELDS if k not in header]
    elif not _ROW.fullmatch(row):
        msgs.append(f"{where}: lacks `row: #<id>`, the row that writes it (rules/specs.md)")
    elif not (dyadlib.rows_dir(root) / f"{row[1:]}.md").is_file():
        msgs.append(f"{where}: row {row} has no row file (rules/specs.md)")
    status = header.get("status", "")
    if template:
        pass
    elif status not in STATUSES:
        msgs.append(f"{where}: status {status!r} is not draft or accepted (rules/specs.md)")
    elif status == "accepted" and _ROW.fullmatch(row) and not row_done(root, row[1:]):
        msgs.append(f"{where}: status accepted, but row {row} holds no `Y done`; acceptance is that done-Y (rules/specs.md)")
    for q in QUESTIONS:
        for lens in LENSES:
            cell = f"{q} / {lens}"
            if (q, lens) not in cells:
                msgs.append(f"{where}: lacks the cell {cell} (`## {q}` with `### {lens}`; rules/specs.md)")
                continue
            lines = cells[(q, lens)]
            stmts = statements(lines)
            na = any(_NA.match(l) for l in lines)
            if not stmts and not na:
                msgs.append(f"{where}: cell {cell} holds no statement and no `n/a: <reason>` (rules/specs.md)")
                continue
            for s in stmts:
                m = _END.search(s)
                if not m:
                    msgs.append(f"{where}: {cell}: statement {s[:60]!r} ends in no citation or mark "
                                f"(`[cite: <ref>]`, `[assumption]`, `[proposed]`; rules/statements.md)")
                elif m["ref"] and not template:
                    ok, note = resolve(m["ref"], root, held)
                    if not ok:
                        msgs.append(f"{where}: {cell}: citation {m['ref'].strip()!r} does not resolve (rules/statements.md)")
                    elif note:
                        msgs.append(f"warning: {where}: {cell}: {note}")
            if q == "WHEN" and not template and stmts and not any(_NAMES_MILESTONE.search(s) for s in stmts):
                msgs.append(f"{where}: {cell}: names no row and no release tag; a milestone is a release or a row, "
                            f"never a date (rules/specs.md)")
    return msgs

def specs(root: Path) -> list[Path]:
    d = dyadlib.instance(root) / STORE
    return sorted(d.glob("*.md")) if d.is_dir() else []

def check_package(root: Path | None = None, pkg: Path = dyadlib.PKG) -> list[str]:
    root = root or dyadlib.repo_root()
    held, msgs = tags(root), []
    if TEMPLATE.is_file():
        msgs += check_text(TEMPLATE.read_text(errors="replace"), "crafts/specs/templates/spec.md", root, template=True)
    else:
        msgs.append("crafts/specs/templates/spec.md: the template is missing (rules/specs.md)")
    if not (dyadlib.instance(root) / STORE).is_dir():
        msgs.append(f"warning: skip specifications: no <instance>/{STORE}/ store")
    for p in specs(root):
        msgs += check_text(p.read_text(errors="replace"), p.relative_to(root).as_posix(), root, held)
    return msgs

def summary(root: Path | None = None, pkg: Path = dyadlib.PKG) -> str:
    return f"{len(specs(root or dyadlib.repo_root()))} specification(s) and the template"

def describe(root: Path, pkg: Path = dyadlib.PKG) -> dict:
    return {"store": f"<instance>/{STORE}/<subject>.md", "parser": "`specs.parse`", "observed": len(specs(root)),
            "note": "fifteen cells: " + ", ".join(QUESTIONS) + " in each of " + ", ".join(LENSES),
            "fields": [("row", "text", "#<id>, a row file", True, "", "specs.FIELDS"),
                       ("status", "text", " | ".join(STATUSES), True, "", "specs.FIELDS")]}

def main(a: list[str]) -> int:
    root = Path(a[0]).resolve() if a else dyadlib.repo_root()
    msgs = check_package(root)
    for m in msgs:
        print(m)
    bad = [m for m in msgs if not m.startswith("warning:")]
    print(f"{'FAIL' if bad else 'ok  '} [specs/specs] {summary(root)}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

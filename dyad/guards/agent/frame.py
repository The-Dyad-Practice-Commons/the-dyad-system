#!/usr/bin/env python3
"""Frame guard (entity `frame`, agent corpus; the operating frame `dyad/CLAUDE.md` is the frame's own,
the guard placed per Rule-11 property 1). Kernel: Python 3.12+.
Every `@rules/<file>` import of the frame names an existing Rule file and every Rule file
(`dyadlib.rule_files`) is imported (the #137 gap: two Rules unimported for a day); every other `@`
import resolves relative to the package root (`@vocabulary/...`, `@../preferences-corpus/...`).
An absent import inside the craft root fails — the #137 gap is a craft that names its own file and
does not carry it. An absent import that resolves *outside* the craft root (a `../` path:
`@../preferences-corpus/PREFERENCES.md`, instance state) only warns: the reference distribution ships
no instance by design, and a fresh install writes its preferences after it installs the craft
(d-work #5). The warning carries the `warning:` prefix the runner reads (#519).
Formerly Rule-20's reference kinds 12 and 13 (`references.py` lists them as `guard:agent/frame.py`).
  frame.py [repo-root]
"""
import sys
if sys.version_info < (3, 12):
    sys.exit("frame.py: Python 3.12+ required")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import dyadlib

ENTITY, CORPUS, TRANSACTION = "frame", "agent", False
NAME, OWNER = "operating frame", "frame (Rule-11 property 2 places the host's import line)"
FIELDS = ("@rules/", "@")           # Rule imports; every other import (vocabulary, preferences)
INVARIANTS = [("rule-import-prefix-first", lambda: FIELDS[0] == "@rules/" and FIELDS[1] == "@")]   # crafts/syseng/rules/invariants.md

def imports(text: str) -> list[str]:
    return [l.strip()[1:] for l in text.splitlines() if l.startswith("@")]

def inside(pkg: Path, i: str) -> bool:
    """Does the import `i` resolve inside the craft root `pkg`? Lexically (`normpath`, no symlink
    resolution and no filesystem read), so an absent path is classed the same as a present one."""
    import os
    target = Path(os.path.normpath(pkg / i))
    return target.is_relative_to(Path(os.path.normpath(pkg)))

def check(frame_text: str, rules: dict[int, Path], pkg: Path) -> list[str]:
    imps = imports(frame_text); fails = []
    rule_imps = {i for i in imps if i.startswith("rules/")}
    for i in imps:
        if not (pkg / i).exists():
            if inside(pkg, i):
                fails.append(f"CLAUDE.md imports `@{i}` which does not exist")
            else:   # outside the craft root: instance state the distribution omits by design (#5)
                fails.append(f"warning: CLAUDE.md imports `@{i}` which does not exist; it resolves outside "
                             f"the craft root, so it is instance state this checkout may not carry")
    for n, p in sorted(rules.items()):
        if f"rules/{p.name}" not in rule_imps:
            fails.append(f"CLAUDE.md does not import `@rules/{p.name}` (Rule-{n})")
    return fails

def check_package(root: Path | None = None, pkg: Path = dyadlib.PKG) -> list[str]:
    frame = pkg / "CLAUDE.md"
    if not frame.exists():
        return ["CLAUDE.md missing (the frame)"]
    return check(frame.read_text(), dyadlib.rule_files(pkg), pkg)

def summary(root: Path | None = None, pkg: Path = dyadlib.PKG) -> str:
    imps = imports((pkg / "CLAUDE.md").read_text()) if (pkg / "CLAUDE.md").exists() else []
    return f"{len(imps)} imports, {sum(i.startswith('rules/') for i in imps)} Rules"

def describe(root: Path, pkg: Path = dyadlib.PKG) -> dict:
    frame = pkg / "CLAUDE.md"
    imps = imports(frame.read_text()) if frame.exists() else []
    rel = frame.relative_to(root) if frame.is_relative_to(root) else frame
    return {"store": str(rel), "parser": "`frame.imports`", "observed": 1 if frame.exists() else 0,
            "note": "loaded at session start; the sentinel proves it (Rule-3); every Rule file is imported",
            "fields": [("@rules/", "path", "one line per Rule file; all of `dyad/rules/` imported", True, next((i for i in imps if i.startswith("rules/")), ""), "frame.FIELDS"),
                       ("@", "path", "package-relative (`vocabulary/…`, `../preferences-corpus/…`)", True, next((i for i in imps if not i.startswith("rules/")), ""), "frame.FIELDS")]}

def main(argv=None) -> int:
    msgs = check_package()
    fails = [m for m in msgs if not m.startswith("warning:")]
    for m in msgs:
        if m.startswith("warning:"):
            print(f"warn [frame] {m.removeprefix('warning:').strip()}", file=sys.stderr)
    for f in fails:
        print(f"FAIL [frame] {f}", file=sys.stderr)
    if not fails:
        print(f"ok   [frame] {summary()} resolve")
    return 1 if fails else 0

dyadlib.enforce(INVARIANTS, __name__)   # Rule-12 p1: the fail-loud check, at import (crafts/syseng/rules/invariants.md p1, #203)

if __name__ == "__main__":
    sys.exit(main())

"""specs.py (the specs craft's guard, entity `specification`; d-work #723): a well-formed specification passes; a missing
header line, question or perspective, an empty cell, an uncited statement, an unresolved path, row, provenance entry
or tag, a WHEN cell naming no row and no tag, and `status: accepted` without a `Y done` each fail; `n/a: <reason>` fills
a cell; an `ext:` citation warns; the template is read for shape alone; an absent store skips with one line; the
invariants."""
import os, shutil, sys, tempfile, unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "dyad" / "scripts"))
import dyadlib
CRAFT = Path(__file__).resolve().parents[2]
specs = dyadlib.load_guard_file(CRAFT / "guards" / "specs.py")

ROW = "id: {i}\ntitle: t\nopened: 2026-11-15\nstate: open\ndisposed: {d}\nrefs: \n"

def spec(status="draft", row="#5", cells=None, drop=()) -> str:
    cells = cells or {}
    out = ["# Specification: a subject", f"row: {row}", f"status: {status}", ""]
    for q in specs.QUESTIONS:
        if q in drop:
            continue
        out.append(f"## {q}")
        for lens in specs.LENSES:
            if (q, lens) in drop:
                continue
            out += [f"### {lens}", cells.get((q, lens), f"- it lands with #5 [cite: #5]"), ""]
    return "\n".join(out) + "\n"

class Spec(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp()); self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        rows = self.root / "agent-corpus" / "d-work" / "rows"; rows.mkdir(parents=True)
        (rows / "5.md").write_text(ROW.format(i=5, d="2026-11-15 Y plan"))
        (rows / "6.md").write_text(ROW.format(i=6, d="2026-11-15 Y plan; 2026-11-16 Y done (merges PR #1 at abc)"))
        prov = self.root / "agent-corpus" / "d-work" / "provenance"; prov.mkdir()
        (prov / "5.md").write_text("# Provenance #5\n\n## 1 prompt 2026-11-15\n\n```\nhi\n```\n")
        (self.root / "docs").mkdir(); (self.root / "docs" / "a.md").write_text("# A\n")
        env = {k: v for k, v in os.environ.items() if k != "DYAD_INSTANCE"}
        p = mock.patch.dict(os.environ, env, clear=True); p.start(); self.addCleanup(p.stop)

    def check(self, text, held=frozenset({"specs-v0.1.0"}), template=False):
        return specs.check_text(text, "s.md", self.root, set(held), template=template)

    def fails(self, msgs):
        return [m for m in msgs if not m.startswith("warning:")]

    def test_well_formed_passes(self):
        self.assertEqual(self.check(spec()), [])

    def test_every_citation_kind_resolves(self):
        cells = {("WHAT", "PRD"): "- a path [cite: docs/a.md#A]\n- a provenance entry [cite: prov #5 entry 1]\n"
                                  "- a tag [cite: specs-v0.1.0]\n- a mark [assumption]\n* another [proposed]",
                 ("WHEN", "UX/UI"): "- ships in specs-v0.1.0 [proposed]"}
        self.assertEqual(self.check(spec(cells=cells)), [])

    def test_n_a_fills_a_cell(self):
        self.assertEqual(self.check(spec(cells={("WHO", "UX/UI"): "n/a: no interface"})), [])

    def test_missing_header_lines_fail(self):
        text = spec().replace("# Specification: a subject", "# A subject").replace("row: #5\n", "").replace("draft", "final")
        msgs = self.fails(self.check(text))
        self.assertTrue(any("`# Specification:" in m for m in msgs))
        self.assertTrue(any("lacks `row: #<id>`" in m for m in msgs))
        self.assertTrue(any("is not draft or accepted" in m for m in msgs))

    def test_row_without_a_row_file_fails(self):
        self.assertTrue(any("row #9 has no row file" in m for m in self.check(spec(row="#9"))))

    def test_missing_question_and_perspective_fail(self):
        msgs = self.check(spec(drop=("WHY", ("HOW", "UX/UI"))))
        self.assertEqual(sum("lacks the cell WHY /" in m for m in msgs), 3)
        self.assertTrue(any("lacks the cell HOW / UX/UI" in m for m in msgs))

    def test_empty_cell_fails(self):
        self.assertTrue(any("cell WHAT / PRD holds no statement" in m
                            for m in self.check(spec(cells={("WHAT", "PRD"): "prose, no bullet"}))))

    def test_uncited_statement_fails(self):
        msgs = self.check(spec(cells={("WHAT", "PRD"): "- a bare claim\n- trailing [cite: #5] words"}))
        self.assertEqual(sum("ends in no citation or mark" in m for m in msgs), 2)

    def test_unresolved_citations_fail(self):
        for ref in ("docs/missing.md", "../etc/passwd", "#9", "prov #5 entry 2", "prov #7 entry 1", "specs-v9.9.9"):
            with self.subTest(ref=ref):
                msgs = self.check(spec(cells={("WHAT", "PRD"): f"- x [cite: {ref}]"}))
                self.assertTrue(any(f"citation {ref!r} does not resolve" in m for m in msgs), msgs)

    def test_ext_citation_warns(self):
        msgs = self.check(spec(cells={("WHY", "PRD"): "- market [cite: ext: https://example.com/a]"}))
        self.assertEqual(self.fails(msgs), [])
        self.assertTrue(any(m.startswith("warning:") and "The World" in m for m in msgs))

    def test_when_naming_no_row_and_no_tag_fails_in_every_perspective(self):
        for lens in specs.LENSES:
            with self.subTest(lens=lens):
                msgs = self.check(spec(cells={("WHEN", lens): "- by 2026-12-01 [proposed]"}))
                self.assertTrue(any(f"WHEN / {lens}: names no row and no release tag" in m for m in msgs), msgs)

    def test_accepted_needs_a_y_done(self):
        self.assertTrue(any("holds no `Y done`" in m for m in self.check(spec(status="accepted"))))
        self.assertEqual(self.check(spec(status="accepted", row="#6")), [])

    def test_template_is_read_for_shape_alone(self):
        text = spec(row="#<id>", status="draft | accepted",
                    cells={("WHAT", "PRD"): "- <statement> [cite: <path>]", ("WHEN", "PRD"): "- <milestone> [proposed]"})
        self.assertEqual(self.check(text, template=True), [])
        msgs = self.check(text.replace("row: #<id>\n", "").replace("- <statement> [cite: <path>]", "- <statement>"),
                          template=True)
        self.assertTrue(any("lacks the header line `row:`" in m for m in msgs))
        self.assertTrue(any("ends in no citation or mark" in m for m in msgs))

    def test_absent_store_skips_with_one_line_and_the_store_is_read(self):
        tpl = self.root / "spec.md"; tpl.write_text(spec(row="#<id>"))
        with mock.patch.object(specs, "TEMPLATE", tpl):
            self.assertEqual(specs.check_package(self.root), ["warning: skip specifications: no <instance>/specs/ store"])
            d = self.root / "agent-corpus" / "specs"; d.mkdir(); (d / "x.md").write_text(spec(row="#9"))
            msgs = specs.check_package(self.root)
        self.assertTrue(any(m.startswith("agent-corpus/specs/x.md: row #9") for m in msgs), msgs)

    def test_missing_template_fails(self):
        with mock.patch.object(specs, "TEMPLATE", self.root / "nope.md"):
            self.assertTrue(any("the template is missing" in m for m in specs.check_package(self.root)))

    def test_invariants_hold(self):
        self.assertEqual(dyadlib.enforce(specs.INVARIANTS, "specs"), len(specs.INVARIANTS))

if __name__ == "__main__":
    unittest.main()

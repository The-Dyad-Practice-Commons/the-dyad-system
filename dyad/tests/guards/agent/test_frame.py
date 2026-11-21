"""Frame guard tests (agent/frame.py): every `@rules/` import exists and every Rule file is imported
(the #137 gap), every other `@` import resolves; the live frame passes. An absent import that resolves
outside the craft root is instance state the distribution omits by design, so it warns rather than
fails (d-work #5); an absent import inside the root still fails, which is the #137 gap itself."""
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import dyadlib
fr = dyadlib.load_guard("agent", "frame")

def fixture(frame: str):
    pkg = Path(tempfile.mkdtemp()) / "dyad"; (pkg / "rules").mkdir(parents=True); (pkg / "vocabulary").mkdir()
    for n in (1, 2): (pkg / "rules" / f"RULE-{n}-x.md").write_text(f"# Rule-{n}\n")
    (pkg / "vocabulary" / "VOCABULARY.md").write_text("| term |\n"); (pkg.parent / "preferences-corpus").mkdir(); (pkg.parent / "preferences-corpus" / "PREFERENCES.md").write_text("p\n")
    (pkg / "CLAUDE.md").write_text(frame); return pkg

GOOD = "# frame\n@rules/RULE-1-x.md\n@rules/RULE-2-x.md\n\n@vocabulary/VOCABULARY.md\n@../preferences-corpus/PREFERENCES.md\n"

class FrameTests(unittest.TestCase):
    def test_good_frame_passes(self):
        pkg = fixture(GOOD); self.assertEqual(fr.check_package(pkg.parent, pkg), [])
        self.assertEqual(fr.imports(GOOD), ["rules/RULE-1-x.md", "rules/RULE-2-x.md", "vocabulary/VOCABULARY.md", "../preferences-corpus/PREFERENCES.md"])
    def test_missing_rule_file_fails(self):
        pkg = fixture(GOOD.replace("@rules/RULE-2-x.md", "@rules/RULE-3-x.md"))
        msgs = fr.check_package(pkg.parent, pkg)
        self.assertEqual(len(msgs), 2, msgs); self.assertIn("`@rules/RULE-3-x.md` which does not exist", msgs[0]); self.assertIn("does not import `@rules/RULE-2-x.md` (Rule-2)", msgs[1])
    def test_unimported_rule_fails(self):
        pkg = fixture(GOOD.replace("@rules/RULE-2-x.md\n", ""))
        msgs = fr.check_package(pkg.parent, pkg); self.assertEqual(len(msgs), 1); self.assertIn("(Rule-2)", msgs[0])
    def test_other_import_must_resolve(self):
        pkg = fixture(GOOD.replace("@vocabulary/VOCABULARY.md", "@vocabulary/NOPE.md"))
        msgs = fr.check_package(pkg.parent, pkg); self.assertEqual(len(msgs), 1); self.assertIn("`@vocabulary/NOPE.md`", msgs[0])
    def test_absent_import_outside_the_craft_root_only_warns(self):
        """d-work #5: the reference distribution ships no instance, so `@../preferences-corpus/PREFERENCES.md`
        cannot resolve there and the guard failed every contributor's push. It warns instead — with the
        `warning:` prefix the runner reads as a warning (#519) — and the frame otherwise passes."""
        pkg = fixture(GOOD); (pkg.parent / "preferences-corpus" / "PREFERENCES.md").unlink()
        msgs = fr.check_package(pkg.parent, pkg)
        self.assertEqual(len(msgs), 1, msgs)
        self.assertTrue(msgs[0].startswith("warning: "), msgs[0])
        self.assertIn("`@../preferences-corpus/PREFERENCES.md`", msgs[0])
        self.assertEqual([m for m in msgs if not m.startswith("warning:")], [])   # nothing the runner fails on
    def test_absent_import_inside_the_craft_root_still_fails(self):
        """The #137 gap: a craft that names its own file and does not carry it. Not a warning."""
        pkg = fixture(GOOD); (pkg / "vocabulary" / "VOCABULARY.md").unlink()
        msgs = fr.check_package(pkg.parent, pkg)
        self.assertEqual(len(msgs), 1, msgs)
        self.assertFalse(msgs[0].startswith("warning:"), msgs[0])
        self.assertIn("`@vocabulary/VOCABULARY.md` which does not exist", msgs[0])
    def test_inside_classifies_lexically(self):
        pkg = fixture(GOOD)
        self.assertTrue(fr.inside(pkg, "vocabulary/VOCABULARY.md")); self.assertTrue(fr.inside(pkg, "rules/RULE-1-x.md"))
        self.assertFalse(fr.inside(pkg, "../preferences-corpus/PREFERENCES.md"))
        self.assertFalse(fr.inside(pkg, "../nope/NOPE.md"))              # absent either way: classed the same
    def test_missing_frame_fails(self):
        pkg = fixture(GOOD); (pkg / "CLAUDE.md").unlink(); self.assertEqual(fr.check_package(pkg.parent, pkg), ["CLAUDE.md missing (the frame)"])

if __name__ == "__main__":
    unittest.main()

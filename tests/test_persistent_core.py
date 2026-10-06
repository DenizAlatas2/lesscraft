"""Check packaged examples and preservation fixtures, not an installer or host.

The guarded replacement below models the documented manual review contract.
It does not establish that an agent will follow it or that a host loads it.
"""

from pathlib import Path
import re
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/lesscraft"
CORE = (PACKAGE / "core.md").read_bytes()
GUIDE = (PACKAGE / "references/persistent-core.md").read_text()
EXAMPLES = re.findall(r"```text\n(.*?)\n```", GUIDE, re.S)
START = b"<!-- lesscraft:core:start -->"
END = b"<!-- lesscraft:core:end -->"


def codex_example(core=CORE, revision="a" * 40):
    return EXAMPLES[0].replace("FULL_COMMIT", revision).encode().replace(
        b"VERBATIM_CORE\n", core
    )


def reviewed_replacement(document, expected, replacement):
    """A fixture-only byte guard for the guide's reviewed replacement rule."""
    if document.count(START) != 1 or document.count(END) != 1:
        raise ValueError("Review ambiguous markers")
    if document.count(expected) != 1:
        raise ValueError("Review local edits against the previous source")
    return document.replace(expected, replacement, 1)


class PersistentCoreTests(unittest.TestCase):
    def test_core_is_in_the_copyable_package_and_linked_from_skill(self):
        skill = (PACKAGE / "SKILL.md").read_text()
        self.assertIn("[the core](core.md)", skill)
        self.assertTrue(CORE.endswith(b"\n"))
        self.assertEqual(len(EXAMPLES), 3)
        self.assertIn(CORE, codex_example())
        self.assertNotIn(b"VERBATIM_CORE", codex_example())

    def test_all_local_markdown_links_have_targets(self):
        for source in [ROOT / "README.md", *PACKAGE.rglob("*.md")]:
            for target in re.findall(r"\]\(([^)]+)\)", source.read_text()):
                path = target.split("#", 1)[0]
                if not path or "://" in path:
                    continue
                self.assertTrue((source.parent / path).exists(), (source, target))

    def test_codex_example_preserves_other_instructions_and_removes_cleanly(self):
        original = b"# Team rules\r\nKeep npm pinned.\r\nUser text without final newline"
        inserted = b"\n\n" + codex_example()
        later = b"\n\n# Later team rule\nKeep the release checklist.\n"
        installed = original + inserted + later
        updated = reviewed_replacement(installed, codex_example(),
                                       codex_example(CORE + b"A reviewed update.\n", "b" * 40))
        self.assertTrue(updated.startswith(original))
        self.assertTrue(updated.endswith(later))
        removed = reviewed_replacement(installed, inserted, b"")
        self.assertEqual(removed, original + later)

    def test_codex_override_fixture_changes_only_the_selected_effective_file(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            normal = home / "AGENTS.md"
            override = home / "AGENTS.override.md"
            normal.write_bytes(b"Normal user instructions\n")
            override.write_bytes(b"Explicit override instructions\n")
            # This fixture declares the nonempty override as effective.
            # It is not an implementation of Codex's instruction discovery.
            before = override.read_bytes()
            override.write_bytes(before + b"\n" + codex_example())
            self.assertEqual(normal.read_bytes(), b"Normal user instructions\n")
            self.assertEqual(override.read_bytes(), before + b"\n" + codex_example())

    def test_claude_import_examples_resolve_from_the_instruction_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cases = [(root / "home/.claude/CLAUDE.md", EXAMPLES[1]),
                     (root / "project/CLAUDE.md", EXAMPLES[2]),
                     (root / "project/.claude/CLAUDE.md", EXAMPLES[1])]
            for instructions, example in cases:
                import_line = next(line for line in example.splitlines() if line.startswith("@"))
                target = instructions.parent / import_line[1:]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(CORE)
                original = b"# Existing Claude instructions\nKeep project terminology.\n"
                instructions.write_bytes(original + b"\n" + example.encode())
                self.assertEqual(target.read_bytes(), CORE)
                self.assertTrue(instructions.read_bytes().startswith(original))
                self.assertNotIn(b"```", instructions.read_bytes())
                self.assertEqual(reviewed_replacement(instructions.read_bytes(),
                                                     b"\n" + example.encode(), b""), original)

    def test_update_and_removal_require_unchanged_unique_sections(self):
        old = codex_example()
        new = codex_example(CORE + b"Reviewed update.\n", "b" * 40)
        original = b"Unrelated rule.\n" + old + b"\nLater user edit."
        self.assertEqual(reviewed_replacement(original, old, new),
                         b"Unrelated rule.\n" + new + b"\nLater user edit.")
        conflicts = [original.replace(CORE, CORE + b"Local preference.\n"),
                     original + old, original.replace(END, b""),
                     original.replace(b"a" * 40, b"c" * 40)]
        for current in conflicts:
            for replacement in (new, b""):
                with self.subTest(current=current[-100:], removal=not replacement):
                    with self.assertRaises(ValueError):
                        reviewed_replacement(current, old, replacement)

    def test_new_claude_file_example_preserves_existing_agents_guidance(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            existing = b"# Existing shared instructions\nKeep the public API stable.\n"
            (project / "AGENTS.md").write_bytes(existing)
            core = project / ".claude/skills/lesscraft/core.md"
            core.parent.mkdir(parents=True)
            core.write_bytes(CORE)
            example = "@AGENTS.md\n\n" + EXAMPLES[2]
            self.assertIn("@AGENTS.md", GUIDE)
            (project / "CLAUDE.md").write_text(example)
            imports = [project / line[1:] for line in example.splitlines()
                       if line.startswith("@")]
            self.assertEqual([path.read_bytes() for path in imports], [existing, CORE])
            self.assertEqual((project / "AGENTS.md").read_bytes(), existing)


if __name__ == "__main__":
    unittest.main()

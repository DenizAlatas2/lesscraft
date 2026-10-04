"""Check the documented file copy, not live agent-host discovery."""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/lesscraft"


class InstallPackageTests(unittest.TestCase):
    def test_package_retains_license(self):
        self.assertEqual((PACKAGE / "LICENSE").read_bytes(),
                         (ROOT / "LICENSE").read_bytes())

    def test_documented_copy_is_complete_and_preserves_existing_install(self):
        readme = (ROOT / "README.md").read_text()
        block = re.search(r"```sh\n(.*?)\n```", readme, re.S).group(1)
        # Test only the local installation section, without fetching a repository.
        commands = block[block.index("# Codex: personal skill"):]
        with tempfile.TemporaryDirectory() as home:
            env = {**os.environ, "HOME": home}
            first = subprocess.run(["sh", "-c", commands], cwd=ROOT, env=env,
                                   capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            expected = {p.relative_to(PACKAGE): p.read_bytes()
                        for p in PACKAGE.rglob("*") if p.is_file()}
            destinations = [Path(home) / host / "skills/lesscraft"
                            for host in (".agents", ".claude")]
            for destination in destinations:
                actual = {p.relative_to(destination): p.read_bytes()
                          for p in destination.rglob("*") if p.is_file()}
                self.assertEqual(actual, expected)
                self.assertIn(Path("SKILL.md"), actual)
                (destination / "SKILL.md").write_text("Existing local changes\n")
            # Existing destinations make the README's guard return nonzero.
            second = subprocess.run(["sh", "-c", commands], cwd=ROOT, env=env,
                                    capture_output=True, text=True)
            self.assertEqual(second.returncode, 1, second.stderr)
            for destination in destinations:
                self.assertEqual((destination / "SKILL.md").read_text(),
                                 "Existing local changes\n")
                self.assertFalse((destination / "lesscraft").exists())


if __name__ == "__main__":
    unittest.main()

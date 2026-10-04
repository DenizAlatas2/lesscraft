"""Exercise the public CLI against real, temporary Git repositories."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/lesscraft/scripts/scope_check.py"


class ScopeCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.write("src/old.txt", b"original\n")
        self.write("exact.txt", b"original\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Base fixture")
        self.base = self.git("rev-parse", "HEAD").decode().strip()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE)

    def write(self, path, data):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Changed fixture")
        return self.git("rev-parse", "HEAD").decode().strip()

    def run_check(self, *extra, payload=None, env=None):
        command = [sys.executable, str(SCRIPT), "--repo", str(self.repo),
                   "--base", self.base, "--head", "HEAD", *extra]
        result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
                                text=True, capture_output=True, env=env)
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_exact_paths_directory_boundary_and_literal_glob(self):
        for path in ["src/new.txt", "src-other/new.txt", "exact.txt", "exact.txt.extra", "literal*.txt"]:
            self.write(path, b"changed\n")
        head = self.commit()
        code, result = self.run_check("--allow", "src/", "--allow", "exact.txt", "--allow", "literal*.txt")
        self.assertEqual(code, 1)
        self.assertEqual(result["head"], head)
        self.assertEqual(result["base"], self.base)
        self.assertEqual([c["path"] for c in result["changes"] if not c["allowed"]],
                         ["exact.txt.extra", "src-other/new.txt"])

    def test_nonempty_allowed_diff_passes(self):
        self.write("src/new.txt", b"new")
        self.commit()
        code, result = self.run_check("--allow", "src/")
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "within_scope")
        self.assertEqual(len(result["changes"]), 1)

    def test_malformed_hook_payload_is_report_only(self):
        command = [sys.executable, str(SCRIPT), "--repo", str(self.repo),
                   "--base", self.base, "--head", "HEAD", "--allow", "src/", "--hook"]
        result = subprocess.run(command, input="{broken", text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertIn("not_checked", json.loads(result.stdout)["systemMessage"])

    def test_other_repository_cwd_is_not_checked(self):
        other = Path(self.temp.name) / "other"
        other.mkdir()
        subprocess.check_call(["git", "-C", str(other), "init", "-q"])
        code, result = self.run_check("--allow", "src/", "--hook",
                                      payload={"hook_event_name": "Stop", "cwd": str(other)})
        self.assertEqual(code, 0)
        self.assertIn("not_checked", result["systemMessage"])

    def test_move_checks_both_sides_binary_and_newline(self):
        (self.repo / "src/old.txt").rename(self.repo / "moved.txt")
        self.write("src/binary", b"\x00\xff\x00")
        self.write("src/line\nbreak", b"new\n")
        self.commit()
        code, result = self.run_check("--allow", "src/")
        self.assertEqual(code, 1)
        changes = {c["path"]: (c["status"], c["allowed"]) for c in result["changes"]}
        self.assertEqual(changes["src/old.txt"], ("D", True))
        self.assertEqual(changes["moved.txt"], ("A", False))
        self.assertEqual(changes["src/binary"], ("A", True))
        self.assertIn("src/line\nbreak", changes)
        code, result = self.run_check("--allow", "moved.txt", "--allow", "src/binary", "--allow", "src/line\nbreak")
        self.assertEqual(code, 1)
        self.assertEqual([c["path"] for c in result["changes"] if not c["allowed"]], ["src/old.txt"])

    def test_invalid_inputs_never_pass(self):
        cases = [("--allow", "src/", "--base", "missing-ref"),
                 ("--allow", "src/", "--head=-bad"),
                 ("--allow", "src/", "--head", "HEAD:src"),
                 ("--allow", "../outside"), ("--allow", "/absolute"),
                 ("--allow", "src//"), ("--allow", ""), ()]
        for args in cases:
            with self.subTest(args=args):
                code, result = self.run_check(*args)
                self.assertEqual(code, 2)
                self.assertEqual(result["status"], "not_checked")

    def test_dirty_worktree_and_index_unchanged_and_omitted(self):
        self.write("exact.txt", b"staged")
        self.git("add", "exact.txt")
        self.write("exact.txt", b"unstaged")
        self.write("untracked", b"untracked")
        before = self.git("status", "--porcelain=v1", "-z")
        index = (self.repo / ".git/index").read_bytes()
        code, result = self.run_check("--allow", "src/")
        self.assertEqual(code, 0)
        self.assertEqual(result["changes"], [])
        self.assertIn("untracked", result["limitation"])
        self.assertEqual(self.git("status", "--porcelain=v1", "-z"), before)
        self.assertEqual((self.repo / ".git/index").read_bytes(), index)
        self.assertEqual((self.repo / "exact.txt").read_bytes(), b"unstaged")
        self.assertEqual((self.repo / "untracked").read_bytes(), b"untracked")

    def test_both_host_stop_payloads_are_report_only(self):
        for host in ("claude", "codex"):
            payload = {"hook_event_name": "Stop", "cwd": str(self.repo / "src"),
                       "session_id": "fixture", "stop_hook_active": False,
                       "last_assistant_message": "Done"}
            if host == "codex":
                payload["turn_id"] = "fixture-turn"
            code, result = self.run_check("--allow", "src/", "--hook", payload=payload)
            self.assertEqual(code, 0)
            self.assertEqual(set(result), {"systemMessage"})
            self.assertIn("within_scope", result["systemMessage"])
            payload["stop_hook_active"] = True
            payload["cwd"] = self.temp.name
            code, result = self.run_check("--allow", "src/", "--hook", payload=payload)
            self.assertEqual(code, 0)
            self.assertIn("not_checked", result["systemMessage"])
        for payload in ({}, [], {"hook_event_name": "PostToolUse"}):
            code, result = self.run_check("--allow", "src/", "--hook", payload=payload)
            self.assertEqual(code, 0)
            self.assertIn("not_checked", result["systemMessage"])

    def test_hook_errors_and_truncation(self):
        code, result = self.run_check("--hook", payload={})
        self.assertEqual(code, 0)
        self.assertIn("not_checked", result["systemMessage"])
        for i in range(40):
            self.write(f"outside/{i:02d}-long-fixture-name.txt", b"new")
        self.commit()
        payload = {"hook_event_name": "Stop", "cwd": str(self.repo)}
        code, result = self.run_check("--allow", "src/", "--hook", payload=payload)
        self.assertEqual(code, 0)
        self.assertIn("out_of_scope", result["systemMessage"])
        self.assertIn("truncated", result["systemMessage"])
        self.assertLessEqual(len(result["systemMessage"]), 1200)
        code, result = self.run_check("--allow", "src/")
        self.assertEqual(len(result["changes"]), 40)

    def test_inherited_git_overrides_do_not_redirect_repository(self):
        env = dict(os.environ, GIT_DIR="/nonexistent", GIT_WORK_TREE="/nonexistent")
        code, result = self.run_check("--allow", "src/", env=env)
        self.assertEqual(code, 0)
        self.assertEqual(result["repo"], str(self.repo))


if __name__ == "__main__":
    unittest.main()

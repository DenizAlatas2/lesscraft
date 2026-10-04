#!/usr/bin/env python3
"""Report paths outside an explicit scope between two committed Git trees."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


LIMIT = "Committed trees only. Staged, unstaged, and untracked changes are omitted."


class NotChecked(ValueError):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise NotChecked(message)


def git(repo, *args):
    # Do not let inherited Git overrides redirect the explicit repository.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    result = subprocess.run(
        ["git", "--no-pager", "-C", str(repo), *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False,
    )
    if result.returncode:
        raise NotChecked("Git could not read the repository or requested commits")
    return result.stdout


def repository(path):
    root = Path(path).resolve(strict=True)
    top = os.fsdecode(git(root, "rev-parse", "--show-toplevel")).removesuffix("\n")
    if Path(top).resolve() != root:
        raise NotChecked("--repo must name the repository root")
    return root


def scope_paths(values):
    for value in values:
        parts = value.removesuffix("/").split("/")
        if not value or "\x00" in value or any(p in ("", ".", "..") for p in parts):
            raise NotChecked("Scope entries must be nonempty repository-relative paths without . or ..")
    return values


def commit(repo, ref):
    if not ref or ref.startswith("-") or "\x00" in ref:
        raise NotChecked("Invalid commit reference")
    return git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode("ascii").strip()


def check(args):
    allowed = scope_paths(args.allow)
    repo = repository(args.repo)
    if args.hook:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict) or payload.get("hook_event_name") != "Stop":
            raise NotChecked("Expected a Stop hook payload")
        cwd = payload.get("cwd")
        if not isinstance(cwd, str) or not Path(cwd).is_absolute():
            raise NotChecked("Stop payload needs an absolute cwd")
        current_top = os.fsdecode(git(Path(cwd), "rev-parse", "--show-toplevel")).removesuffix("\n")
        if Path(current_top).resolve() != repo:
            raise NotChecked("Stop cwd belongs to a different repository")
    base, head = commit(repo, args.base), commit(repo, args.head)
    raw = git(repo, "diff", "--name-status", "-z", "--no-renames", "--no-ext-diff",
              "--no-textconv", "--ignore-submodules=none", base, head, "--")
    fields = raw.split(b"\0")
    if fields[-1] != b"" or (len(fields) - 1) % 2:
        raise NotChecked("Unexpected Git path output")
    changes = []
    for index in range(0, len(fields) - 1, 2):
        status, path = fields[index].decode("ascii"), os.fsdecode(fields[index + 1])
        inside = any(path.startswith(rule) if rule.endswith("/") else path == rule for rule in allowed)
        changes.append({"status": status, "path": path, "allowed": inside})
    return {"status": "out_of_scope" if any(not c["allowed"] for c in changes) else "within_scope",
            "limitation": LIMIT, "repo": str(repo), "base": base, "head": head,
            "allowed": allowed, "changes": changes}


def hook_summary(report):
    prefix = "Lesscraft scope check: " + report["status"] + ". " + LIMIT
    if report["status"] == "not_checked":
        detail = " Reason: " + report["reason"]
    else:
        outside = [c["path"] for c in report["changes"] if not c["allowed"]]
        detail = (" Compared " + report["base"] + " to " + report["head"] + ". "
                  + str(len(report["changes"])) + " changed paths, " + str(len(outside))
                  + " outside scope. Paths: " + json.dumps(outside, ensure_ascii=True))
    summary = prefix + detail
    if len(summary) > 1200:
        summary = summary[:1050] + " [Summary truncated. Run the manual command for full details.]"
    return {"systemMessage": summary}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    hook = "--hook" in argv
    parser = Parser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--repo", required=True, help="Explicit repository root")
    parser.add_argument("--base", required=True, help="Commit reference for the starting tree")
    parser.add_argument("--head", required=True, help="Commit reference for the ending tree")
    parser.add_argument("--allow", required=True, action="append", help="Exact path or trailing-slash directory prefix")
    parser.add_argument("--hook", action="store_true", help="Read a Stop payload and emit a report-only summary")
    try:
        args = parser.parse_args(argv)
        report = check(args)
    except (NotChecked, OSError, ValueError, UnicodeError) as error:
        report = {"status": "not_checked", "limitation": LIMIT, "reason": str(error)}
    print(json.dumps(hook_summary(report) if hook else report, ensure_ascii=True, indent=None if hook else 2))
    return 0 if hook or report["status"] == "within_scope" else 1 if report["status"] == "out_of_scope" else 2


if __name__ == "__main__":
    sys.exit(main())

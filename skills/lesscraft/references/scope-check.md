# Optional scope check

Use the bundled [helper](../scripts/scope_check.py) only when the user has
explicitly authorized a check. It needs Python 3.9 or newer and Git. Nothing
installs dependencies or hooks automatically.

The manual command is the authoritative interface:

```sh
python3 /path/to/lesscraft/scripts/scope_check.py \
  --repo /absolute/path/to/project \
  --base BASE_COMMIT --head HEAD_COMMIT \
  --allow src/feature/ --allow tests/test_feature.py
```

Choose the repository root, both endpoints, and the allowed paths explicitly.
Use full commit IDs for a repeatable comparison. References are resolved to
commit IDs before the diff, and both IDs appear in the report. The comparison
is between the two committed trees, not a merge-base or working-tree diff.

An allowed entry is either an exact repository-relative file path or a directory
prefix ending in `/`. `src/` includes `src/file.py`, not `src-other/file.py`.
Paths are case-sensitive and use `/`. Do not include leading `/`, empty path
components, `.` or `..`. Quote shell arguments when needed. Wildcard characters
are literal, never globs. The helper does not infer scope from a prompt.

The full JSON report lists every changed path and whether it is allowed.
Moves are a deletion and an addition, so both paths are checked. Binary files
and unusual filenames are included. Submodule changes are reported at the
submodule path, not as paths within its repository.

Manual exit codes are `0` for `within_scope`, `1` for `out_of_scope`, and `2`
for `not_checked`. Invalid configuration or unresolved references never pass.
An empty committed diff can be `within_scope` even with a dirty worktree.

**Staged, unstaged, and untracked changes are omitted.** The helper does not
attribute changes to an agent or person, prove that work is complete, or provide
a security boundary. It reads Git data without writing files, changing the
index, reverting work, creating snapshots or commits, or using the network.

## Optional report-only Stop command

After explicit approval to configure the host, the same command can be used as
a command-type `Stop` hook by adding `--hook`. Keep absolute paths and explicit
arguments in the configured command. Follow the current host documentation:
[Codex hooks](https://learn.chatgpt.com/docs/hooks) or
[Claude Code hooks](https://code.claude.com/docs/en/hooks).
The manual interface remains usable without either host.

The hook reads the host's JSON payload from standard input and requires a
`Stop` event with an absolute `cwd` in the configured repository. Session IDs,
turn IDs, stop-hook state, and assistant messages do not define scope or change
the comparison. Set the endpoints and allowed paths deliberately for each task.
A fixed hook command cannot discover the right task baseline on its own.

Hook mode emits only a JSON `systemMessage` and exits `0`, including when a
check fails or cannot run. It never blocks completion or requests another agent
turn. Summaries longer than the output limit are explicitly marked as truncated.
Run the same command without `--hook` for the complete report.

Tests exercise both hosts' payload shapes with temporary Git fixtures. They do
not establish that a hook is installed or runs in a particular host session.

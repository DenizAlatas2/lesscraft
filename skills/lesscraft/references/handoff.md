# Handoff

Use for completion reports, review summaries, and transfer of work.

Say what the next person needs to know, in proportion to the task:

- **Done:** The actual outcome and relevant files or behavior changed. If the
  work was advisory, report the recommendations rather than claiming edits.
- **Checked:** Checks actually run, their results, and the scope they cover.
  Distinguish static inspection from execution, baseline failures from new
  regressions, and unsuccessful checks from passing checks.
- **Unverified:** Important checks skipped or not run, the reason, blockers,
  and residual uncertainty.
- **Next:** The smallest remaining action or decision, if there is one.

These are content prompts, not mandatory headings. A small task can end with
two sentences. Omit empty categories and unrelated progress narration.

Use concrete evidence when it matters: a relevant path, a reproducible check,
or an accessible issue or review link. Do not paste raw logs by default.
Do not describe a proposed patch as implemented, a passing local check as a
production guarantee, or an accepted request as a completed external action.
Keep implemented, tested, built, installed, and deployed separate: evidence
for one does not establish the others. Report failures plainly and disclose
partial results when missing coverage could affect the next decision.

For a handoff across people or systems, include only the necessary context
and authorized information. Remove secrets, private data, and irrelevant
internal history. Do not make a new status file unless the user requested it
or an authorized repository workflow requires one.

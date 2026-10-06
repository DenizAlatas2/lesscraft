# Maintaining Lesscraft

Lesscraft is portable engineering guidance with a persistent core and optional
skill workflows. Keep the package small, original, public-safe, and advisory
by default.

## Working boundaries

- The skill lives in `skills/lesscraft/`. Its entry point is `SKILL.md`.
- Shared principles and authorization boundaries belong in `core.md`.
  The skill entry point must load it. Put conditional workflow detail in
  the relevant linked reference. Preserve existing host instructions during
  installation. The repository root AGENTS.md is contributor guidance, not
  the core to install into another project.
- Keep automatic discovery enabled. Discovery must not grant permission to
  edit, delete, run checks, commit, or publish.
- Respect explicit user authorization already given without expanding its
  scope. Repository maintenance instructions are not permission to publish.
- Do not add private examples, copied skill text, secrets, or invented metrics.
- Keep Clear English independent. Do not claim formal language-standard
  conformance or add a copied controlled dictionary.
- Write new commit messages in plain, natural language about the actual change.
  Follow required repository conventions. Do not rewrite existing history for style.

## Review changes

Check frontmatter, relative links, and consistency between the entry point,
core, references, metadata, and README. Keep the complete core inside the
copyable package. Installation fixture checks do not prove host loading or
model behavior. Validate with an available Agent Skills
validator when practical. Report what it checks and what it does not.

For material behavior changes, exercise realistic requests in an isolated
workspace. Review outcomes rather than testing for exact prose or headings.
Useful cases include an implicitly selected cleanup review, an explicitly
authorized small patch, a test with unique coverage, an indirectly used
module, and a status document with active callers.

Preserve these invariants: no mutation from discovery alone, no blanket
unit-test ban, no count-driven cleanup, no deletion based only on a filename,
and no unrun checks reported as passing. Add a narrow correction only for a
demonstrated issue. Avoid turning the skill into a large process framework.

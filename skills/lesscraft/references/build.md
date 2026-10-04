# Build

Use for feature work, debugging, and refactoring. The advisory and permission
boundaries in `SKILL.md` apply throughout.

## Trace before designing

Identify the requested behavior and one representative user or system flow.
Find the existing entry point, state owner, domain rules, and external
boundaries. Inspect relevant callers and nearby tests. Expand the search
only when the current evidence leaves a material question unanswered.

For a bug, distinguish the symptom from the cause. Describe a useful
reproduction or regression check. Run it only when authorized. If the cause
is uncertain, prefer a targeted observation over a speculative rewrite.
Investigate the cause before choosing a patch. Do not remove working behavior
merely to eliminate the symptom. Preserve existing capabilities unless the
requested change intentionally replaces them.

## Propose the smallest complete change

- Extend an existing, suitable path before creating a parallel subsystem.
- Keep domain decisions near the code that owns them.
- Use plain data and direct control flow when a framework adds no clear value.
- Add an interface, configuration option, or generalized helper for a real
  boundary or repeated need, not a hypothetical future consumer.
- Preserve required failure handling and public contracts. Name intentional
  behavior changes rather than disguising them as cleanup.
- Prefer existing dependencies. A broad new dependency or environment change
  needs a demonstrated task benefit and appropriate authorization.

Compare alternatives only when they have a meaningful tradeoff. A short
explanation of why the current structure is enough is often the best design.
Do not equate fewer lines with simpler behavior or lower maintenance cost.

## Match verification to the change

Propose the important happy path and the failure or edge case most likely
to cause harm. Reuse an existing behavioral check when it covers the change.
Add a small unit invariant when it isolates a meaningful risk more clearly
than a full-flow check. Account for nondeterminism, real service costs, and
environment limits before proposing execution.

When implementation is explicitly authorized, keep edits within that scope.
Report actual check results, blocked checks, and residual risks. Do not mix
unrelated refactors or test deletions into the patch for convenience.
Distinguish failures already present in a known baseline from regressions
introduced by the change. If the baseline is unknown, say so. Do not label an
inconvenient failure pre-existing without evidence. Preserve command exit
status when filtering logs or wrapping smoke checks so failure stays visible.

## Keep shared work safe

Inspect the current diff before editing. Preserve other people's changes and
unrelated local work. Do not stash shared work, reset it, or overwrite it to
make a task easier. If Git writes are authorized, use explicit file paths and
review the staged diff. Avoid sweeping unrelated changes into a commit.
Group commits by coherent, reviewable changes. Use truthful messages and
normal timestamps. Do not manufacture a development history or add automatic
AI co-author trailers. Follow the repository's actual attribution policy.

When parallel work is useful and available, give each worker a bounded outcome
and clear file or interface ownership. Name the integration owner, avoid
overlapping edits, and respect resource limits. Review each result and verify
the combined behavior. Do not merge outputs blindly or treat a worker's
completion report as proof that integration works.

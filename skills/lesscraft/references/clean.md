# Clean

Use for test review, dead-code candidates, and repository hygiene. Produce
evidence-backed recommendations by default. This mode grants no mutation or
execution permission.

## Code: prove the candidate

Before calling code unused, inspect direct callers and plausible indirect
entry points: exports, configuration, registration, reflection, generated
code, jobs, scripts, and external consumers. Review relevant history or
ownership context when available. A search with no matches is evidence,
not proof. Record the limits of the search.
If a search or history result is partial, continue or state the missing scope
before making a removal recommendation. Preserve known working capabilities
while evaluating whether an implementation is genuinely obsolete.

Recommend removal only when the code has no required role and the supporting
evidence is strong enough for the risk. Otherwise recommend a targeted check
or retain it. Do not delete compatibility paths because current local callers
do not exercise them.

Apply [Build's comment guidance](build.md) within the authorized cleanup scope.
Recommend trimming redundant or stale narration only after checking its purpose.
Retain useful rationale, contracts, and required notices. Do not blanket-delete
comments or use a comment-count target.

## Tests: compare failures, not counts

Map a candidate test to the behavior or failure it protects. Identify any
existing replacement by the failure it can actually detect, including its
boundary and limitations. Similar names, assertions, or happy paths do not
establish duplicate coverage.

Consider simplifying a brittle setup, moving an assertion to a better layer,
or fixing nondeterminism before suggesting removal. Keep unique critical
invariants and useful edge cases. Expensive full-flow tests and numerous
unit tests both need a reason to exist. Neither category is inherently wrong.

A reduction proposal should name the candidate, evidence of overlap or
obsolescence, retained protection, and any verification still needed. If
coverage is unclear, say so and withhold the removal recommendation.

## Documents: understand their job

Before changing an internal status, handoff, plan, or process document, check
its purpose, links and callers, relevant history, audience, and current use.
It may support an active workflow, onboarding, an audit, or a future handoff.
A filename, age, or internal-looking content alone is not a removal reason.

Suggest updating, merging, archiving, or excluding from published output when
that fits the actual purpose. Identify broken links or process effects that
would need attention. Preserve records with retention or ownership questions
until those questions are resolved. Permission for code work does not imply
permission to discard repository history or documents.

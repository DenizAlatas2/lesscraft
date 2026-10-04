# Impact mapping

Use when a change, cleanup candidate, or handoff needs relationships that are
hard to see from one file. Skip the map when direct reading is enough.
The advisory and authorization boundaries in `SKILL.md` still apply.

## Map the question, not the whole repository

Start with the proposed change and the behavior it affects. Use available
symbol navigation, reference search, imports, configuration, and tests to
follow relevant callers and consumers. Reuse an existing index if its scope
and freshness are known. Do not install a graph database, embedding pipeline,
or new service merely because a relationship map could help.

Keep only relationships that help decide this change. For each one, retain:

- The two entities and the kind of relationship.
- A source location or observed execution that supports it.
- The examined revision, or a note that it includes uncommitted changes.
- Whether it is observed, inferred, or still unknown.

Example, using invented names:

| Relationship | Evidence | Status |
| --- | --- | --- |
| Receipt view calls `total` | `receipt.py:42` at the examined revision | Observed |
| `test_exact_money` checks decimal totals | Read its input and assertion | Observed |
| Plugin loader may load `tax_rules` | Configuration names it. Dispatch not traced | Inferred |

Do not infer that a test covers behavior from its filename alone. Read the
assertion and relevant setup, or label the relationship as unverified.

## Treat missing edges as a limit

Static analysis may miss reflection, generated code, plugins, events, string
dispatch, framework conventions, or external consumers. An empty caller list
does not prove that code is dead. Check these paths before proposing removal.
If the evidence is incomplete, keep the item as a candidate with an explicit
gap instead of manufacturing confidence.

Recheck affected relationships after code changes. Do not use a stale index
as proof about the current revision. If a tool truncates results, disclose
the limit and inspect the missing relevant scope before claiming completeness.

## Use the result

In Build, use the map to reuse the right path and identify impacted behavior.
In Clean, use it to support retention or removal proposals and their checks.
In Handoff, preserve the important relationship and its reason, not an index
dump. In Design, trace components and tokens without mistaking dependency
structure for evidence of good usability.

A graph is context, not a verdict. Measure its value by the useful evidence
it adds and the mistakes it prevents, including the cost of building and
maintaining it. A source-backed list is often enough.

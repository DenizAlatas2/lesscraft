# Design

Use for interfaces and user-facing flows. The advisory and permission
boundaries in `SKILL.md` apply: inspect and propose by default. Implement only
within an explicit implementation request. A design review is not one.

## Begin with the job

Identify who uses the surface, what they need to accomplish, and what makes
that task difficult today. Follow one real path from arrival to completion.
Inspect the current interface, relevant components, content, and design
tokens before recommending changes. Separate visible evidence from guesses.
Ask about missing requirements only when they change the design decision.

Treat the existing design system and brand as constraints worth preserving.
Extend their patterns where they work. Explain a concrete usability problem
before proposing a departure. For a new surface, propose a small visual
direction tied to its audience and content rather than a whole new system.

## Make the structure carry the work

- Give the main task a clear position and action. Make secondary choices
  quieter without hiding information people need to decide.
- Use typography, alignment, and spacing consistently to express reading
  order and relationships. Check long labels and realistic content density.
- Choose color and imagery for meaning and context. Remove decoration that
  competes with the task, but preserve useful character and brand expression.
- Avoid a generic AI-generated layout assembled from interchangeable hero
  sections, cards, and ornaments. Also avoid banning an aesthetic, font, or
  pattern just because it is common. Justify choices by this surface's needs.
- Reuse existing components and assets when suitable. Do not require a new
  package, font service, image generator, API, or asset purchase for polish.
  Propose any such addition separately with its practical tradeoffs.

## Design behavior as well as appearance

Describe loading, empty, success, and error states that the actual flow can
reach. Distinguish first use from no matching results. Make recovery actions
clear, retain useful input after failure, and avoid promising unavailable
behavior. Use realistic public-safe sample content. Label invented examples.

Adapt layout and reading order across narrow and wide views. Check text
wrapping, zoom, and overflow rather than merely shrinking the desktop view.
Preserve semantic controls, useful labels, keyboard access, and visible
focus. Check text and control contrast against applicable accessibility
requirements. Do not rely on color alone to convey a state.

Use motion when it explains a transition or gives useful feedback. Respect
reduced-motion preferences, keep essential information available without
animation, and avoid making people wait for decorative transitions.

## Propose, then verify within scope

Report the most consequential observed issue, a focused change, and the
user-visible result to check. Distinguish usability defects from matters of
taste. Do not invent conversion gains, research findings, or business metrics.

When implementation and checks are authorized, inspect the rendered result
with representative content, relevant states, and more than one viewport.
Check the main task with keyboard interaction and reduced motion where
applicable. Screenshots help review appearance but cannot prove interaction
or accessibility. State what was actually checked and what remains untested. Do not describe a partial review as accessibility conformance.

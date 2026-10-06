---
name: lesscraft
description: Apply a lean, evidence-led lens to feature work, debugging, UI review, refactoring, test review, repository cleanup, and technical handoffs. Use for engineering requests such as simplify this, challenge this plan, review this UI, find dead code, or summarize this branch, including German cues like vereinfachen, Plan hinterfragen, Oberfläche prüfen, aufräumen, and Übergabe. Suggest the smallest useful change and proportionate verification. Also use when explicitly asked to turn STE-inspired or ASD-STE100 communication mode on or off. Advisory by default. Discovery alone never authorizes edits or execution.
---

# Lesscraft

Read [the core](core.md) before using this skill. Apply its language,
sparring, scope, code-quality, and verification principles throughout the
work. Read it even when this host already supplies a persistent copy.
Loading either file grants no additional permission.

For principles present before skill selection, use the optional
[persistent installation](references/persistent-core.md). Skill discovery
alone supplies metadata, not a guarantee that these instructions are active.

## Read only the workflow detail the task needs

Normal development does not require the user to activate a mode. Select
relevant references from the task and combine them when useful. Do not load
all references or impose every workflow on a small request.

- **Build:** For feature design, debugging, and refactoring, including
  "simplify this", "challenge this plan", "vereinfachen", or "Plan hinterfragen", read
  [Build](references/build.md).
- **Design:** For interface design, visual review, and interaction quality,
  including "review this UI" or "Oberfläche prüfen",
  read [Design](references/design.md). Use alongside Build when implementing UI.
- **Clean:** For test portfolio review, dead-code candidates, and repository
  hygiene, including "find dead code" or "aufräumen", read [Clean](references/clean.md).
- **Handoff:** When the task calls for a completion report, review summary,
  or transfer of work, including "summarize this branch" or "Übergabe", read
  [Handoff](references/handoff.md). Do not create a handoff file by default.
- **Impact mapping:** When dependencies are unclear, optionally use
  [Impact mapping](references/impact-map.md). Prefer existing code navigation
  and a small source-backed map over new graph infrastructure.
- **Natural writing:** For a closer prose edit, use
  [Natural writing](references/natural-writing.md). The core's language rules
  already apply to ordinary explanations.
- **ASD-STE100 mode:** When explicitly requested, read
  [STE-inspired communication](references/clear-english.md) and apply it to
  your explanations, questions, updates, and handoffs. It is STE-inspired,
  not validated ASD-STE100 conformance.

These phrases are contextual cues, not guaranteed activation commands.
An explicit request to turn ASD-STE100 or STE-inspired mode on activates it
for the current conversation until the user turns it off or supplies a
different scope. Turning it off restores normal wording. Do not change
persistent settings or files merely to activate a mode.

# Natural writing

Use this guide when prose distracts from a useful engineering explanation.
It applies across modes. It does not activate STE-inspired mode or authorize
editing project files. Plain, accurate prose is the goal. This guide does not
identify authorship or promise any result from an AI detector.

- Start where the reader's question starts. Give the answer, evidence, or
  needed decision before background they already have.
- Keep sentences that help the reader understand or act. Remove ceremonial
  openings, self-praise, generic encouragement, and repeated conclusions.
- Describe the actual behavior. Replace broad praise with a supported detail,
  or remove it when no detail is available. Keep technical names consistent.
- Let the content determine paragraph length and list size. Do not force
  three examples, identical sentence shapes, or a dramatic closing line.
- Preserve the writer's meaning and level of formality. A sample can guide
  tone within the user's explicit style constraints. Do not add slang,
  personal stories, emotions, or opinions to manufacture a voice.

For ordinary prose, follow the punctuation rule in `SKILL.md`: no em dashes,
en dashes, semicolons, or decorative inline middle dots. Real list bullets
are fine. Preserve syntax in code, commands, identifiers, quotations, and
formal source text. Do not silently rewrite user wording outside the requested
editing scope.

Before returning an edit, compare its claims with the original. Preserve
numbers, names, attribution, conditions, negatives, and meaningful uncertainty.
Keep a qualification when removing it would imply stronger evidence. Leave
code, data, links, and exact technical strings intact unless their change is
part of the authorized task. If the original is already clear, leave it alone.

Background reading: [Humanizer](https://github.com/blader/humanizer) and its
[skill](https://github.com/blader/humanizer/blob/main/SKILL.md) informed this
independent guidance. Humanizer is [MIT-licensed](https://github.com/blader/humanizer/blob/main/LICENSE).
No upstream instructions or examples are bundled, and it is not a dependency.

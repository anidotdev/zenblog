# Editorial and Design Specification

## Positioning

A public engineering notebook built around working artifacts. The site is not a conventional portfolio or a general-interest blog. Its recurring question is: what becomes visible when an abstraction is derived, implemented, measured, and pushed against its limits?

## Audience paths

**Recruiter:** identity and technical direction → featured investigation → short summary → artifact or source link.

**Hiring manager / engineer:** claim → artifact → relevant model or derivation → implementation decisions → failure modes, assumptions, and next tests.

**Technical reader:** a navigable, self-contained explanation with real evidence and links to source material.

## Homepage hierarchy

1. Identity, pitch, and links.
2. One manually featured article (or newest article if none is explicitly featured).
3. The rest of the chronological feed, without repeating the featured article.
4. Stop after the work; no decorative footer copy.

No sidebar, animated hero, separate about page, comments, newsletter pitch, search, or tag directory in v1.

## Article hierarchy

1. **Header:** title, one-line summary, date, topics, source link(s).
2. **Artifact:** result, figure, demo, source excerpt, or benchmark. It must be accurately captioned.
3. **Jump links:** generated from level-two headings so navigation stays in sync with content.
4. **Investigation:** derivation or mental model; implementation choices; experiments and interpretation.
5. **Limitations:** failure modes, unsupported inputs, uncertainty, numerical limits, or unresolved work.

This is a reusable structure, not a rigid outline. Systems work may not need a mathematical derivation. An algorithm article may not have a meaningful performance result yet. Use only sections justified by the work.

## Visual tokens

- Paper: `#faf9f6`
- Ink: `#191919`
- Muted ink: `#6b6964`
- Hairline: `#e5e2dc`
- Code surface: `#f1efea`
- Accent: `#873333`
- Interface face: Inter
- Reading face: Newsreader
- Code face: system monospace stack; no third external font
- Prose measure: approximately `66ch`
- Body: 18–19px, line height 1.65–1.75
- Headings: modest serif scale, slightly tight tracking
- Separation: whitespace and hairlines rather than card borders or shadows
- No editorial kicker labels, oversized category banners, featured-work labels, or explanatory chrome

## Editorial guardrails

- Artifact thumbnails should represent an actual result, a clearly labeled conceptual diagram, or a real source excerpt.
- Never imply a benchmark or parity claim before the test and tolerance are documented.
- Every published investigation should explain one limitation or boundary; it does not need to manufacture a dramatic failure.
- Keep one canonical source file per artifact and avoid dead repository links.
- Add navigation features only when the amount of published content makes them useful.

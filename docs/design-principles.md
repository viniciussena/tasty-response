# Design principles

Two contracts, both binding on every generated artifact. The **content
contract** is what actually reduces cognitive load. The **visual system** is
necessary but not sufficient — a beautiful page full of padded prose fails
the point of this project.

## 0. The tiebreaker

When two options are both defensible and one is more legible while the other
is more beautiful, **the more legible one wins**. Least friction is the
premise; "cool" and "elegant" are not.

This is not a preference, it is the point of the project. An artifact exists
to cost the reader less than the terminal text did. A choice that makes the
page more admirable and marginally harder to read has moved in the wrong
direction, however good it looks in a screenshot.

The rule comes from D-015, where it overturned a decision that was already
built, already paid for, and better looking than what replaced it.

## 1. Content contract

Before finalizing any artifact, the following must hold. This is a checklist
the skill applies, not a field schema the answer must fill: the *shape* of an
answer stays free-form per topic; only the quality bar is fixed.

| Principle | Test it passes | Failure smell |
| --- | --- | --- |
| **Concise** | Every sentence carries information the reader does not already have | Restating the question; "as mentioned above"; throat-clearing preambles |
| **Concrete** | Claims are anchored to names, numbers, paths, or examples | "Improves performance"; "several options"; "best practices" |
| **Complete** | Necessary nuance survives the compression | A caveat dropped because it did not fit the slide |
| **Direct** | The fact sits in the headline and in the section's first sentence | The fact held one beat back for effect |
| **Didactic** | Every term the conclusion depends on is built before it is used | Jargon assumed; the payoff buried three sections down |

**Complete beats concise when they collide.** The goal is density reduction,
not information loss. If a nuance matters, give it its own section rather
than cutting it.

**Direct and didactic pull opposite ways, and that is expected.** Directness
removes words; building a hard term adds them. They are not in conflict
because they govern different things — directness is about where the fact
sits in a sentence, didacticism about whether the reader has ground to stand
on. Groundwork written directly satisfies both. The operational form of both
rules lives in SKILL.md §4 (D-017, D-018).

### Register

The delayed fact is a failure mode of its own (D-017). A headline built on
the surprise rather than on the finding, a heading that names the effect on
the reader instead of the content, a list of three with a turn at the end:
each moves real information one beat later so that it lands harder. The beat
costs the reader time, and costs anyone scanning only headlines the fact
itself.

The overcorrection is worse. A headline stripped of its claim becomes a
label, and the headline scan exists to catch that. The target is between the
two, and one test separates them: **could the reader disagree with it?** A
teaser admits no disagreement. A claim can be wrong.

### Explaining a hard term

When an answer rests on a concept the reader does not have, the concept gets
built before it is used — plainly, and without ornament (D-018).

The judgement is about who the reader is, not about how hard the term is:
**explain what they would have to go look up, not what they use every day.**
Evidence that they use it every day is observable — the term appears in their
prompt, in their repository, or in an earlier turn. Explaining those back to
them spends attention in the wrong place.

A concrete instance from the reader's own domain beats an analogy borrowed
from another one. The analogy is a second thing to learn and then discard,
and metaphor is exactly the ornament this rule excludes. Where a confusion is
predictable, saying what the thing is *not* is usually worth more than the
definition that corrects it.

### Chunking

- One idea per section. If a section needs the word "also", it is two
  sections.
- Three levels of hierarchy, used consistently: headline (the claim),
  supporting point (why), detail (the specifics). A reader scanning only
  headlines must still come away with the answer.
- Prefer a table when comparing 3+ things across 2+ dimensions. Prefer a list
  when order or completeness matters. Prefer prose when the reasoning
  connecting the points *is* the content.
- Groundwork goes before whatever depends on it, and may need a section of
  its own. Such a section is earned when the reader genuinely lacks the term
  and padding when they do not — that is the whole line between it and slide
  theater.
- A diagram earns its place by showing a mechanism words handle badly —
  flow, topology, timing. A diagram that restates a list is decoration.

## 2. Visual system

### What makes a design read as "tasty"

The palette is a parameter (D-012), but every option has to satisfy the same
brief, so it is worth naming what the brief actually is:

- **Hue.** Appetite responds to warm, saturated color — red, orange, amber,
  yellow. Blue does the opposite; almost no food is naturally blue, and food
  branding avoids it. Green reads as *fresh* rather than as the main course.
  Brown carries roasted, caramelized, umami.
- **Plating.** The dark ground is not a developer affectation, it is the
  plate. A dark surface makes bright color leap, which is why food
  photography lives on slate and cast iron. But the dark has to have
  temperature — never neutral black.
- **Material.** Matte and slightly grainy reads artisanal; glossy and smooth
  reads industrial confectionery. This is what the grain layer buys.
- **Space.** Generous negative space reads fine dining; crowded reads diner.
- **Type.** Rounded geometric = sweet. High-contrast serif = menu, expensive.
  Condensed caps = market signage. Soft serif = artisanal bakery. Mono =
  spec sheet.

The content here is technical, so **mono is the counterweight that keeps the
whole thing from turning kitsch** — it holds every label and datum while the
display face and the palette carry the warmth. The hard line: nothing
literal. No checked tablecloths, no chef hats, no food emoji. Literalism
costs the reader's trust in the content.

Dark is the default regardless of the reader's OS; light is opt-in through a
persisted toggle (D-009).

### Typography

Three roles, and two of them travel inside the file as base64 rather than
being borrowed from the reader's system.

**Body — `Atkinson Hyperlegible`, embedded (D-014).** This is the role that
governs reading ergonomics, so it is the one that must not be left to chance.
It was originally only *named first* in a font stack, which on a normal
machine fell straight through to whatever the system had. Designed by the
Braille Institute to differentiate the letterforms readers most often confuse
— `I l 1`, `O 0`, `b d p q`.

**Display — a build parameter (D-013).** `nunito` (rounded sans) by default,
`fraunces` (soft serif) kept as the alternative. Headlines are load-bearing
here, not decorative: the headline scan is a self-check the artifact must
pass. So the display face is a legibility decision, not only a stylistic one
— and when the two pulled apart, legibility took it (D-015).

**Mono** handles every label and datum, and is the counterweight that keeps a
technical artifact from reading as a dessert menu.

### Tokens

Defined once as CSS custom properties, then referenced everywhere. **No
hardcoded colors in element rules** — that is what keeps a new theme to a
one-file change.

- **Palette**: five section accents plus a neutral scale. Color must carry
  *meaning* — section identity, callout severity — never decorate at random.
  One accent per section, applied by token cascade so the whole section
  recolors from a single attribute.
- **Type**: see Typography above. The contrast between the display and mono
  roles *is* the typographic identity. Remote fonts remain forbidden (D-007);
  embedded ones are not remote, which is the distinction that made a real
  identity affordable (D-013, D-014).
- **Scale**: one modular scale. Body text no smaller than 16px, line height
  around 1.65, measure capped near 68 characters — long lines are the single
  biggest readability regression on a wide monitor.
- **Spacing**: one scale, used for every gap. The rhythm between sections
  must be visibly larger than the rhythm within one; that difference is what
  makes chunks read as chunks. If it flattens, the page becomes a styled
  wall.
- **Texture**: a faint inline-SVG grain keeps the dark ground reading warm
  rather than flat. It is the one piece of pure atmosphere in the system, and
  it stays under 5% opacity.

### The docket

Every artifact opens with a provenance ticket: project, path or URL, what was
asked, one line of context, named attachments, timestamp, orientation count.
It exists because artifacts accumulate and six open tabs otherwise look
identical (D-010).

It is also the system's **signature element** — the one place boldness is
spent. Everything around it stays disciplined.

### Accessibility

Non-negotiable, and testable:

- Contrast at least 4.5:1 for body text and 3:1 for large text, **in both
  themes**.
- Never encode meaning in color alone — pair it with an icon, a label, or a
  border.
- Respect `prefers-reduced-motion`. Motion is armed by script only when
  motion is allowed, and content is never left hidden behind an effect that
  did not run.
- The page must be complete with JavaScript disabled. The theme toggle,
  section reveal, and keyboard navigation are enhancements, never
  load-bearing.
- Keyboard-navigable, with a visible focus ring and a skip link to the
  answer.
- Semantic HTML: real headings in order, real lists, real tables. The visual
  hierarchy and the document outline must agree.

## 3. HTML generation contract

| Rule | Reason |
| --- | --- |
| Single file | It survives being emailed, moved, or opened from a USB stick |
| No external requests — CSS and JS inlined, no CDN, no remote fonts | It must open offline, in an airplane, years from now |
| Images as `data:` URIs or omitted | Same reason |
| Responsive: relative units, no horizontal page scroll | It gets opened on a laptop and a phone |
| Wide content scrolls inside its own container | A wide table must not break the page layout |
| Explicit `<title>` | It becomes the browser tab; a scannable name, not a summary |
| Valid standalone document | It is not embedded anywhere; it is the whole page |

## 4. Anti-patterns

Things that would technically satisfy the letter of the spec and defeat it:

- **The pretty wall.** Styled, themed, accessible — and still nine
  undifferentiated paragraphs. Style applied to unrestructured prose is the
  main failure mode of this project.
- **Slide theater.** Chunking padded content across twelve near-empty
  sections to look structured. Sections must be earned by ideas.
- **Trailer voice.** The fact held one beat back so that its arrival lands.
  Same information, moved so that it reaches the reader late.
- **The analogy detour.** A metaphor from another domain where a real
  instance from this one was available.
- **Explaining what they already know.** Defining a term the reader used in
  their own prompt.
- **Lossy compression.** Cutting the caveat that made the answer correct
  because it did not fit the layout.
- **Decorative diagrams.** A flowchart of three boxes that a sentence covered
  better.
- **Terminal abandonment.** Emitting only a file path. The terminal always
  keeps enough that a missed browser tab is an inconvenience, not a loss.

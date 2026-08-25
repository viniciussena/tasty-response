# Design principles

Two contracts, both binding on every generated artifact. The **content
contract** is what actually reduces cognitive load. The **visual system** is
necessary but not sufficient — a beautiful page full of padded prose fails
the point of this project.

## 1. Content contract

Before finalizing any artifact, the following must hold. This is a checklist
the skill applies, not a field schema the answer must fill: the *shape* of an
answer stays free-form per topic; only the quality bar is fixed.

| Principle | Test it passes | Failure smell |
| --- | --- | --- |
| **Concise** | Every sentence carries information the reader does not already have | Restating the question; "as mentioned above"; throat-clearing preambles |
| **Concrete** | Claims are anchored to names, numbers, paths, or examples | "Improves performance"; "several options"; "best practices" |
| **Complete** | Necessary nuance survives the compression | A caveat dropped because it did not fit the slide |
| **Didactic** | Terms are defined at first use; each idea builds on the last | Jargon assumed; the payoff buried three sections down |

**Complete beats concise when they collide.** The goal is density reduction,
not information loss. If a nuance matters, give it its own section rather
than cutting it.

### Chunking

- One idea per section. If a section needs the word "also", it is two
  sections.
- Three levels of hierarchy, used consistently: headline (the claim),
  supporting point (why), detail (the specifics). A reader scanning only
  headlines must still come away with the answer.
- Prefer a table when comparing 3+ things across 2+ dimensions. Prefer a list
  when order or completeness matters. Prefer prose when the reasoning
  connecting the points *is* the content.
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

Three roles, and one of them is embedded rather than borrowed from the
system: **Fraunces SuperSoft Bold**, subset and inlined as base64 (D-013). No
platform ships a soft serif, and a soft serif is the single most effective
typographic move available for this brief — so it travels inside the file.
Body stays a high-legibility sans with `Atkinson Hyperlegible` first, and
mono handles every label.

### Tokens

Defined once as CSS custom properties, then referenced everywhere. **No
hardcoded colors in element rules** — that is what keeps a new theme to a
one-file change.

- **Palette**: five section accents plus a neutral scale. Color must carry
  *meaning* — section identity, callout severity — never decorate at random.
  One accent per section, applied by token cascade so the whole section
  recolors from a single attribute.
- **Type, three roles**: a display face for claims (heavy, tight tracking), a
  high-legibility body face with `Atkinson Hyperlegible` first for the
  dyslexia goal, and a mono utility face for every label, kicker, and datum.
  The contrast between the display and mono roles *is* the typographic
  identity — no remote fonts are allowed (D-007), so it has to come from how
  system stacks are set rather than from a downloaded typeface.
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
- **Lossy compression.** Cutting the caveat that made the answer correct
  because it did not fit the layout.
- **Decorative diagrams.** A flowchart of three boxes that a sentence covered
  better.
- **Terminal abandonment.** Emitting only a file path. The terminal always
  keeps enough that a missed browser tab is an inconvenience, not a loss.

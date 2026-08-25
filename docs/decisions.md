# Decision records

Each record states what was decided, why, and what would reverse it. The
first four close open questions carried in the archived PLAN.md §10.

---

## D-001 — Name: `tasty-response`

**Status:** decided.

Chosen after a brainstorm across five axes. The pain identified along the
way: dense plain-text answers force the reader to build the hierarchy
themselves; TR delivers the structure already built, in a pleasant,
low-friction package. `tasty-response` won on capturing the affective "I want
to read this" reaction, memorability, and non-collision with existing skills.

**Cost, accepted:** the name does not self-announce the HTML/visual
mechanism. The tagline must carry it — *"turns any answer into a colorful,
single-page HTML you actually want to read."*

Axes explored and set aside: didactic/clarity (`clear-response`,
`readable-response` — accurate, generic); reaction/wow (`Aha`, `Tcharam`,
`Prisma` — fun, opaque to a developer at a glance); pain-naming
(`unburden-response`, `nostrain-response` — named the symptom, not the fix);
ergonomics (`frictionless-response`, `ergo-response` — precise but clinical);
pleasant/sensory (`pleasant-response`, `cozy-response` — close runner-up).
Descriptive compounds considered before the pivot: `visual-brief`,
`clear-brief`, `view-brief`, `html-brief`, `slide-brief`, `open-brief`,
`clearview`, `legible`, `didact`, `unfold`.

---

## D-002 — Claude generates the artifact; the hook only opens it

**Status:** decided. Closes PLAN.md §10 Q1.

A hook cannot rewrite the final assistant message. A `Stop` hook can read the
session transcript and can block to force continuation, but there is no
interception point that replaces rendered output. So TR does not try.

The skill instructs Claude to write the artifact as an ordinary tool step; a
`PostToolUse` hook matching `Write` opens it. Simpler, no privileged
capability, and it degrades well — if the hook never fires the file still
exists and its path was printed.

**Reverses if:** Claude Code later exposes a supported final-message
transform, *and* generation-by-instruction proves unreliable in practice.

---

## D-003 — Always keep terminal text

**Status:** decided. Closes PLAN.md §10 Q2.

The artifact never replaces the terminal answer entirely. Default
`keep_terminal_text: "summary"` — one or two lines plus the file path. Full
replacement risks silently losing content when the browser tab is not
watched, and makes the mode feel like a black box.

`full` and `path-only` exist as opt-ins for users who have formed the habit
in either direction.

---

## D-004 — Per-conversation opt-out ships in v0.1

**Status:** decided. Closes PLAN.md §10 Q3.

The skill must honor a natural-language opt-out ("no HTML this time", "just
answer in the terminal") for the remainder of the turn, and a session-level
"turn off tasty-response" until re-enabled.

Deferring this was considered and rejected: an always-on mode with no cheap
escape hatch is the fastest way to get uninstalled. The escape hatch is what
makes always-on tolerable.

---

## D-005 — Two scopes, no `--scope global`

**Status:** decided.

`--scope project` writes to a repository's `.claude/`; `--scope user` writes
to `~/.claude/`. There is no machine-wide policy layer to target, so `user`
is effectively global per account. Project config overrides user config key
by key.

**Reverses if:** Claude Code adds a machine-wide policy layer.

---

## D-006 — Activation errs toward skipping

**Status:** decided.

The heuristic (architecture §4) generates an artifact only for substantive,
structured answers. A missed artifact costs a scroll. A spurious one costs a
browser tab, and a mode that opens tabs for "yes, that's correct" trains the
user to ignore it — which is fatal for an always-on tool.

---

## D-007 — Self-contained, offline-first, no CDN

**Status:** decided.

All CSS and JS inlined, no remote fonts, no external requests. The artifact
must open offline and years later. This constrains the visual system to
system font stacks and hand-written CSS, which is accepted: a slide library
would buy polish at the cost of the one property that makes these files worth
keeping.

---

## D-008 — v0.1 is deliberately smaller than brief-spec v0.5

**Status:** decided.

Claude Code only, one theme, one skill, two hook events, manual scoped
installer, no export formats. The idea has to be validated on one harness
before any portability work is justified.

---

## D-009 — Dark is the default; light is opt-in

**Status:** decided. Supersedes the light-first token layout of the first
theme draft.

The audience reads code on dark all day. A light artifact opening into a dark
workspace is a flash and a context switch. So `:root` carries the dark
palette and light lives behind `[data-theme="light"]`, set by a persisted
toggle.

**Cost, accepted:** the artifact does not follow `prefers-color-scheme`. A
reader whose OS is set to light still gets dark on first open, and must
toggle once. This was chosen deliberately over OS-following, because "dark by
default" was the requirement; the toggle persists, so the cost is one click,
once, per reader.

**Reverses if:** readers report the first-open flash in light environments.
The change is mechanical — wrap the light token block in
`@media (prefers-color-scheme: light)` guarded by
`:root:not([data-theme="dark"])`, and make the toggle three-state again.

---

## D-010 — The docket: provenance header

**Status:** decided.

Artifacts accumulate, and the failure mode is six open tabs that all look
alike. Every artifact opens with a docket — an order ticket carrying project
name, path or URL, what was asked, one line of context, named attachments,
timestamp, and a section/read-time count.

Three rules make it work rather than decorate:

- **The ask is the reader's words**, verbatim when short. A tidied paraphrase
  destroys the recall cue, which is the entire function.
- **Attachments are named, never inlined.** The docket records what was on
  the table; the artifact is not an archive.
- **Every field is filled.** A half-empty docket is worse than none, because
  it trains the reader to stop looking at it.

It doubles as the artifact's signature element — the one memorable piece of
visual identity — which is why it gets the mono treatment, the accent rule,
and the dashed separators rather than being a plain metadata strip.

---

## D-011 — Warm dark, not cold slate

**Status:** superseded in its specifics by D-012 (which replaced the single
espresso palette with four themes) and D-013 (which lifted the system-fonts-
only reading). The *principle* below still governs every theme: warm, edible,
never cold slate.

Developer tooling defaults to cold slate-blue, and AI-generated design
converges on near-black with a single acid-green accent. The artifact avoids
both: the ground is espresso (`#17120E`), a warm near-black, and the accents
are edible — saffron, pistachio, chili, plum, mint — one per section.

The name promises something you want to consume. A cold palette would
contradict it, and would make these files indistinguishable from every other
dark surface already open on the machine.

Supporting choices, all downstream of that direction: a faint inline-SVG
grain so the dark ground reads warm rather than flat; three type roles
(display for claims, a legible body face with `Atkinson Hyperlegible` first
for the dyslexia goal, mono for every label and datum); and section accents
that recolor their whole section by token cascade.

**Constraint that shaped it:** no remote fonts (D-007), so the typographic
identity has to come from system stacks and how they are set — tight
tracking on a heavy display face against a mono utility face — rather than
from a distinctive downloaded typeface.

---

## D-012 — Four themes, patisserie by default

**Status:** decided. Supersedes the single espresso palette of D-011.

The palette is a parameter, not a fixed choice. Four ship, each a coherent
direction rather than a hue shift of the others:

| Theme | Direction | Pole it occupies |
| --- | --- | --- |
| `patisserie` *(default)* | Cocoa-plum ground; raspberry, pistachio, caramel, blueberry, vanilla | Sweet, high delight |
| `cellar-gold` | Aubergine ground; gold leaf, burgundy, fig, sage, copper | Elegant, considered |
| `charred-citrus` | Charcoal with a green undertone; yolk, lime, blood orange, chili | Bold, high energy |
| `matcha-ceramic` | Warm sumi ink; matcha, persimmon, plum, kinako, indigo | Calm, crafted |

This forced a structural split that was worth doing on its own:
`styles/core.css` holds structure and contains **zero color literals**, and
`themes/*.css` holds nothing but tokens. A theme is now genuinely a one-file
change, and `templates/base.html` is assembled by `build.py` rather than
hand-maintained.

Every palette, in both its dark and light form, is verified by
`check-contrast.py` against WCAG AA — including each accent against its own
tint, which is what sits behind kickers, table headers, callout labels, and
the docket. Two patisserie light accents failed at 4.42 and 4.44 and were
darkened until they passed. **A theme that does not pass is not a theme.**

**Reverses if:** readers change themes constantly, which would mean the
palette is decoration rather than identity.

---

## D-013 — The display face is embedded; D-007 gains one exception

**Status:** decided. Narrows D-007.

D-007 forbids remote fonts, and that stands: an artifact must open offline
years from now. But "no remote fonts" was being read as "system fonts only",
and that put a ceiling on the typography — no platform ships a soft serif,
which is the single most "tasty" typographic move available.

A font embedded as a `data:` URI is not a remote font. It makes zero network
requests and survives offline exactly as well as the rest of the file.

Shipping: **Fraunces SuperSoft Bold**, optical size pinned to 60, subset to
Basic Latin + Latin-1 Supplement (full pt-BR coverage) + typographic
punctuation. 16.6KB of woff2, about 22KB as base64, against a ~25KB artifact.
The family is renamed `TR Display` so an installed copy of Fraunces cannot
shadow the embedded one and silently change how an artifact renders.

Fraunces is SIL OFL 1.1; the license text ships in `licenses/Fraunces-OFL.txt`
and the attribution is in the CSS comment beside the `@font-face`.

**Why a soft serif:** it is the vernacular of artisanal food branding —
doughy, hand-cut, warm. Mono stays the utility face, which is what keeps a
technical artifact from reading as a dessert menu.

**Reverses if:** artifact size becomes a real complaint, or a system-stack
alternative appears that lands the same tone.

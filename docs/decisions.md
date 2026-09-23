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
to `~/.claude/`. *(Since D-020 these are `npx skills add` without and with
`-g`, not TR flags. The two scopes are unchanged.)* There is no machine-wide policy layer to target, so `user`
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

**Status:** decided. Three of its terms were later changed: four themes, not
one (D-012); no installer (D-020); and at most one hook, built only if
evidence asks for it (D-021). The principle — validate on one harness before
any portability work — stands.

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
- **Attachments are named, never inlined**, and "attachment" means only
  what the reader put into the prompt. Files the model opened while answering
  are not attachments, and listing them was the first real bug the docket
  produced in the field: a reader who attached nothing got six spreadsheets
  in their header. When nothing was attached, the row is deleted rather than
  filled with a dash.
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

## D-012 — Four themes, charred-citrus by default

**Status:** decided. Supersedes the single espresso palette of D-011.

The palette is a parameter, not a fixed choice. Four ship, each a coherent
direction rather than a hue shift of the others:

| Theme | Direction | Pole it occupies |
| --- | --- | --- |
| `charred-citrus` *(default)* | Charcoal with a green undertone; yolk, lime, blood orange, chili, smoke | Bold, high energy |
| `cellar-gold` | Aubergine ground; gold leaf, burgundy, fig, sage, copper | Elegant, considered |
| `patisserie` | Cocoa-plum ground; raspberry, pistachio, caramel, blueberry, vanilla | Sweet, high delight |
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

The default moved twice before settling — `patisserie`, then `cellar-gold`,
then `charred-citrus` — each time by looking at rendered artifacts rather than
at swatch lists. That is the intended way to make this call, and the reason
`examples/` is generated rather than described.

One note kept on the record: `charred-citrus` contains the lime accent that
was originally flagged as close to the near-black-plus-acid-green look that
AI-generated design converges on. It was chosen anyway, on a rendered
side-by-side rather than on the abstract objection. If the resemblance ever
becomes the complaint, the fix is to pull lime toward yolk rather than to
change the default again.

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

Fraunces is SIL OFL 1.1; the license text ships in `fonts/licenses/Fraunces-OFL.txt`
and the attribution is in the CSS comment beside the `@font-face`.

**Note:** this record originally shipped Fraunces SuperSoft Bold on the
argument that a soft serif is the vernacular of artisanal food branding. The
mechanism — embed, subset, rename — survived; the face did not. See D-015.
Mono stays the utility face throughout, which is what keeps a technical
artifact from reading as a dessert menu.

**Reverses if:** artifact size becomes a real complaint, or a system-stack
alternative appears that lands the same tone.

---

## D-014 — The body face is embedded too, because the accessibility claim was decorative

**Status:** decided. Extends D-013 from the display face to the body face.

The docs said the body stack put `Atkinson Hyperlegible` first "for the
dyslexia goal". Checked against the actual development machine: neither
Atkinson Hyperlegible nor `Inter` is installed. The stack fell straight
through to Segoe UI. Every artifact generated so far had been rendering in a
system font while the design documents claimed an accessibility property.

**A font stack that names a face nobody has is a wish, not a decision.** The
project's stated motivation is readers with ADHD, autism, and dyslexia; the
body face is the one that governs continuous reading, and it was the one left
to chance while the display face — used for a dozen words per page — was
carefully embedded.

Now embedded: Atkinson Hyperlegible 400 and 700, subset to Latin-1, about
24KB as base64. Designed by the Braille Institute specifically to
differentiate commonly confused letterforms (`I l 1`, `O 0`, `b d p q`).
Renamed `TR Body` so a local copy cannot shadow it. SIL OFL 1.1;
`fonts/licenses/AtkinsonHyperlegible-OFL.txt`.

**The general lesson, worth more than the fix:** a claim in a design document
is not a property of the artifact. Anything the docs assert about how the
output behaves has to be verified against a real machine, not against the
CSS.

---

## D-015 — Nunito is the display face; least friction beats elegance

**Status:** decided. Closes the question D-013 left open, and narrows its
justification.

Two ergonomics questions were raised about Fraunces SuperSoft Bold: its
distinctive curved `f`, and whether a serif belongs at all when everything
else on the page is sans.

**On the `f`:** it is not the `WONK` axis. Rendering the glyph at `WONK=0`
and `WONK=1` produces an identical outline — 34 contour commands, advance
871. The shape is inherent to the typeface and cannot be tuned away, so the
choice was binary: keep Fraunces with its `f`, or change face.

**On serifs:** the general claim that sans is more legible than serif for
body text does not hold up well for sighted adults; the research finds no
consistent difference. But this project names its audience in the second
sentence of its own README, and published dyslexia guidance is explicit in
recommending sans-serif. When the general evidence is equivocal and the
audience-specific guidance is not, the guidance wins.

**Decided:** `nunito` (rounded sans, ExtraBold) is the default display face.
Rounded terminals still carry the confectionery warmth the name asks for,
without serifs and without high stroke contrast. `fraunces` stays in the
repository as a selectable alternative — it costs 23KB on disk and nothing at
all unless chosen.

### The rule this produced

Fraunces was already built, already paid for, already subset and licensed,
and by the owner's own judgement the better-looking of the two. It lost
anyway. That is worth stating as a general rule rather than leaving as a
one-off:

> **Least friction is the premise. "Cool" and "elegant" are not.** When a
> choice is between the more legible option and the more beautiful one,
> legibility takes it — including when the beautiful one is already
> implemented.

An artifact exists to cost the reader less than the terminal text did. A
choice that makes the page more admirable and marginally harder to read has
moved in the wrong direction, however well it screenshots. This now sits at
the top of `docs/design-principles.md`, ahead of the content contract.

**Reverses if:** the rounded sans proves to undercut the identity badly
enough that readers stop recognizing their artifacts — a recognition problem,
not an aesthetic one.

---

## D-016 — During M1, the skill opens the artifact itself

**Status:** decided, provisional. Narrows D-002 for M1 only. **Its premise
was wrong** — a skill *can* register a hook, from its own frontmatter
(D-020). The M1 behavior stands; the reason it had to be provisional does
not.

D-002 assigns the opening to a `PostToolUse` hook. A hook cannot be
registered from a skill — it needs `settings.json` or a plugin manifest — so
under a skill-only install the artifact gets written and never opened. That
leaves M1 testing the artifact without testing the thing that makes the mode
feel like a mode.

So for M1 the skill instructs Claude to run the platform's opener as an
ordinary shell step (SKILL.md §2, "Opening it"). This buys an end-to-end loop
with no install beyond dropping the skill in place, and it costs three
things, all accepted for a prototype:

| Cost | Why it is tolerable in M1, and not after |
| --- | --- |
| A permission prompt per open, unless the reader allowlists the command | Annoying, but visible and self-inflicted — not a silent failure |
| The model both chooses the path and opens it, so the prefix and extension check of architecture §5 has no independent enforcer | M1 runs on the author's own machine, against paths the author can see |
| Instruction-following instead of a deterministic match on `Write` | A missed open costs one click; the plan's risk table cares about the opposite failure |

The second row is the one that must not ship. Path validation is a control
*on* the model, and a model validating its own chosen path is not a control.

**Reverses when:** M2 lands the hook. At that point the "Opening it" section
comes *out* of SKILL.md rather than coexisting with it — two openers racing
on the same `Write` is a duplicate browser tab, which is precisely the
spurious-tab cost D-006 exists to avoid.

---

## D-017 — Register is part of the content contract: `Direct` joins it

**Status:** decided. Adds a fifth principle to design-principles.md §1.

The generated artifacts read like film-trailer copy. The owner named the
pattern before it had a name here: *"a house, a car, and nobody imagines what
it would be."* Three examples from one real artifact:

| Written | The fact it was carrying |
| --- | --- |
| "Two new accounts, and a whole report nobody knew existed" | Account 2810 posts to an entity, and no view renders entities |
| "The part that confuses everyone" | Totals do not sum the detail lines |
| "A Dynamics report is two lists, and we copy one of them by hand" | The row definition is transcribed manually; there is no API |

The mechanism is **delay**, not verbosity. The rewrites are the same length.
What changes is where the fact sits: in the original it arrives one beat
late, so that it lands harder. The owner's report of the cost is the decisive
evidence — *"it hurts me more than it helps."* A reader who scans only
headlines leaves without the most important fact in the answer.

**Three causes, and the third was not expected:**

1. **The headline rule had no register constraint.** SKILL.md §7 said
   "headlines are labels instead of claims — rewrite them as claims", and
   *claim* invites rhetoric. The punchiest phrasing satisfies the letter of
   the rule.
2. **`Concise` plus claim-shaped produces epigram.** Compression pushed
   toward aphorism, which is the trailer register's native form.
3. **This repository's own documents were written that way**, and CLAUDE.md
   instructs them to demonstrate the contract they specify. They were
   functioning as an unintended style example. Cleaned up in the same change,
   in the places where a fact was actually being delayed — the sharp
   *rationale* addressed to the model stays, because it does not withhold
   anything.

**Decided:** a fifth contract row, **Direct** — the fact sits in the headline
and in the section's first sentence. Kept separate from `Didactic` rather
than folded into it, because D-018 gives that row a different test, and one
row carrying two tests that sometimes pull opposite ways is not checkable.

### The trap this must not fall into

Over-correcting is worse than the original. A headline stripped of its claim
becomes a label — "Analysis of the new accounts" — which the headline scan
was written to catch in the first place. The target is a three-way
distinction, not a two-way one: **a claim, not a label; a claim, not a
teaser.** One test separates them:

> **Could the reader disagree with it?** "The part that confuses everyone"
> admits no disagreement, so it is not a claim. "Totals do not sum the detail
> lines" can be wrong, so it is one.

**Reverses if:** artifacts written flat turn out to be *less* read to the
end — an engagement problem, not a taste one — or if a reader asks for a
livelier register by name.

---

## D-018 — When a term is load-bearing, build it from the ground up

**Status:** decided. Rewrites the `Didactic` row alongside D-017.

`Didactic` used to test only coverage: terms defined at first use, each idea
building on the last. That says nothing about what a definition owes a reader
who genuinely does not have the concept. Requested directly: use the Feynman
method for hard concepts, *"no frills, but didactically"*, and detect when it
is needed rather than waiting to be asked.

**"Use Feynman" alone is not actionable** — on its own it is a licence to
write more. Reduced to four checkable moves, in order:

| Move | Failure it prevents |
| --- | --- |
| Ordinary words first; the term once; then only the term | Two vocabularies running in parallel down the rest of the page |
| Anchor on a real instance from the reader's own domain | A borrowed analogy: a second thing to learn and then discard |
| Say what it is *not*, where the confusion is predictable | The right name and the wrong mental model |
| If it cannot be said without using the term itself, rewrite | "A row definition defines the report's rows" |

The second move is where "no frills" bites. **A concrete instance beats an
analogy**: row `25A` with `Totaling = 1000..1599` teaches more than any
comparison and introduces no second domain to discard afterwards. The third
move usually earns the most — naming the confusion is often worth more than
the definition correcting it.

### Detection, which is the hard half

Without a trigger the rule fires always and the artifact bloats. The
criterion is about the reader, not about the term:

> **Explain what the reader would have to go look up. Do not explain what
> they use every day.**

Evidence that they use it every day is observable: the term appears in their
prompt, in their repository, or in an earlier turn. Four triggers, any one
sufficient:

- They asked — "from scratch", "assume I know nothing".
- **The conclusion depends on it.** They cannot judge whether the answer is
  right without the term. The strongest of the four.
- It is a false friend: the term means something here it does not mean in
  ordinary use. A Dynamics `financial report` holds no numbers.
- It appears nowhere in what the reader wrote or in their code.

The negative case is a real cost, not a hypothetical one. In the artifact
that prompted this, the reader plainly owned dbt, seeds and views; defining
those would have read as condescension and spent the attention budget in the
wrong place.

### What it collides with

**`Concise` fights it.** "Every sentence carries something the reader does
not have yet" plus "complete beats concise" did not cover a section that
exists only to build vocabulary. So the chunking rules gain one: groundwork
precedes what depends on it and may take its own section — earned when a
trigger fired, padding when none did. That is the entire line between it and
slide theater.

**It also pushes against §1 activation.** Explained terms make artifacts
longer. Accepted: the artifact exists to cost the reader less than the
terminal did, and an unexplained term costs a search.

**Reverses if:** the triggers prove to fire on terms readers already knew
often enough that the groundwork sections read as padding. That is a
detection failure, and the fix would be narrowing the triggers, not dropping
the method.

---

## D-019 — The plugin root is `plugins/tasty-response/`, not `plugin/`

**Status:** superseded by D-020 on the same day. TR is not a plugin. The
finding about `plugin/` stands; the `plugins/<name>/` layout it produced was
removed.

The repository carried a `plugin/` directory holding `skills/tasty-response/`
directly. **Claude Code has no `plugin/` convention.** Components are found at
the *plugin root* — `skills/`, `hooks/`, `agents/`, `commands/`, `scripts/`,
`bin/` — and a directory named `plugin/` is just a directory. Nothing was
broken yet only because no manifest existed anywhere, so nothing had tried to
load it.

The manifest paths in `plugin.json` (`skills`, `hooks`, `agents`, …) could
have been pointed at the old location instead. Rejected: it spends a manifest
override to preserve a layout that has no reason to exist, and every reader
who knows the convention then has to discover that this repo opted out of it.

**Decided:** the shape `anthropics/claude-code` itself ships —

```
.claude-plugin/marketplace.json      # catalog, one entry
plugins/tasty-response/              # the plugin root
  .claude-plugin/plugin.json
  skills/tasty-response/
  hooks/            (M2)
  scripts/          (M2)
src/tr/  docs/  examples/  tests/    # repo, not plugin
```

Two properties made this the choice over putting the plugin at the repository
root:

| Property | Why it matters here |
| --- | --- |
| The repo is also a marketplace of one | `/plugin marketplace add viniciussena/tasty-response` then `/plugin install` works with no third-party catalog. A bare plugin repo with no `marketplace.json` has no such path |
| Plugin and repo stay separable | `src/tr/` (the installer CLI), `docs/`, `examples/` and `tests/` are repository concerns, not plugin contents. At the repo root they would sit among `skills/` and `hooks/` |

The manifest declares no component paths at all, which is the point: every
component sits where the convention already looks for it.

**Consequence worth stating:** the skill is invoked as
`tasty-response:tasty-response`. The repetition looks like a mistake and is
not — a plugin and its principal skill sharing a name is what Anthropic's own
`frontend-design` plugin does.

**Reverses if:** TR ever ships more than one plugin from this repository, in
which case nothing changes structurally — `plugins/` already holds the plural
case. Or if the marketplace-of-one turns out to be a worse install story than
publishing into an existing catalog, which would drop `marketplace.json` and
leave the rest intact.

---

## D-020 — TR is a skill distributed from GitHub, not a plugin

**Status:** decided. Supersedes D-019, drops the `tr` installer (M3), and
removes the premise of D-016.

Asked for directly: *"I want only a skill, not a plugin — on GitHub, easy and
ready to download, the way people have been doing it."*

Three findings made that cheaper than it sounds, and all three were verified
against current documentation and live repositories rather than assumed:

| Finding | Source | What it removed |
| --- | --- | --- |
| **A skill can declare hooks in its own frontmatter**, same format as settings files, registered on invocation for the rest of the session | Claude Code hooks docs, "Hooks in skills and agents" | The only thing the plugin was buying. D-016 said a skill could not register a hook; that was wrong |
| **`skills/<name>/SKILL.md` is the distribution layout** | `anthropics/skills`; the flat-layout search in `vercel-labs/skills` | Any need for a manifest, a marketplace catalog, or a `plugins/` level |
| **`npx skills add owner/repo` installs a skill from GitHub**, project scope by default and user scope with `-g` | `vercel-labs/skills` | The entire `tr setup` / `tr uninstall` installer — it would have reimplemented this |

**Decided:**

```
skills/tasty-response/     # the skill; copied verbatim on install
docs/  examples/  README.md  CLAUDE.md
```

Installation is one command, or a `cp -r` without Node. Nothing is written to
the user's `settings.json`, which removes the failure the original design
feared most — a half-written hook entry breaking every session. The skill
directory is all of TR, so uninstalling is deleting it.

### What was given up, stated plainly

- **Native `/plugin install`.** That route needs a `marketplace.json`, which
  is the plugin machinery this decision declines. `anthropics/skills` itself
  ships both a `skills/` tree and a marketplace. Adding one later is purely
  additive: the `skills/` layout would not move.
- **`tr config` and `tr doctor`.** Config becomes a hand-edited JSON file,
  all of it optional; natural-language opt-out already covers the common
  case. The doctor's checks move into the README as four manual steps.
- **The `.gitignore` entry `tr setup` would have written.** That job moves
  into SKILL.md, which now appends `.tasty-response/` before the first
  project-scope write. Moving it was necessary: architecture §3 asserting a
  behavior no component performed would repeat the mistake of D-014.

### Two things this makes unverified, not solved

A skill hook is registered **when the skill is invoked**. Whether it fires
for a `Write` inside that same turn — the very first artifact of a session —
is not stated anywhere. Neither is what a relative `./scripts/...` path in
the frontmatter resolves against. Both are M2 step 2, on a real machine.
Until then, the in-skill opener of D-016 stays, because it is the path known
to work.

**Reverses if:** the skill hook turns out unable to open the first artifact
of a session *and* no in-skill fallback is acceptable — at which point a
plugin's settings-level hook is the remaining option. Or if native
`/plugin install` becomes the expected route for skills, which would add a
`marketplace.json` without moving anything else.

---

## D-021 — The roadmap lives in the README, ordered by evidence

**Status:** decided. Replaces `docs/implementation-plan.md`, which is deleted.

Asked for directly: change the plan radically, keep a plugin rollout only as
a possible future to be decided later — or put it all in the README and drop
the file. The second was taken. Once TR became one skill with no installer
(D-020), the plan shrank to four steps, and a four-row table does not need a
document of its own. One fewer file is also one fewer place to drift: this
revision found `architecture.md` still describing a configuration file that
nothing read.

**Decided — four steps, each waiting for evidence from the one before:**

| Step | Earlier name | What changed |
| --- | --- | --- |
| 1. Validate the skill | M1 | Nothing. It remains the go/no-go |
| 2. Release v0.1 | M3 | Now "ready to download": `LICENSE`, `npx skills` verified in both scopes, README sufficient on its own |
| 3. Dogfood | M4 | Moved ahead of the hook |
| 4. Silent opener | M2 | **Moved last, and made conditional** |

Records before this one use the earlier names; the middle column translates.

**Why the hook moved from second to last, and became optional.** The
shell-step opener already works. The hook carries two questions nobody has
verified — whether it fires in the same turn it is registered, and what its
relative path resolves against — and its only gain over the current opener is
removing a permission prompt the reader can already remove by allowlisting
the command. Building it before dogfooding shows the prompt matters is
plumbing ahead of evidence, which is what CLAUDE.md tells this project not to
do.

**Deferred with a condition instead of planned.** Two ideas are listed in the
README under *Possible later*, each with what would justify deciding on it:

- **Plugin package.** Worth deciding on only if the skill's own hook cannot
  open the first artifact of a session, or if `/plugin` becomes the way
  people expect to install skills. The `skills/` directory would not move.
- **Config file.** Worth deciding on only if a setting needs to persist
  across sessions and plain language cannot carry it. Removed from
  architecture §6 rather than left there: it had no location and no reader,
  so describing it in detail was a doc asserting behavior the artifact does
  not have — the D-014 failure again.

**Reverses if:** dogfooding shows the permission prompt is costly from day
one, which pulls step 4 forward; or the roadmap grows past what a README
table carries, which brings back a separate document.

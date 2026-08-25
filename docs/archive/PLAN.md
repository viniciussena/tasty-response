# Project Plan: Visual-First Response Mode for Claude Code

**Name:** `tasty-response` (decided — referred to as TR below)

## 1. One-line pitch

A Claude Code plugin that, once enabled, makes Claude answer substantive
requests by generating a single self-contained, colorful, didactic HTML
artifact (slide-like, sectioned) and opening it automatically in the browser
— instead of, or in addition to, a wall of plain text in the terminal.

## 2. Problem

Long, technical, plain-text answers in a terminal/IDE chat pane are hard to
scan and re-read, especially for neurodivergent users (ADHD, autism,
dyslexia) but arguably for everyone doing dense technical work. The content
is often fine; the presentation forces a linear, undifferentiated read.

## 3. Relationship to prior art (research done before writing this plan)

- **brief-spec** (github.com/luanmorenommaciel/brief-spec, private/fork
  available) solves an adjacent but different problem: it standardizes the
  *structure* of the terminal handoff (Outcome Brief: Status → Outcome →
  Human action → Proof → Gaps → Next → Open), via hooks + skills across
  Codex/Claude/OMP/Grok/Kimi. It is markdown-first; HTML is one export
  format among several, generated on demand (`brief-spec export`), not the
  default live response mode. TR borrows its installer/scope pattern
  (user vs project, atomic install, doctor/uninstall) but is orthogonal in
  purpose: brief-spec standardizes *what fields appear*, TR standardizes
  *how any answer is visually rendered and auto-delivered*.
- **html-slides / reveal.js skills, frontend-slides, ss-make-slides**
  (marketplace skills): build presentation decks *on explicit request*
  ("make me a deck"). They are invoked skills, not a persistent response
  mode, and they optimize for pitch-deck aesthetics, not didactic density
  reduction for every answer.
- **neurodivergent-visual-org**: closest in spirit (ADHD/accessibility
  framing, Claude Code skill, auto-detection of overwhelm) but focused on
  task breakdowns/Mermaid roadmaps, not on turning arbitrary Q&A/plan
  responses into a styled single-file HTML that opens automatically.

No existing project found that combines: (a) always-on visual mode once
installed, (b) single self-contained HTML per response, (c) auto-open in
browser without the user asking, (d) explicit didactic writing principles
baked into the generation instructions, (e) brief-spec-style scope control
(project / user / global). This looks like a legitimate gap, not a
reinvented wheel — worth building.

## 4. Core concept

Two things ship together, mirroring brief-spec's shape:

1. **A skill** (`SKILL.md` + supporting templates/CSS) that defines:
   - The visual system: color palette(s), typography scale, spacing,
     section/"slide" chunking, dark/light themes.
   - The **didactic writing principles** the content itself must follow
     (see §5) — this is the part that actually reduces cognitive load; the
     styling alone is necessary but not sufficient.
   - The HTML generation contract: single file, no external requests
     (inline CSS/JS, no CDN dependency by default so it opens offline),
     semantic HTML, keyboard-navigable if slide-like.
2. **A hook** (UserPromptSubmit and/or Stop, à la brief-spec) that injects
   a short reminder into context so the behavior persists across turns
   without the user re-prompting each time, plus triggers the "save +
   open in browser" side effect after Claude writes the HTML.

## 5. Didactic principles (content contract, not just visual)

Codified as a short checklist the skill instructs Claude to apply before
finalizing any TR response, regardless of topic complexity:

- **Concise**: cut restatement and padding; say the thing once, well.
- **Concrete**: prefer examples, numbers, and named specifics over
  abstractions.
- **Complete**: don't drop necessary nuance for the sake of brevity — the
  goal is density reduction, not information loss.
- **Didactic**: assume the reader is smart but not yet oriented; define
  terms on first use, sequence ideas so each builds on the last.
- Chunk into sections/slides with one idea each; use visual hierarchy
  (headline, supporting point, detail) instead of uniform paragraphs.

These are principles, not a rigid field schema (explicitly *not* copying
brief-spec's fixed Status/Outcome/Proof/Gaps skeleton) — Vinícius wants the
answer's *shape* to stay free-form per topic, only the delivery mechanism
and quality bar to be standardized.

## 6. Trigger & delivery mechanics

- On a substantive response (heuristic similar to brief-spec's
  "activation: substantive" — skip trivial acks/short factual answers),
  Claude generates the HTML file to a predictable path, e.g.
  `.tasty-response/<timestamp>-<slug>.html` (project scope) or
  `~/.tasty-response/<timestamp>-<slug>.html` (user scope).
- A post-response hook opens it automatically:
  - macOS: `open <file>`
  - Linux: `xdg-open <file>`
  - Windows: `start <file>`
- Fallback: if the hook can't detect a GUI (headless/SSH), just print the
  path and skip auto-open — never block the terminal response on this.
- The plain-text/markdown answer can still be echoed briefly in the
  terminal (e.g. a 1-2 line summary + the file path) so the flow isn't
  fully opaque if the browser tab is missed.

## 7. Scope control

Same three-level control Vinícius asked for, matching brief-spec's model:

- `tr setup --scope project --project /path` → `.claude/` in that repo only.
- `tr setup --scope user` → applies to all of the user's Claude Code
  sessions (`~/.claude/`).
- A future `--scope global` if Claude Code ever supports a machine-wide
  policy layer; until then "user" is effectively global per-account.
- `tr config` for toggles: on/off, theme, activation threshold, whether to
  also keep the plain-text answer, per-project overrides.

## 8. MVP scope (v0.1)

Keep it deliberately smaller than brief-spec's v0.5 surface:

- Claude Code only (not Codex/OMP/Grok/Kimi) — validate the idea on one
  harness first.
- One default visual theme (colorful, high-contrast, dyslexia-friendly
  font stack), no theme marketplace yet.
- Single hook (Stop) + one skill.
- Manual `tr setup --scope {user,project}` installer, no auto-detection
  matrix yet.
- No PDF/audio export (brief-spec already does that well if ever needed).

## 9. Proposed repo structure

```
tasty-response/
  skills/
    visual-brief/
      SKILL.md          # style system + didactic principles + HTML contract
      templates/
        base.html        # skeleton, inlined CSS, theme variables
      themes/
        default.css
  hooks/
    stop-open-browser.*  # writes file, opens it, per-OS dispatch
    user-prompt-reminder.*
  src/
    vb/
      cli.py             # setup / uninstall / config / doctor
      installer.py        # project vs user scope, atomic writes
      config.py
  schemas/
    config.schema.json
  docs/
    architecture.md
    design-principles.md
  tests/
  README.md
  plugin.json            # Claude Code plugin manifest
```

## 10. Open questions for the next session

- Does Claude Code's current hook system expose a clean "final assistant
  message" interception point, or does the HTML have to be generated by
  Claude itself as a normal tool-use step (simpler, no interception
  needed — just an instruction to always also produce the file)?
- Should TR ever *replace* the terminal text, or always keep both? (Leaning
  toward: always keep a short terminal summary — full replacement risks
  losing content when the browser isn't watched.)
- Per-conversation opt-out phrase (e.g. "no HTML this time") — worth
  supporting from v0.1 or deferred?
- ~~Naming~~ — decided, see §11.

## 11. Naming — decided: `tasty-response`

Chosen after a longer brainstorm across several axes (didactic/clarity,
reaction/wow, pain-naming, ergonomics/friction, pleasant/sensory). The
pain identified along the way: dense plain-text answers force the reader
to build the hierarchy themselves (cognitive cost); TR removes that by
delivering the structure already built, in an affectively pleasant,
colorful, low-friction package. `tasty-response` won because it captures
the affective/sensory "I want to read this" reaction directly, is short
and memorable, and doesn't collide with existing skills in this space —
at the cost of not self-announcing the HTML/visual mechanism on its own,
so the repo tagline needs to carry that: *"tasty-response: turns any
answer into a colorful, single-page HTML you actually want to read."*

Runner-up axes explored, kept for context:

| Axis | Examples | Why not chosen |
| --- | --- | --- |
| Didactic/clarity | `clear-response`, `readable-response` | accurate but generic, low "wow" |
| Reaction/wow | `Aha`, `Tcharam`, `Prisma` | fun but not self-explanatory to a dev at a glance |
| Pain-naming | `unburden-response`, `nostrain-response` | named the symptom, not the fix; didn't resonate |
| Ergonomics/friction | `frictionless-response`, `ergo-response` | precise but clinical, less "wow" |
| Pleasant/sensory | `pleasant-response`, `cozy-response` | close, but `tasty-response` won on memorability |

## 12. Naming brainstorm (full log)

Preference stated: favor names that are self-explanatory to a developer at
a glance — same logic as `brief-spec` (you read the name, you know it hands
you a brief spec). Visual/didactic angle, not a mood word.

Descriptive, `brief-spec`-style compounds (say what it does):

| Name | Reads as |
| --- | --- |
| `visual-brief` | current working name; a brief, but visual |
| `clear-brief` | a brief, but clear/legible |
| `view-brief` | a brief you view, not read |
| `html-brief` | literal: brief rendered as HTML |
| `easy-brief` | a brief that's easy to consume |
| `slide-brief` | a brief rendered slide-style |
| `open-brief` | a brief that opens itself (double meaning: auto-opens + open format) |

Single descriptive words (plain, literal, no compound needed):

| Name | Reads as |
| --- | --- |
| `clearview` | you see the answer clearly |
| `plainview` | plain, unobstructed answer |
| `legible` | literally "readable" |
| `readably` | adverb form, reads as a brand |
| `didact` | teaches; short, techy suffix |
| `explainer` | does what it says, maybe too generic/taken |
| `unfold` | the answer "unfolds" into a visual page |

Discarded from the earlier round (reaction-based, not descriptive — kept
for the record since they were fun, but they fail the "developer glances
and knows" test you just set): `Aha`, `Tcharam`, `Uau`, `Prisma`.

Leaning candidates given the stated preference: `visual-brief` (safest,
already used throughout this doc) or `clearview` (shortest, still
self-explanatory, easy CLI verb: `clearview setup`).

## 13. Immediate next steps

1. Initialize the `tasty-response` repo with the structure in §9.
2. Draft `SKILL.md` v0 (style system + didactic checklist) and test it by
   hand on 2-3 real past answers (e.g. an ECRI or dbt explanation) to see
   if the HTML output actually reads better.
3. Prototype the Stop hook's "write + open" behavior on Windows, macOS,
   and WSL (Vinícius already has a Windows setup guide from the AVAD
   Claude Code rollout — reuse that groundwork).
4. Write the `tr setup --scope` installer, copying brief-spec's atomic
   install/uninstall/receipt pattern rather than reinventing it.

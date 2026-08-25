# tasty-response

> Turns any Claude Code answer into a colorful, single-page HTML you actually want to read.

**Status: M1.** The skill and the visual system exist and are installable by
hand; the hook that auto-opens the browser and the `tr` installer do not yet.
See [docs/implementation-plan.md](docs/implementation-plan.md) for what is
still missing and what has to be true before it lands.

## The problem

A long technical answer in a terminal pane is a wall. The information is
usually fine; the *presentation* forces a linear, undifferentiated read, and
the reader has to build the hierarchy in their head. That cost is highest for
neurodivergent readers (ADHD, autism, dyslexia) but it is paid by everyone
doing dense technical work.

## What tasty-response does

Once installed, substantive answers are also written as a **single
self-contained HTML file** — sectioned, high contrast, dark by default — and
**opened automatically in your browser**. The terminal keeps a short summary
plus the file path, so nothing is lost if you miss the tab.

*(The auto-open half is M2 and not built yet — today the path is printed and
you open it.)*

```
you ask something substantive
        |
        v
Claude answers  ->  writes .tasty-response/2026-08-25-1432-topic.html
        |                        |
        v                        v
 2-line terminal          hook opens it in
 summary + path            your browser
                                 |
                                 v
                      docket: which project, what
                      you asked, what was attached
                      then the answer, in sections
```

Four properties distinguish it from adjacent tools:

| Property | Why it matters |
| --- | --- |
| Always-on, not invoked | You never ask for the visual; it is the default response mode |
| One self-contained file | No CDN, no network requests — opens offline, survives being emailed |
| Content contract, not just CSS | The writing itself must be concise, concrete, complete, didactic |
| Every page opens with a docket | Project, path, and what you asked — so six open tabs stay tellable apart |

## Is this wasteful?

Yes. It costs more tokens, and it takes longer.

It is worth every token and every extra second. You were going to read that
answer three times anyway — once to find the shape, once to find the part you
needed, once because you lost it. This pays that tax up front, once, in a
file you can send to someone else.

Good food takes longer than instant noodles. That is not a bug in the recipe.

## Themes

Four palettes ship, each a direction rather than a hue shift of the others.
`patisserie` is the default; the rest are selectable per artifact.

| Theme | Reads as |
| --- | --- |
| `patisserie` *(default)* | Dark chocolate counter — raspberry, pistachio, caramel |
| `cellar-gold` | Wine list — aubergine ground, gold leaf |
| `charred-citrus` | Cast iron, night market — yolk, lime, blood orange |
| `matcha-ceramic` | Kissaten — matcha, persimmon, plum |

Dark is the default in all four; light is one click away and persists. Every
palette passes WCAG AA in both modes, verified by a script rather than by
eye, and the display face travels inside the file as base64 — so the page is
still one self-contained document that opens offline.

## Scope control

Installation is explicit and reversible, at one of two levels:

- `--scope project` — writes into `.claude/` of one repository.
- `--scope user` — writes into `~/.claude/`, applying to every session.

## Documentation

| Document | What it covers |
| --- | --- |
| [docs/architecture.md](docs/architecture.md) | Components, control flow, hook integration, config schema, failure modes |
| [docs/design-principles.md](docs/design-principles.md) | The didactic content contract and the visual system spec |
| [docs/decisions.md](docs/decisions.md) | Decision records, including the ones that closed the original open questions |
| [docs/implementation-plan.md](docs/implementation-plan.md) | Milestones, exit criteria, risks |
| [CLAUDE.md](CLAUDE.md) | Working agreement for Claude Code inside this repository |

## Prior art

`tasty-response` was designed after surveying the adjacent space, and it sits
in a real gap rather than duplicating existing work:

- **brief-spec** standardizes *which fields* a terminal handoff contains
  (Status, Outcome, Proof, Gaps, Next). tasty-response leaves the answer's
  shape free and standardizes *how it is rendered and delivered*. The
  installer pattern — scoped install, atomic writes, doctor, uninstall — is
  deliberately borrowed.
- **Slide-deck skills** (html-slides, reveal.js, ss-make-slides) build decks
  *on request*, optimized for pitch aesthetics. They are invoked, not a
  persistent response mode.
- **neurodivergent-visual-org** shares the accessibility framing but targets
  task breakdowns and Mermaid roadmaps, not arbitrary Q&A rendering.

The full reasoning, including the naming brainstorm, lives in
[docs/decisions.md](docs/decisions.md); the original planning document is
archived at [docs/archive/PLAN.md](docs/archive/PLAN.md).

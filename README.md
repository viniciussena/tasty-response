# tasty-response

> Turns any Claude Code answer into a colorful, didactic single-page HTML you actually want to read.

**Status: works, not yet validated.** The skill installs, writes the
artifact, and opens it. Whether the artifact actually reads *better* than the
terminal answer has not been tested on real dense answers yet — that is the
next step, and it decides whether the project continues. See
[Roadmap](#roadmap).

## Install

```bash
npx skills add viniciussena/tasty-response -a claude-code      # this project only
npx skills add viniciussena/tasty-response -g -a claude-code   # every project
```

That is the whole installation. It is a single [Claude Code
skill](https://code.claude.com/docs/en/skills) — one directory — installed
by [`npx skills`](https://github.com/vercel-labs/skills). Nothing is written to
your `settings.json`.

**Without Node**, copy the directory yourself:

```bash
git clone https://github.com/viniciussena/tasty-response
cp -r tasty-response/skills/tasty-response ~/.claude/skills/          # every project
cp -r tasty-response/skills/tasty-response .claude/skills/            # this project only
```

Then **start a new Claude Code session** and ask something substantive.

**To remove it**, run `npx skills remove tasty-response -a claude-code` (add
`-g` if you installed globally), or delete the directory by hand. TR itself
keeps nothing anywhere else except the artifacts it wrote to
`.tasty-response/`.

One thing `npx skills` leaves behind: in project scope it writes a
`skills-lock.json` at the project root, and `remove` deletes the skill but
**not** that file's `tasty-response` entry. Delete the entry — or the file,
if TR was its only skill — yourself.

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

*(The skill runs the opener itself as a shell step, so the first one in a
session may ask for permission. Allowlisting the command removes the prompt.
A silent hook is on the [Roadmap](#roadmap), only if the prompt turns out to
matter.)*

```
you ask something substantive
        |
        v
Claude answers  ->  writes .tasty-response/2026-08-25-1432-topic.html
        |                        |
        v                        v
 2-line terminal          it opens in
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
| Content contract, not just CSS | The writing itself must be concise, concrete, complete, direct, and didactic |
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
`charred-citrus` is the default; the rest are selectable per artifact.

| Theme | Reads as |
| --- | --- |
| `charred-citrus` *(default)* | Cast iron, night market — yolk, lime, blood orange |
| `cellar-gold` | Wine list — aubergine ground, gold leaf |
| `patisserie` | Dark chocolate counter — raspberry, pistachio, caramel |
| `matcha-ceramic` | Kissaten — matcha, persimmon, plum |

**To see them:** open [examples/index.html](examples/index.html) locally — a
contact sheet of all four palettes in both modes, linking to the same answer
rendered in each. Regenerate with `python examples/render.py`. (GitHub will
not render these; clone and open them.)

Dark is the default in all four; light is one click away and persists. Every
palette passes WCAG AA in both modes, verified by a script rather than by
eye, and both the display and body faces travel inside the file as base64 —
so the page is still one self-contained document that opens offline.

## Turning it off

Say so. *"No HTML this time"* skips one answer; *"turn off tasty-response"*
skips the rest of the session. Nothing to configure, and the skill never
argues. To remove it for good, delete its directory (see Install).

## Checking an install

If artifacts are not appearing, check these four, in order:

1. The directory exists at `~/.claude/skills/tasty-response/` or
   `.claude/skills/tasty-response/`, with `SKILL.md` directly inside it.
2. You started a **new** session after installing.
3. The answer was substantive — TR deliberately skips short ones.
4. `.tasty-response/` exists in the project and is writable. If the file is
   there but no tab opened, the opener was skipped; the path in the terminal
   still works.

## Roadmap

Ordered by evidence: each step waits until the one before it has shown it is
worth doing.

| Step | State | Done when |
| --- | --- | --- |
| **1. Validate the skill** | **Now** | Two or three real dense answers, regenerated under the skill, read *better* than the originals — a specific fact is found faster, and the headlines alone still deliver the answer |
| **2. Release v0.1** | Mostly done | A `LICENSE` exists; `npx skills add` is verified in both scopes on a clean machine; someone new gets a first artifact from this README alone |
| **3. Dogfood** | After release | A normal week of real work without wanting to turn it off, counting artifacts that fired when they should not have and the ones that were missed |
| **4. Silent opener** | Only if step 3 asks | The shell-step permission prompt proves to be a real cost. Then a `PostToolUse` hook in the skill's frontmatter — after checking on a real machine that it fires in the same turn it is registered |

**Step 1 is the go/no-go.** If the output is a styled wall of the same prose,
the content contract is not working, and the skill is rewritten before
anything else happens. No amount of packaging fixes a page that is not easier
to read.

**One rule holds at every step:** TR must never fail a Claude Code turn. A
broken opener degrades to "the file exists, the path is in the terminal" —
never to an error.

### Possible later, to be decided later

Neither of these is planned. Each has a condition that would put it on the
table, and until that condition shows up it stays here.

| Idea | What it would add | What would justify deciding on it |
| --- | --- | --- |
| **Ship as a Claude Code plugin** | Native `/plugin install`, and a hook registered in settings — active before the first turn, not only after the skill's first use | The skill's own hook proves unable to open the first artifact of a session, or `/plugin` becomes the way people expect to install skills. The `skills/` directory would not move either way |
| **A config file** | Persistent settings: a default theme, output directory, retention | A setting people want to keep across sessions that asking in plain language cannot carry. Today "turn off tasty-response" and "use cellar-gold" cover what has come up |

## Documentation

| Document | What it covers |
| --- | --- |
| [docs/architecture.md](docs/architecture.md) | Layout, control flow, opening the artifact, failure modes |
| [docs/design-principles.md](docs/design-principles.md) | The didactic content contract and the visual system spec |
| [docs/decisions.md](docs/decisions.md) | Decision records: what was decided, why, and what would reverse it |
| [CLAUDE.md](CLAUDE.md) | Working agreement for Claude Code inside this repository |

## Prior art

`tasty-response` was designed after surveying the adjacent space, and it sits
in a real gap rather than duplicating existing work:

- **brief-spec** standardizes *which fields* a terminal handoff contains
  (Status, Outcome, Proof, Gaps, Next). tasty-response leaves the answer's
  shape free and standardizes *how it is rendered and delivered*.
- **Slide-deck skills** (html-slides, reveal.js, ss-make-slides) build decks
  *on request*, optimized for pitch aesthetics. They are invoked, not a
  persistent response mode.
- **neurodivergent-visual-org** shares the accessibility framing but targets
  task breakdowns and Mermaid roadmaps, not arbitrary Q&A rendering.

The full reasoning, including the naming brainstorm, lives in
[docs/decisions.md](docs/decisions.md); the original planning document is
archived at [docs/archive/PLAN.md](docs/archive/PLAN.md).

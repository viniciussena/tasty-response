# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`tasty-response` (TR) is a **Claude Code skill** — one directory, not a
plugin — that makes substantive answers render as a single self-contained
HTML artifact, opened automatically in the browser, instead of a wall of
terminal text. It is distributed straight from GitHub and installed with
`npx skills add viniciussena/tasty-response` (D-020). Tagline: *turns any
Claude Code answer into a colorful, didactic single-page HTML you actually
want to read.*

## Current state: validating the skill (roadmap step 1)

**There is no test suite and no dependency manifest.** The only tooling is
the two scripts below, which need nothing but a stdlib Python. Do not invent
commands for tooling that does not exist. There is no `tr` CLI and none is
planned — installation is `npx skills` or a directory copy (D-020).

What exists:

| Path | State |
| --- | --- |
| `docs/` | Complete. The design is settled; see the table below |
| `skills/tasty-response/` | **The skill — this whole directory is what gets installed.** Copied verbatim to `.claude/skills/tasty-response/` |
| `.../SKILL.md` | v0 written, **not yet validated** |
| `.../styles/core.css` | Structure and components. **Zero color literals** — that invariant is what makes a theme one file |
| `.../themes/*.css` | Four palettes, tokens only. `charred-citrus` is the default (D-012) |
| `.../fonts/tr-body.css` | Atkinson Hyperlegible 400/700, subset, base64. ~24KB (D-014) |
| `.../fonts/tr-display-*.css` | Display options, one per file. `nunito` is the default; `fraunces` is kept as the serif alternative (D-015) |
| `.../fonts/licenses/` | OFL texts, inside the skill so they travel with the fonts wherever it is installed |
| `.../templates/base.html` | **Generated** by `build.py`. Never hand-patch it — edit the source part and rebuild |
| `.../scripts/`, frontmatter `hooks:` | Not started, and conditional — built only if dogfooding shows the shell-step prompt matters (roadmap step 4) |
| `LICENSE` | Missing. Needed for release (roadmap step 2) |

Two scripts gate changes to the visual system, and both must pass:

```bash
cd skills/tasty-response
python build.py --check        # base.html still matches its sources
python check-contrast.py       # every theme passes WCAG AA, both modes
python build.py --theme cellar-gold   # rebuild with a different palette
cd ../.. && python examples/render.py   # regenerate the example artifacts
```

`examples/` holds one real answer rendered in every theme, plus a contact
sheet. Both are generated — the swatches are parsed out of the theme files,
so they cannot drift. Re-run `render.py` after any change to the visual
system.

The open task is roadmap step 1: regenerate 2-3 real dense past answers under
the skill and judge whether the artifact reads *better*, not merely prettier.
The roadmap lives in the README — there is no separate plan document (D-021).
Until that passes, treat the skill as unproven and do not build plumbing
around it.

Everything inside `skills/tasty-response/` ships to every user who installs.
Anything that is for developing TR rather than running it — docs, examples —
belongs **outside** that directory. `build.py` and
`check-contrast.py` are the accepted exception: small, stdlib-only, and useful
to anyone who wants to rebuild with another theme.

## Where the design lives

Read these before proposing changes; they are the source of truth and they
disagree with the archived plan in places.

| Document | Authoritative for |
| --- | --- |
| [README.md](README.md) | Install, and the **Roadmap** — step order, what counts as done, and what is deferred until evidence asks for it |
| [docs/architecture.md](docs/architecture.md) | Layout, control flow, opening the artifact, failure modes |
| [docs/design-principles.md](docs/design-principles.md) | Content contract and visual system |
| [docs/decisions.md](docs/decisions.md) | Why things are the way they are, and what would reverse them |
| [docs/archive/PLAN.md](docs/archive/PLAN.md) | Historical only — **superseded**, do not treat as current |

## Constraints that are easy to violate

These are the decisions most likely to be undone by accident:

- **The hook never intercepts the assistant message.** Claude writes the
  artifact as an ordinary `Write` step; a `PostToolUse` hook only opens it
  (D-002). Any design that depends on rewriting rendered output is wrong.
- **The hook can never fail a turn.** It exits 0 unconditionally. Every
  failure degrades to "the file exists, the path was printed" (architecture
  §5). A broken opener breaking a Claude Code session is a release blocker.
- **Artifacts are fully self-contained.** Inlined CSS/JS, no CDN, no remote
  fonts, no external requests — the file must open offline years from now
  (D-007).
- **The terminal always keeps something.** Default is a short summary plus
  the path; the artifact never fully replaces the answer (D-003).
- **Activation errs toward skipping.** A spurious browser tab is more costly
  than a missing one, because it trains the user to ignore the mode (D-006).
- **Style is not the lever.** The content contract — concise, concrete,
  complete, direct, didactic — is what reduces cognitive load. A beautifully themed
  wall of unrestructured prose is the project's main failure mode.
- **Least friction wins ties.** When a choice is between the more legible
  option and the more elegant one, legibility takes it — even when the
  elegant one is better looking and already built (D-015). "Cool" is not a
  premise this project optimizes for.
- **A claim in the docs is not a property of the artifact.** Anything the
  documentation asserts about the output must be verified against a real
  machine, not against the CSS (D-014).

## Skill structure facts

Verified against the current Claude Code docs and against `anthropics/skills`
and `vercel-labs/skills`. An earlier layout got these wrong (D-019, D-020):

- **A skill is a directory named after itself, holding `SKILL.md`.** No
  manifest, no registry. It lives at `.claude/skills/<name>/` (project) or
  `~/.claude/skills/<name>/` (user), and the directory existing *is* the
  installation.
- **`skills/<name>/SKILL.md` is the distribution layout.** Both
  `anthropics/skills` and the `npx skills` flat-layout search use it.
- **Never put a `SKILL.md` at the repository root.** `npx skills` lets a
  shallower `SKILL.md` shadow everything nested below it, so a root one would
  hide the real skill. The same applies to `.claude/skills/` in this repo,
  which `npx skills` also searches.
- **A skill can declare hooks in its own frontmatter** (`hooks:`, same format
  as settings files). Claude Code registers them on invocation and keeps them
  for the session. That is why TR needs no plugin and never touches the
  user's `settings.json`.
- Whether such a hook fires for a `Write` in the *same* turn it was
  registered, and what a relative `./scripts/...` resolves against, are
  **unverified**. Settle them on a real machine before building the hook
  (roadmap step 4, architecture §2).

## Conventions

- Documentation is written in English, even though project discussion happens
  in Portuguese.
- Decisions go in `docs/decisions.md` as a numbered record with a reversal
  condition — not as prose buried in another document.
- The repository's own documents should demonstrate the content contract they
  specify. If a doc here reads as a wall, it is failing its own spec.

## A note on dogfooding

Developing TR is not the same as running TR. Unless the skill is actually
installed in this session, answers here are ordinary Claude Code answers —
do not generate `.tasty-response/` artifacts by hand to simulate the feature.

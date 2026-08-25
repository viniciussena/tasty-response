# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`tasty-response` (TR) is a Claude Code plugin that makes substantive answers
render as a single self-contained HTML artifact, opened automatically in the
browser, instead of a wall of terminal text. Tagline: *turns any answer into
a colorful, single-page HTML you actually want to read.*

## Current state: M1 in progress

**There is no build, no test suite, and no dependency manifest.** Do not
invent commands for tooling that does not exist, and do not report a `tr` CLI
as runnable — it is specified, not built.

What exists:

| Path | State |
| --- | --- |
| `docs/` | Complete. The design is settled; see the table below |
| `plugin/skills/tasty-response/SKILL.md` | v0 written, **not yet validated** |
| `.../styles/core.css` | Structure and components. **Zero color literals** — that invariant is what makes a theme one file |
| `.../themes/*.css` | Four palettes, tokens only. `patisserie` is the default (D-012) |
| `.../fonts/tr-display.css` | Fraunces SuperSoft Bold, subset, base64. ~22KB (D-013) |
| `.../templates/base.html` | **Generated** by `build.py`. Never hand-patch it — edit the source part and rebuild |
| `plugin/hooks/`, `src/tr/`, `schemas/` | Not started (M2, M3) |

Two scripts gate changes to the visual system, and both must pass:

```bash
cd plugin/skills/tasty-response
python build.py --check        # base.html still matches its sources
python check-contrast.py       # every theme passes WCAG AA, both modes
python build.py --theme cellar-gold   # rebuild with a different palette
```

The open task is M1 step 3: regenerate 2-3 real dense past answers under the
skill and judge whether the artifact reads *better*, not merely prettier.
Until that passes, treat the skill as unproven and do not build plumbing
around it.

The planned commands, once M3 lands, are `tr setup --scope {project,user}`,
`tr uninstall`, `tr config`, and `tr doctor`. See
[docs/implementation-plan.md](docs/implementation-plan.md) for what must be
true before each exists.

## Where the design lives

Read these before proposing changes; they are the source of truth and they
disagree with the archived plan in places.

| Document | Authoritative for |
| --- | --- |
| [docs/architecture.md](docs/architecture.md) | Layout, control flow, hooks, config schema, failure modes |
| [docs/design-principles.md](docs/design-principles.md) | Content contract and visual system |
| [docs/decisions.md](docs/decisions.md) | Why things are the way they are, and what would reverse them |
| [docs/implementation-plan.md](docs/implementation-plan.md) | Milestone order and exit criteria |
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
  complete, didactic — is what reduces cognitive load. A beautifully themed
  wall of unrestructured prose is the project's main failure mode.

## Plugin structure facts

Verified against a real installed plugin, and differing from the archived
plan:

- The manifest is `.claude-plugin/plugin.json`, not a root `plugin.json`.
- Hooks live in `hooks/hooks.json` as `{"hooks": {"<Event>": [...]}}`, and
  hook commands reference their files via `${CLAUDE_PLUGIN_ROOT}`.
- The Python package is `src/tr/`. Any reference to `src/vb/` is a leftover
  from the abandoned `visual-brief` name.

## Conventions

- Documentation is written in English, even though project discussion happens
  in Portuguese.
- Decisions go in `docs/decisions.md` as a numbered record with a reversal
  condition — not as prose buried in another document.
- The repository's own documents should demonstrate the content contract they
  specify. If a doc here reads as a wall, it is failing its own spec.

## A note on dogfooding

Developing TR is not the same as running TR. Unless the plugin is actually
installed in this session, answers here are ordinary Claude Code answers —
do not generate `.tasty-response/` artifacts by hand to simulate the feature.

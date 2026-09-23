# Architecture

Specification for `tasty-response` (TR) v0.1. Nothing here is implemented
yet; this document is the contract the implementation must satisfy.

## 1. Component map

TR ships as a **Claude Code plugin** with four parts:

| Component | Path in repo | Responsibility |
| --- | --- | --- |
| Skill | `plugins/tasty-response/skills/tasty-response/SKILL.md` | Instructs Claude *what* to generate: visual system, didactic contract, HTML rules |
| Hook config | `plugins/tasty-response/hooks/hooks.json` | Registers the events TR listens to |
| Hook script | `plugins/tasty-response/scripts/open-artifact.*` | Side effect: open the generated file in a browser, per OS |
| Installer CLI | `src/tr/` | `setup` / `uninstall` / `config` / `doctor`, scoped project or user |

### Corrections to the original plan

The layout in the archived PLAN.md §9 predates verification against a real
installed plugin. Three things differ and the implementation must follow the
verified form:

- The manifest is `.claude-plugin/plugin.json`, **not** a root-level
  `plugin.json`.
- **Components live at the plugin root, and there is no `plugin/` directory
  convention.** `skills/`, `hooks/`, `scripts/` sit directly inside the
  plugin, and the plugin itself is one directory under `plugins/` with a
  repo-root marketplace catalog pointing at it (D-019). An earlier draft of
  this document specified `plugin/skills/...`, which Claude Code does not
  recognize.
- Hook configuration is `hooks/hooks.json` (a `{"hooks": {...}}` object keyed
  by event name), and hook commands reference their own files through the
  `${CLAUDE_PLUGIN_ROOT}` variable.
- The Python package is `src/tr/`, not `src/vb/` — `vb` was the abandoned
  `visual-brief` working name.

### Target repository layout

```
tasty-response/
  .claude-plugin/
    marketplace.json     # catalog: one entry, pointing at ./plugins/tasty-response
  plugins/
    tasty-response/            # ← the plugin root; ${CLAUDE_PLUGIN_ROOT} resolves here
      .claude-plugin/
        plugin.json      # manifest: name, version, description, author, keywords
      skills/tasty-response/
        SKILL.md           # the response-mode contract
        build.py           # assembles templates/base.html from the parts below
        check-contrast.py  # WCAG gate every theme must pass
        styles/core.css    # structure; zero color literals
        themes/*.css       # four palettes, tokens only
        fonts/tr-body.css tr-display-nunito.css tr-display-fraunces.css
        fonts/licenses/*.txt
        templates/base.html   # GENERATED — never hand-patch
        templates/_head.html templates/_tail.html
      hooks/hooks.json
      scripts/open-artifact.sh
      scripts/open-artifact.ps1
  src/tr/
    cli.py  installer.py  config.py
  schemas/config.schema.json
  docs/
  examples/
  tests/
```

## 2. Control flow

The central design question from the original plan was whether a hook can
intercept and replace the final assistant message. It cannot — a `Stop` hook
can read the transcript and can *block* to force continuation, but it has no
mechanism to rewrite what was already rendered. TR therefore does not
intercept anything.

**Claude writes the artifact itself, as an ordinary tool step. A hook only
opens it.** This is simpler, has no privileged interception requirement, and
degrades gracefully: if the hook never fires, the file still exists.

```
UserPromptSubmit
      |  hook injects a one-line reminder of the TR contract
      v
Claude reasons and answers
      |  skill instructs: also Write the artifact
      v
Write .tasty-response/<timestamp>-<slug>.html
      |
      v
PostToolUse (matcher: Write)
      |  script checks the path is a TR artifact, then opens it
      v
browser opens          terminal shows 2-line summary + path
```

### Why `PostToolUse` on `Write`, not `Stop`

`PostToolUse` fires immediately after the file exists, so the browser opens
while Claude is still writing the terminal summary — the page is ready by the
time the reader looks up. A `Stop` hook would work too but adds latency and
requires re-deriving which file was just written from the transcript. `Stop`
is kept as a fallback only if `PostToolUse` matching proves unreliable.

**The `UserPromptSubmit` reminder is what makes the mode persistent.** A skill
alone is consulted when relevant; the injected reminder is what keeps the
behavior alive across a long session without the user re-asking.

## 3. Artifact location and naming

| Scope | Directory |
| --- | --- |
| project | `.tasty-response/` at the repo root |
| user | `~/.tasty-response/` |

Filename: `<YYYY-MM-DD>-<HHMM>-<slug>.html`, where `slug` is a kebab-case
reduction of the answer's topic, capped at 40 characters. Sorting by name
sorts by time, which is the property that matters when the directory grows.

`tr setup --scope project` must add `.tasty-response/` to the repository's
`.gitignore`. Artifacts are disposable output, not source.

## 4. Activation heuristic

The skill must decide, per response, whether an artifact is warranted.
Generate one when **any** of these hold:

- The answer contains more than roughly 15 lines of prose, or 3+ distinct
  sections.
- The answer explains a system, compares options, or lays out a plan.
- The user explicitly asks for a visual, a diagram, or a page.

Skip when:

- The answer is an acknowledgement, a confirmation, or a single fact.
- The user is mid-debug and wants a fast, terse loop.
- The session's config sets `enabled: false`, or the user has used the
  opt-out phrase this turn.

The heuristic errs toward *skipping*. A missing artifact costs a scroll; a
spurious one costs a browser tab and trains the user to ignore the mode.

## 5. Opening the artifact

| OS | Command |
| --- | --- |
| macOS | `open <file>` |
| Linux (GUI) | `xdg-open <file>` |
| Windows | `start "" <file>` |
| WSL | `wslview <file>`, falling back to `explorer.exe` on the translated path |

**The hook must never block or fail the response.** It exits 0
unconditionally. Every failure path degrades to "the file exists, the path was
printed":

| Condition | Detection | Behavior |
| --- | --- | --- |
| Headless / SSH | no `DISPLAY`/`WAYLAND_DISPLAY`, `SSH_CONNECTION` set | skip open, path only |
| Opener missing | command not found | skip open, path only |
| Open command hangs | timeout (3s) | detach or abandon, never block |
| Path is not a TR artifact | prefix + extension check | no-op |
| `auto_open: false` | config | skip open, path only |

The path check is a security boundary, not just tidiness: the hook receives a
path chosen by the model and must refuse anything outside the configured
artifact directory.

## 6. Configuration

Stored per scope, validated by `schemas/config.schema.json`:

| Key | Type | Default | Effect |
| --- | --- | --- | --- |
| `enabled` | bool | `true` | Master switch for the response mode |
| `auto_open` | bool | `true` | Whether the hook opens the browser |
| `theme` | enum | `"charred-citrus"` | `charred-citrus` \| `cellar-gold` \| `patisserie` \| `matcha-ceramic` (D-012) |
| `activation` | enum | `"substantive"` | `substantive` \| `always` \| `on-request` |
| `keep_terminal_text` | enum | `"summary"` | `summary` \| `full` \| `path-only` |
| `artifact_dir` | string | scope default | Override the output directory |
| `retention_days` | int | `30` | `tr doctor` offers to prune older artifacts |

Project config overrides user config key by key. A project that sets nothing
inherits everything.

## 7. Installer semantics

Borrowed wholesale from brief-spec, because the pattern is sound:

- **Atomic** — write to a temporary path, then rename. A failed install must
  never leave a half-written hook that breaks the user's sessions.
- **Receipt** — record every file created and every settings key touched, so
  `tr uninstall` removes exactly what was added and nothing else.
- **Idempotent** — re-running `setup` on an existing install upgrades in
  place rather than duplicating hook entries.
- **`tr doctor`** — verify the hook is registered, the skill is discoverable,
  the opener command exists for this OS, and the artifact directory is
  writable and gitignored. Report, do not silently repair.

## 8. Non-goals for v0.1

Claude Code only (no Codex/Gemini/other harnesses). One theme. No PDF or
audio export. No auto-detection matrix in the installer. No `--scope global`
until Claude Code exposes a machine-wide policy layer; `user` is effectively
global per account.

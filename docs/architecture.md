# Architecture

Specification for `tasty-response` (TR) v0.1. Nothing here is implemented
yet; this document is the contract the implementation must satisfy.

## 1. Component map

TR ships as a **Claude Code skill** — not a plugin, and with no installer of
its own (D-020). Three parts, all inside one directory:

| Component | Path in repo | Responsibility |
| --- | --- | --- |
| Skill | `skills/tasty-response/SKILL.md` | Instructs Claude *what* to generate: visual system, didactic contract, HTML rules |
| Hook | frontmatter `hooks:` inside that same `SKILL.md` | Registers `PostToolUse` so the artifact opens without a shell step (M2) |
| Hook script | `skills/tasty-response/scripts/open-artifact.*` | Side effect: open the generated file in a browser, per OS |

The skill directory is self-contained: everything it needs at runtime lives
inside it, so installing is copying one directory and uninstalling is
deleting it.

### Verified against the current docs

Two facts govern the layout, and an earlier draft of this document had both
wrong:

- **A skill is a directory named after itself, holding `SKILL.md`.** It
  installs at `~/.claude/skills/<name>/` for user scope or
  `.claude/skills/<name>/` for project scope. There is no manifest and no
  registry — the directory existing *is* the installation.
- **`skills/<name>/SKILL.md` is the distribution convention.** It is the
  layout `anthropics/skills` uses, and the "flat layout" `npx skills` searches
  first. A `SKILL.md` at the repository root would shadow it, so there must
  not be one.
- **A skill can register hooks from its own frontmatter**, in the same
  configuration format settings files use. This is what removed the reason to
  be a plugin at all (D-020). Claude Code registers them when the skill is
  invoked and keeps them for the rest of the session; `once: true` drops a
  hook after its first successful run.

### Target repository layout

```
tasty-response/
  skills/tasty-response/     # ← copied verbatim to .claude/skills/tasty-response/
    SKILL.md                 # the response-mode contract, and the hook declaration
    build.py                 # assembles templates/base.html from the parts below
    check-contrast.py        # WCAG gate every theme must pass
    styles/core.css          # structure; zero color literals
    themes/*.css             # four palettes, tokens only
    fonts/tr-body.css tr-display-nunito.css tr-display-fraunces.css
    fonts/licenses/*.txt
    templates/base.html      # GENERATED — never hand-patch
    templates/_head.html templates/_tail.html
    scripts/open-artifact.sh scripts/open-artifact.ps1   # M2
  schemas/config.schema.json
  docs/
  examples/
  tests/
```

The repository path mirrors the install path on purpose: `skills/` here
becomes `.claude/skills/` there, with nothing renamed in between.

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
the skill activates on a substantive answer
      |  Claude Code registers the hooks in its frontmatter, for the session
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

**The hook is declared in `SKILL.md` frontmatter, not in a settings file.**
That is what lets TR be a skill and still open the browser by itself:

```yaml
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "./scripts/open-artifact.sh"
```

Two consequences to verify on a real machine before M2 counts as done, rather
than to assume from the documentation (the lesson of D-014):

| Question | Why it matters |
| --- | --- |
| Does a hook registered on skill invocation fire for a `Write` in that *same* turn? | If not, the first artifact of every session opens late or not at all, and the skill must keep its own opener as the first-turn path |
| What is `./scripts/...` relative to? | The command needs an anchor. If it is not the skill directory, the path has to be derived some other way |

### Why `PostToolUse` on `Write`, not `Stop`

`PostToolUse` fires immediately after the file exists, so the browser opens
while Claude is still writing the terminal summary — the page is ready by the
time the reader looks up. A `Stop` hook would work too but adds latency and
requires re-deriving which file was just written from the transcript. `Stop`
is kept as a fallback only if `PostToolUse` matching proves unreliable.

**Persistence works differently now that TR is a skill.** The original design
leaned on a `UserPromptSubmit` hook injecting a reminder every turn. A skill
cannot do that before it has been invoked once — its hooks register on
invocation — so the first activation of a session comes from the skill's own
`description`, which is what the always-on framing actually rests on. A
`UserPromptSubmit` reminder can still be declared for the turns *after* the
first, and whether it is needed is an M4 measurement, not an assumption.

## 3. Artifact location and naming

| Scope | Directory |
| --- | --- |
| project | `.tasty-response/` at the repo root |
| user | `~/.tasty-response/` |

Filename: `<YYYY-MM-DD>-<HHMM>-<slug>.html`, where `slug` is a kebab-case
reduction of the answer's topic, capped at 40 characters. Sorting by name
sorts by time, which is the property that matters when the directory grows.

Artifacts are disposable output, not source, so `.tasty-response/` belongs in
the repository's `.gitignore`. With no installer to write that entry, the
skill does it: before the first write into a project-scope directory, it
checks `.gitignore` and appends the line if it is missing.

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

A JSON file per scope, edited by hand — there is no `tr config` (D-020) —
and validated by `schemas/config.schema.json`. Everything in it is optional:
the defaults are the product, and natural-language opt-out (SKILL.md §1)
covers the common case without touching a file.

| Key | Type | Default | Effect |
| --- | --- | --- | --- |
| `enabled` | bool | `true` | Master switch for the response mode |
| `auto_open` | bool | `true` | Whether the hook opens the browser |
| `theme` | enum | `"charred-citrus"` | `charred-citrus` \| `cellar-gold` \| `patisserie` \| `matcha-ceramic` (D-012) |
| `activation` | enum | `"substantive"` | `substantive` \| `always` \| `on-request` |
| `keep_terminal_text` | enum | `"summary"` | `summary` \| `full` \| `path-only` |
| `artifact_dir` | string | scope default | Override the output directory |
| `retention_days` | int | `30` | Artifacts older than this are candidates for pruning |

Project config overrides user config key by key. A project that sets nothing
inherits everything.

## 7. Distribution and installation

**There is no TR installer.** Installing a skill is placing a directory, and
the community already has a tool for it (D-020):

```bash
npx skills add viniciussena/tasty-response -a claude-code      # this project
npx skills add viniciussena/tasty-response -g -a claude-code   # every project
```

`npx skills` finds `skills/tasty-response/` by its flat-layout search and
copies it to `.claude/skills/` or `~/.claude/skills/`. Without Node, a manual
copy of the same directory is an equally complete install. Either way, **no
`settings.json` is edited** — the hook travels inside `SKILL.md`. That removes
the failure the original design worried about most: a half-written hook entry
in a settings file breaking every session.

The two scopes of D-005 survive unchanged; they are just no longer TR's code.

What the planned `tr doctor` would have checked is still worth knowing, and
belongs in the README as a manual checklist: the skill directory is where the
scope says, `SKILL.md` parses, the opener command exists on this OS, and the
artifact directory is writable and gitignored.

## 8. Non-goals for v0.1

Claude Code only. `npx skills` can install into other agents, but the opener,
the hook, and the activation heuristic are verified against Claude Code
alone. One theme. No PDF or
audio export. No auto-detection matrix in the installer. No `--scope global`
until Claude Code exposes a machine-wide policy layer; `user` is effectively
global per account.

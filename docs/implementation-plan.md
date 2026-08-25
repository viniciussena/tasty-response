# Implementation plan

Internal roadmap from specification to a validated v0.1. **No code has been
written.** Each milestone has an exit criterion that must be demonstrated
before the next begins.

## M0 — Specification (current)

Done: README, architecture, design principles, decisions, this plan.

**Exit:** the layout in architecture §1 is agreed, and D-002 (Claude writes,
hook opens) is accepted as the mechanism.

## M1 — SKILL.md v0, validated by hand

The highest-risk deliverable, so it goes first and it is validated before any
plumbing exists.

1. Write `SKILL.md`: activation heuristic, content contract, visual system,
   HTML contract.
2. Write `styles/core.css`, the four `themes/*.css`, the embedded display
   face, and assemble `templates/base.html` with `build.py`. Every theme must
   pass `check-contrast.py` before it counts as shipped.
3. **Validate by hand:** take 2-3 real dense past answers (an ECRI
   walkthrough, a dbt explanation) and have Claude regenerate them under the
   skill. Open the results side by side with the originals.

**Exit:** the artifact reads *better* than the terminal original — not merely
prettier. Judged on: can you find a specific fact faster, and does the
headline-only scan still deliver the answer? If the output is a styled wall
of the same prose, the content contract is not biting and M1 repeats.

This is the go/no-go for the whole project. Everything after M1 is plumbing
around a validated core; if M1 fails, no amount of installer polish saves it.

## M2 — Hook prototype, cross-platform

1. `hooks.json` with `PostToolUse` on `Write` and `UserPromptSubmit` for the
   persistence reminder.
2. `open-artifact` script: path validation against the configured artifact
   directory, per-OS dispatch, unconditional exit 0.
3. Test the matrix: Windows (primary dev machine), macOS, Linux GUI, WSL,
   and headless SSH.

**Exit:** every failure row in architecture §5 demonstrably degrades to
"path printed, response unaffected". Specifically: a broken opener must not
be able to fail a Claude Code turn.

## M3 — Installer CLI

`tr setup --scope {project,user}`, `uninstall`, `config`, `doctor`.
Atomic writes, install receipt, idempotent re-run, `.gitignore` entry for the
artifact directory, `schemas/config.schema.json`.

**Exit:** install → verify with `doctor` → uninstall leaves the filesystem
and settings byte-identical to before install.

## M4 — Dogfood, then package

Run TR on real work for a stretch of ordinary sessions, tracking two numbers:
how often an artifact was generated when it should not have been, and how
often it was skipped when it should have fired. Tune the heuristic against
that, not against intuition. Then write `.claude-plugin/plugin.json` and the
install documentation.

**Exit:** the mode is not annoying enough to disable during a normal week.

## Risks

| Risk | Signal | Response |
| --- | --- | --- |
| Styled wall of text | M1 output is prettier but no faster to read | Sharpen the content contract; the visual system is not the lever |
| Artifact fatigue | Tabs accumulate unread | Tighten the heuristic toward skipping (D-006); revisit `retention_days` |
| Instruction drift over long sessions | Later turns quietly stop generating | This is exactly what the `UserPromptSubmit` reminder exists for; measure it in M4 |
| Hook breaks a session | Any turn fails because of TR | Treated as a release blocker, not a bug — M2's exit criterion |
| Path injection via model-chosen path | Hook opens something outside the artifact dir | Prefix + extension validation in the script, tested in M2 |
| Windows/WSL path translation | File opens in the wrong context or not at all | Explicit WSL branch, tested in M2's matrix |

## Explicitly out of scope for v0.1

Other harnesses (Codex, Gemini, OMP, Grok, Kimi), a theme marketplace, PDF or
audio export, auto-detection in the installer, and `--scope global`.

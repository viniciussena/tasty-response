# Implementation plan

Internal roadmap from specification to a validated v0.1. Each milestone has
an exit criterion that must be demonstrated before the next begins.

TR is a single skill distributed through GitHub (D-020), so there is no
installer milestone and no packaging step: the repository *is* the release.

## M0 — Specification (done)

Done: README, architecture, design principles, decisions, this plan.

**Exit:** the layout in architecture §1 is agreed, and D-002 (Claude writes,
hook opens) is accepted as the mechanism.

## M1 — SKILL.md v0, validated by hand (current)

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
around a validated core; if M1 fails, no amount of plumbing saves it.

## M2 — Hook in the skill's frontmatter, cross-platform

1. Declare `PostToolUse` on `Write` in `SKILL.md` frontmatter, pointing at
   `scripts/open-artifact.*` inside the skill directory.
2. **Settle the two open questions in architecture §2 on a real machine**:
   whether a hook registered on invocation fires for a `Write` in that same
   turn, and what `./scripts/...` resolves against. The answers decide
   whether the skill keeps its own opener as a first-turn fallback.
3. `open-artifact` script: path validation against the artifact directory,
   per-OS dispatch, unconditional exit 0.
4. Test the matrix: Windows (primary dev machine), macOS, Linux GUI, WSL,
   and headless SSH.
5. Remove the "Opening it" shell step from SKILL.md, or reduce it to the
   first-turn fallback — never both running, since two openers on one
   `Write` are a duplicate tab (D-016).

**Exit:** every failure row in architecture §5 demonstrably degrades to
"path printed, response unaffected". Specifically: a broken opener must not
be able to fail a Claude Code turn.

## M3 — Ready to download

1. `npx skills add viniciussena/tasty-response -a claude-code` installs a
   working skill on a clean machine, in both scopes. Verified by doing it,
   not by reading the `npx skills` docs.
2. The manual `cp -r` path in the README works the same way.
3. A `LICENSE` at the repository root. The fonts are already OFL and carry
   their own texts; the rest needs one too, or the repository is visible but
   not legally reusable.
4. The README's four-step check (Checking an install) resolves every failure
   met during 1 and 2.

**Exit:** someone who has never seen the repository gets their first
artifact from the README alone.

## M4 — Dogfood

Run TR on real work for a stretch of ordinary sessions, tracking two numbers:
how often an artifact was generated when it should not have been, and how
often it was skipped when it should have fired. Tune the heuristic against
that, not against intuition. Also measure whether later turns in a long
session quietly stop generating; that decides whether a `UserPromptSubmit`
reminder is worth adding (architecture §2).

**Exit:** the mode is not annoying enough to disable during a normal week.

## Risks

| Risk | Signal | Response |
| --- | --- | --- |
| Styled wall of text | M1 output is prettier but no faster to read | Sharpen the content contract; the visual system is not the lever |
| Artifact fatigue | Tabs accumulate unread | Tighten the heuristic toward skipping (D-006); revisit `retention_days` |
| Instruction drift over long sessions | Later turns quietly stop generating | Measure in M4; if real, declare a `UserPromptSubmit` reminder in the frontmatter |
| Hook breaks a session | Any turn fails because of TR | Treated as a release blocker, not a bug — M2's exit criterion |
| Skill hook registers too late | The first artifact of a session never opens | The open question in M2 step 2; keep the in-skill opener as a first-turn fallback |
| Path injection via model-chosen path | Hook opens something outside the artifact dir | Prefix + extension validation in the script, tested in M2 |
| Windows/WSL path translation | File opens in the wrong context or not at all | Explicit WSL branch, tested in M2's matrix |

## Explicitly out of scope for v0.1

Other harnesses (Codex, Gemini, OMP, Grok, Kimi) — `npx skills` can install
there, but nothing is verified there — a theme marketplace, PDF or audio
export, a TR-specific installer, and a Claude Code plugin package (D-020).

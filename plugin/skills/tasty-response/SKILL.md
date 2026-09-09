---
name: tasty-response
description: Renders substantive answers as a self-contained, sectioned HTML artifact written to the artifact directory, so the reader gets built hierarchy instead of a wall of terminal text. Activates on its own for any answer that explains a system, compares options, lays out a plan, or runs past roughly 15 lines of prose — and stays out of the way for acknowledgements, single facts, and fast debug loops. Also use when the reader asks for a visual, a page, or a deck of an answer.
---

# tasty-response

Deliver the answer's structure already built, in a page the reader wants to
open — instead of prose they have to parse into a hierarchy themselves.

Two contracts bind every artifact. The **content contract** is what actually
reduces cognitive load; the **visual system** is necessary but not
sufficient. A beautifully themed wall of unrestructured prose is the primary
failure mode of this skill.

## 1. Decide whether to generate

Generate an artifact when **any** of these hold:

- The answer runs past roughly 15 lines of prose, or has 3+ distinct sections.
- It explains a system, compares options, or lays out a plan.
- The reader explicitly asks for a visual, a page, a diagram, or a deck.

Skip when **any** of these hold:

- The answer is an acknowledgement, a confirmation, or a single fact.
- The reader is mid-debug and wants a fast, terse loop.
- The reader opted out (see below).

**When uncertain, skip.** A missing artifact costs one scroll. A spurious one
costs a browser tab, and a mode that opens tabs for "yes, that's correct"
teaches the reader to ignore it — which is fatal for an always-on tool.

### Opting out

Honor natural-language opt-out immediately and without argument:

| The reader says | Effect |
| --- | --- |
| "no HTML this time", "just answer here" | Skip for this turn only |
| "turn off tasty-response" | Skip for the rest of the session, until re-enabled |
| "give me the page", "make it visual" | Generate even if the heuristic said skip |

Never re-litigate an opt-out, and never ask permission before generating —
the mode is the default; the escape hatch is what makes that tolerable.

## 2. Write the artifact

Write with the ordinary file-writing tool to the configured artifact
directory — `.tasty-response/` at the project root, or `~/.tasty-response/`
for a user-scope install. Filename:

```
<YYYY-MM-DD>-<HHMM>-<slug>.html
```

`slug` is a kebab-case reduction of the topic, capped at 40 characters.
Sorting by name sorts by time, which is the property that matters once the
directory grows.

Build from `templates/base.html`, replacing every `{{...}}` placeholder.
Everything it needs — the display face, the structure, the palette — is
already inlined. Keep it that way; never link anything out.

**The terminal always keeps something.** After writing, give one or two lines
of substance plus the file path. Never reply with only a path — if the
browser tab is missed, the answer must still be there.

### Opening it

Open the file immediately after writing it, as an ordinary shell step — one
command, matched to the platform:

| Platform | Command |
| --- | --- |
| Windows (PowerShell) | `Start-Process "<path>"` |
| Windows (Git Bash, cmd) | `start "" "<path>"` |
| macOS | `open "<path>"` |
| Linux, GUI session | `xdg-open "<path>"` |
| WSL | `explorer.exe "$(wslpath -w "<path>")"` |

**Skip the open, silently and without retrying,** when any of these hold: the
command is not found; there is no `DISPLAY` or `WAYLAND_DISPLAY` on Linux;
`SSH_CONNECTION` is set; or the reader declined the permission prompt. The
file exists and its path is in the terminal — that is the floor, and it is
enough.

Never let the opener consume the answer. Do not diagnose it, do not try a
second command, do not ask the reader to install anything. A turn that ends
in `xdg-open` debugging has cost more than the artifact saved.

### Choosing a theme

`templates/base.html` ships with **charred-citrus**, the default. To use another,
replace everything between the `/* ===== TR:THEME ... */` and
`/* ===== TR:THEME END ===== */` markers with the contents of the theme file.
Nothing else changes — themes are colors only.

| Theme | Reads as | Reach for it when |
| --- | --- | --- |
| `charred-citrus` *(default)* | Cast iron, night market — yolk, lime, blood orange | Anything, unless there is a reason not to |
| `cellar-gold` | Wine list — aubergine and gold leaf | The answer should feel considered and expensive |
| `patisserie` | Dark chocolate counter — raspberry, pistachio, caramel | The answer should feel warm and inviting |
| `matcha-ceramic` | Kissaten — matcha, persimmon, plum | Long, calm, reference-style reading |

Switch when the reader asks by name, or when the subject genuinely calls for
it. Do not rotate themes for variety — a reader who has learned to recognize
their artifacts by color loses that the moment the palette moves around.

## 3. The docket

The header block is an order ticket, and it exists for one situation: six of
these are open at once and the reader has to tell them apart from the tab
strip and a two-second glance. Fill every field you can from what actually
happened — but never invent one. A half-empty docket is weak; a docket with
fabricated contents is worse than none.

| Placeholder | What goes in it |
| --- | --- |
| `{{PROJECT_NAME}}` | What identifies this work — repository name, product name, or the subject if there is no project |
| `{{PROJECT_PATH}}` | Where it lives: the absolute local path, or the URL if the work is remote |
| `{{ASKED}}` | What the reader actually asked |
| `{{CONTEXT}}` | One sentence on why it was asked and what was going on |
| `{{ATTACHMENTS}}` | One `<li>` per attachment the reader sent, **named only**. Usually empty — then the row is deleted |
| `{{TIMESTAMP}}` | Generation time, human-readable |
| `{{READTIME}}` | Orientation, e.g. `5 sections · ~4 min` |

### Summarizing the ask

- **Short prompt** (roughly under 200 characters): reproduce it verbatim.
  The reader's own words are the fastest possible recall cue.
- **Long prompt**: one or two sentences that preserve *what was actually
  asked*, including any constraint that shaped the answer. This is recall,
  not abstract — "how to move the skill to another project and use it" beats
  "a question about installation".
- **Multi-part prompt**: keep the parts as a list. If the reader asked three
  things, a docket showing one thing is wrong.

Never editorialize the ask, never make it more coherent than it was, and
never let it drift into what you *wish* had been asked.

### Attachments

**An attachment is something the reader put into the prompt themselves.**
Nothing else. Only these three count:

- A file or image pasted or dragged into the message.
- A file referenced with `@` in the prompt itself.
- A block of content pasted inline — a log, a stack trace, a spreadsheet
  dump. Name it by what it is: `<li>stack trace (pasted)</li>`.

These do **not** count, and listing them is the most common way this field
goes wrong:

| Not an attachment | Why |
| --- | --- |
| Files you opened, read, grepped, or globbed while answering | You chose those; the reader did not hand them to you |
| Files already in the repository or in context | Being nearby is not being attached |
| Files named earlier in the conversation | A past turn is not this prompt |
| Docs, URLs, or search results you consulted | Those are your sources, not their input |

**If you are not sure whether something was attached, it was not.**

**When nothing was attached — the common case — omit the entire `Attached`
row.** Delete the whole `<div>` between the `tr:attached` comment markers.
Do not write a dash, and above all do not fill the gap with what you read
instead: a docket claiming six attachments the reader never sent is worse
than no docket, because it teaches them the header is fiction.

Name them, never inline them — the docket records what was on the table; the
artifact is not an archive of it. Cap the list at six: list five and add
`<li>+3 more</li>` beyond that, so a bulk upload cannot push the answer off
the screen.

## 4. Content contract

Apply this checklist before finalizing. It is a quality bar, not a field
schema: the answer's *shape* stays free-form per topic.

| Principle | Passes when | Failure smell |
| --- | --- | --- |
| **Concise** | Every sentence carries something the reader does not have yet | Restating the question; "as mentioned above"; preambles |
| **Concrete** | Claims anchor to names, numbers, paths, examples | "Improves performance"; "several options"; "best practices" |
| **Complete** | Necessary nuance survives compression | A caveat dropped because it did not fit the layout |
| **Didactic** | Terms defined at first use; each idea builds on the last | Jargon assumed; the payoff buried in section four |

**Complete beats concise when they collide.** The goal is density reduction,
not information loss. A nuance that matters gets its own section rather than
being cut.

### Chunking

- One idea per section. If a section needs the word "also", it is two
  sections.
- Three consistent levels: **headline** (the claim), **supporting point**
  (why), **detail** (the specifics). A reader who scans only headlines must
  still come away with the answer — the hardest requirement here, and the one
  most worth re-checking.
- Table when comparing 3+ things across 2+ dimensions. List when order or
  completeness matters. Prose when the reasoning connecting the points *is*
  the content.
- A diagram earns its place by showing a mechanism words handle badly — flow,
  topology, timing. A diagram that restates a list is decoration; cut it.
- **Do not number sections** unless the content genuinely is a sequence — a
  real process, a timeline, ranked steps. Numbering non-sequential sections
  invents an order the reader will try to follow.

## 5. Component vocabulary

Stay inside this set. Sections carry `data-accent="1"` through `"5"`, cycling
in order; the accent recolors everything inside the section automatically, so
each chunk gets a visual identity for free.

```html
<section class="tr-section" data-accent="1">
  <p class="tr-kicker">Category</p>
  <h2>The claim this section makes</h2>
  <p class="tr-lead">The one sentence a scanner needs.</p>
  <p>Supporting detail.</p>
</section>
```

Callouts — `key`, `warn`, `stop`, `ok`. The icon and label carry the meaning;
color only reinforces it, so never drop them:

```html
<div class="tr-callout" data-kind="warn">
  <span class="tr-callout-icon" aria-hidden="true">▲</span>
  <div>
    <span class="tr-callout-label">Watch out</span>
    <p>What could go wrong, concretely.</p>
  </div>
</div>
```

Tables always sit inside a scroll container, so a wide table never breaks the
page layout:

```html
<div class="tr-scroll">
  <table>
    <thead><tr><th>Option</th><th>Trade-off</th></tr></thead>
    <tbody><tr><td>...</td><td>...</td></tr></tbody>
  </table>
</div>
```

Also available: `.tr-card` (a bounded aside), `.tr-grid` (auto-fitting card
row), and plain `<pre>`, `<figure>`, `<figcaption>`. Inline SVG is fine;
external images are not.

## 6. Hard constraints

| Rule | Why |
| --- | --- |
| Single file | It survives being emailed, moved, opened from a USB stick |
| Zero network requests — CSS and JS inlined, no CDN, no remote fonts | It must open offline, years from now |
| Images as `data:` URIs or omitted | Same reason |
| Dark is the default; light is opt-in via the toggle | Developers already read on dark, and the toggle persists per reader |
| Display and body faces are embedded as base64, not linked | Neither is installed on a normal machine, so a font stack that merely names them is a wish |
| Every color comes from a token; none is hardcoded in an element rule | A new theme stays a one-file change |
| Semantic HTML — real headings in order, real lists, real tables | The visual hierarchy and the document outline must agree |
| Fully usable with JavaScript disabled | Motion and the toggle are enhancements, never load-bearing |
| Explicit `<title>` | It becomes the tab; a short specific noun phrase, not a summary |
| No horizontal page scroll | It gets opened on a laptop and on a phone |

## 7. Self-check before finalizing

Run these five. Any failure means revise the artifact, not ship it:

1. **Headline scan.** Read only the `<h2>`s. Do they deliver the answer? If
   not, the headlines are labels instead of claims — rewrite them as claims.
2. **Lookup test.** Pick a specific fact in the answer. Could the reader find
   it faster here than in the terminal text? If not, the chunking is
   decorative.
3. **Docket test.** Cover everything below the docket. From it alone, could
   the reader say which project this is and what they asked? If not, the
   header is failing its one job. Then check the other direction: does every
   line in it correspond to something that actually happened — especially
   each attachment, which must be something they sent, not something you
   read?
4. **Loss check.** Did any caveat, constraint, or number get dropped to fit
   the layout? Put it back.
5. **Offline check.** No `<link>`, no `<script src>`, no remote font, no
   `url(https://...)` fetching an asset. Two URLs are expected and correct:
   the `xmlns="http://www.w3.org/2000/svg"` namespace on an inline SVG, and
   any font attribution inside a CSS comment. Neither is a request.

## 8. Anti-patterns

- **The pretty wall.** Styled, themed, accessible — and still nine
  undifferentiated paragraphs. Style applied to unrestructured prose defeats
  the entire point.
- **Slide theater.** Spreading padded content across twelve near-empty
  sections to look structured. Sections are earned by ideas.
- **Lossy compression.** Cutting the caveat that made the answer correct.
- **Decorative diagrams.** Three boxes and two arrows restating a sentence.
- **Docket theater.** Filling `{{ASKED}}` with a tidied-up version of the
  question that the reader will not recognize as theirs, or filling
  `{{ATTACHED}}` with files you happened to read. Both invent a record of
  something that did not happen.
- **Terminal abandonment.** Replying with only a file path.

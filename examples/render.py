#!/usr/bin/env python3
"""Render one real answer into every theme, so the palettes can be compared.

The content is identical across all four files — the only variable is the
theme. That is the point: put them side by side and what differs is the
palette, not the writing.

These go through the real pipeline (build.py's renderer, the real template,
the real theme files), so they double as an end-to-end check that the
theme-swap mechanism works.

    python render.py

Writes examples/<theme>.html for every theme in the skill.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(
    os.path.dirname(HERE), "plugins", "tasty-response", "skills", "tasty-response"
)
sys.path.insert(0, SKILL)

import build  # noqa: E402  (path has to be set first)

FIELDS = {
    "TITLE": "Embedded Display Face",
    "PROJECT_NAME": "tasty-response",
    "PROJECT_PATH": "C:\\tasty-response",
    "ASKED": "Não gostei das cores, consegue pensar em outras paletas? "
             "O que em termos de design passaria a ideia de tasty "
             "(fontes, cores, etc.)?",
    "CONTEXT": "M1 design review — the first palette was rejected and the "
               "typography had never been questioned.",
    # Nothing was attached to that prompt, so the row is dropped entirely.
    # Files consulted while answering are NOT attachments — see SKILL.md.
    "ATTACHMENTS": "",
    "TIMESTAMP": "25 Aug 2026, 16:40",
    "READTIME": "5 sections · ~4 min",
    "EYEBROW": "Design decision",
    "HEADLINE": "The palette was the wrong place to look first",
    "STANDFIRST": "Four themes now ship instead of one, but the change that "
                  "actually moved the needle was checking which fonts were "
                  "installed on a real machine — and finding out none of them "
                  "were.",
    "META": "tasty-response · example artifact",
}

SECTIONS = """
  <section class="tr-section" data-accent="1">
    <p class="tr-kicker">The brief</p>
    <h2>Appetite responds to warm, saturated color — and to almost nothing blue</h2>
    <p class="tr-lead">Before choosing hues, it helps to name what the brief
    actually is, because every theme has to satisfy the same one.</p>
    <p>Practically no food is naturally blue, and food branding avoids it with
    something close to fear. Green reads as <em>fresh</em> rather than as the
    main course. Brown carries roasted, caramelized, umami. That narrows the
    field before a single swatch is picked.</p>
    <p>The dark ground is not a developer affectation either — it is the
    plate. Food photography lives on slate and cast iron because a dark
    surface makes bright color leap. The one requirement is that the dark has
    temperature; neutral black kills the effect.</p>
    <div class="tr-callout" data-kind="key">
      <span class="tr-callout-icon" aria-hidden="true">◆</span>
      <div>
        <span class="tr-callout-label">The hard line</span>
        <p>Nothing literal. No checked tablecloths, no chef hats, no food
        emoji. Literalism costs the reader's trust in the content, and the
        content here is technical.</p>
      </div>
    </div>
  </section>

  <section class="tr-section" data-accent="2">
    <p class="tr-kicker">What ships</p>
    <h2>Four directions, not four hue shifts of the same idea</h2>
    <p>Each theme occupies a different pole, so choosing one is a real
    decision rather than a preference between neighbours.</p>
    <div class="tr-scroll">
      <table>
        <thead>
          <tr><th>Theme</th><th>Ground</th><th>Accents</th><th>Pole</th></tr>
        </thead>
        <tbody>
          <tr><td><code>charred-citrus</code> <strong>(default)</strong></td><td>Charcoal, green undertone</td>
              <td>Yolk, lime, blood orange, chili, smoke</td><td>Bold, high energy</td></tr>
          <tr><td><code>patisserie</code></td><td>Cocoa-plum</td>
              <td>Raspberry, pistachio, caramel, blueberry, vanilla</td><td>Sweet, high delight</td></tr>
          <tr><td><code>cellar-gold</code></td><td>Aubergine</td>
              <td>Gold leaf, burgundy, fig, sage, copper</td><td>Elegant, considered</td></tr>
          <tr><td><code>matcha-ceramic</code></td><td>Warm sumi ink</td>
              <td>Matcha, persimmon, plum, kinako, indigo</td><td>Calm, crafted</td></tr>
        </tbody>
      </table>
    </div>
    <p>This forced a split worth doing on its own: <code>styles/core.css</code>
    holds structure and contains zero color literals, and each theme holds
    nothing but tokens. A theme is now genuinely one file.</p>
  </section>

  <section class="tr-section" data-accent="3">
    <p class="tr-kicker">Typography</p>
    <h2>The accessibility claim was decorative until the font was embedded</h2>
    <p>The body stack named <code>Atkinson Hyperlegible</code> first, "for the
    dyslexia goal". Checked against the development machine: not installed.
    Neither was the second choice. The stack fell straight through to the
    system sans while the design documents claimed an accessibility
    property.</p>
    <p>"No remote fonts" had been read as "system fonts only". But a font
    embedded as a <code>data:</code> URI is not a remote font — it makes zero
    network requests and survives offline exactly as well as the rest of the
    page. Subsetting makes it cheap:</p>
    <pre>Nunito 800          16.5KB  ->  12.5KB subset
Baloo 2 700         19.4KB  ->  16.0KB subset
Fraunces SuperSoft  33.0KB  ->  16.6KB  (opsz pinned to 60)</pre>
    <p>Nunito ExtraBold carries the display; Atkinson Hyperlegible carries the
    body at 24KB for both weights. Fraunces was more beautiful and lost
    anyway — headlines are a reading path here, not decoration, and least
    friction is the premise.</p>
    <div class="tr-callout" data-kind="warn">
      <span class="tr-callout-icon" aria-hidden="true">▲</span>
      <div>
        <span class="tr-callout-label">Watch out</span>
        <p>The families are renamed <code>TR Display</code> and
        <code>TR Body</code>. Without that, a reader who happens to have the
        real font installed would silently get their copy instead of the
        embedded one, and the artifact would render differently on their
        machine than on yours.</p>
      </div>
    </div>
  </section>

  <section class="tr-section" data-accent="4">
    <p class="tr-kicker">Verification</p>
    <h2>The contrast audit failed, which is the only reason to trust it</h2>
    <p>Every accent is checked against the page ground <em>and</em> against
    its own tint — the tint is what sits behind kickers, table headers,
    callout labels, and the docket, and it is where contrast quietly
    breaks.</p>
    <pre>ok    cellar-gold.css        ok    charred-citrus.css
ok    matcha-ceramic.css     ok    patisserie.css
4 themes checked, 0 failures</pre>
    <p>It did not pass on the first run. Two patisserie light accents came in
    at 4.42 and 4.44 against the 4.5 minimum — invisible by eye, caught by
    arithmetic. Both were darkened until they passed.</p>
    <div class="tr-callout" data-kind="ok">
      <span class="tr-callout-icon" aria-hidden="true">●</span>
      <div>
        <span class="tr-callout-label">Now a rule</span>
        <p>A theme that does not pass <code>check-contrast.py</code> is not a
        theme.</p>
      </div>
    </div>
  </section>

  <section class="tr-section" data-accent="5">
    <p class="tr-kicker">Still open</p>
    <h2>Everything here was verified by script, and none of it by eye</h2>
    <p>What the tooling can honestly claim, and what it cannot:</p>
    <ul>
      <li><strong>Verified:</strong> zero network requests, WCAG AA in eight
      palettes, the template matching its sources.</li>
      <li><strong>Not verified:</strong> whether the grain reads as warmth or
      as noise, and whether the docket earns the space it takes.</li>
    </ul>
    <div class="tr-callout" data-kind="stop">
      <span class="tr-callout-icon" aria-hidden="true">■</span>
      <div>
        <span class="tr-callout-label">The gate</span>
        <p>M1 does not pass because the artifact is prettier. It passes when a
        specific fact is faster to find here than in the terminal text, and
        when reading only the headlines still delivers the answer. That is a
        judgement only a person can make.</p>
      </div>
    </div>
  </section>
"""


def swatches(theme):
    """Pull each palette's tokens straight out of the theme file.

    Parsed rather than restated, so the contact sheet can never drift from
    the themes it is showing.
    """
    import re
    css = open(os.path.join(SKILL, "themes", f"{theme}.css"), encoding="utf-8").read()
    modes = {}
    for block in re.finditer(r"(:root[^{]*)\{([^}]*)\}", css):
        selector, body = block.group(1).strip(), block.group(2)
        tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9A-Fa-f]{6})\s*;", body))
        names = dict(re.findall(r"--a(\d)-fg:\s*#[0-9A-Fa-f]{6};\s*--a\d-tint:\s*#[0-9A-Fa-f]{6};\s*/\*\s*([\w-]+)", body))
        modes["light" if "light" in selector else "dark"] = (tokens, names)
    return modes


def build_index(theme_list):
    rows = []
    for theme in theme_list:
        modes = swatches(theme)
        default = " &middot; default" if theme == build.DEFAULT_THEME else ""
        cards = []
        for mode in ("dark", "light"):
            tokens, names = modes[mode]
            chips = "".join(
                f'<li style="--c:{tokens[f"--a{i}-fg"]};--t:{tokens[f"--a{i}-tint"]}">'
                f'<span class="chip"></span>{names.get(str(i), "a" + str(i))}'
                f'<code>{tokens[f"--a{i}-fg"]}</code></li>'
                for i in range(1, 6)
            )
            cards.append(
                f'<div class="mode" style="--bg:{tokens["--bg"]};--fg:{tokens["--fg"]};'
                f'--muted:{tokens["--fg-muted"]};--line:{tokens["--border-strong"]}">'
                f'<p class="mode-name">{mode}</p><ul class="chips">{chips}</ul></div>'
            )
        rows.append(
            f'<section class="theme"><h2><a href="{theme}.html">{theme}</a>'
            f'<span class="tag">{default}</span></h2>'
            f'<div class="modes">{"".join(cards)}</div></section>'
        )

    html = INDEX_SHELL.replace("{{ROWS}}", "\n".join(rows))
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print(f"wrote examples/index.html  ({len(html) / 1024:.0f}KB)")


INDEX_SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark light">
<title>tasty-response themes</title>
<style>
  :root { --page: #16141A; --ink: #EFEAE4; --dim: #9A9199; --edge: #2E2A34; }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--page); color: var(--ink);
    font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    padding: 3rem 1.5rem 5rem; }
  .wrap { max-width: 60rem; margin: 0 auto; }
  h1 { font-size: 1.75rem; letter-spacing: -.02em; margin: 0 0 .5rem; }
  .sub { color: var(--dim); margin: 0 0 3rem; max-width: 46ch; }
  .theme { margin-bottom: 3rem; }
  .theme h2 { font-size: 1.125rem; margin: 0 0 .75rem; font-weight: 600; }
  .theme h2 a { color: var(--ink); text-underline-offset: 4px; }
  .tag { color: var(--dim); font-weight: 400; font-size: .875rem; }
  .modes { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr)); }
  .mode { background: var(--bg); color: var(--fg); border: 1px solid var(--line);
    border-radius: 12px; padding: 1rem 1.25rem; }
  .mode-name { font-size: .75rem; letter-spacing: .12em; text-transform: uppercase;
    color: var(--muted); margin: 0 0 .75rem; }
  .chips { list-style: none; margin: 0; padding: 0; display: grid; gap: .5rem; }
  .chips li { display: grid; grid-template-columns: 1.25rem 1fr auto;
    align-items: center; gap: .625rem; font-size: .875rem; }
  .chip { width: 1.25rem; height: 1.25rem; border-radius: 50%;
    background: var(--c); box-shadow: 0 0 0 4px var(--t); }
  .chips code { font-size: .75rem; color: var(--muted);
    font-family: ui-monospace, Consolas, monospace; }
  footer { color: var(--dim); font-size: .875rem; margin-top: 3rem;
    border-top: 1px solid var(--edge); padding-top: 1.5rem; }
</style>
</head>
<body>
<div class="wrap">
  <h1>tasty-response &mdash; themes</h1>
  <p class="sub">The same answer rendered four times. Only the palette differs.
  Click a name to open that artifact; each shows all five accent groups, one
  per section.</p>
  {{ROWS}}
  <section class="theme"><h2>Display face &mdash; same theme, same words</h2>
  <p class="sub" style="margin:0">
    <a href="display-fraunces.html">fraunces</a> (soft serif, current default)
    vs <a href="display-nunito.html">nunito</a> (rounded sans).
    Body text is Atkinson Hyperlegible in both.</p></section>

  <footer>Generated by examples/render.py from the theme files &mdash; the
  swatches are parsed, not restated, so they cannot drift.</footer>
</div>
</body>
</html>
"""


def main():
    fields = dict(FIELDS, SECTIONS=SECTIONS)
    for theme in build.themes():
        html = build.render(theme)
        if not fields["ATTACHMENTS"].strip():
            html = re.sub(r"[^\S\n]*<!-- tr:attached.*?/tr:attached -->\n",
                          "", html, flags=re.S)
        for key, value in fields.items():
            html = html.replace("{{%s}}" % key, value)

        leftover = [k for k in fields if "{{%s}}" % k in html]
        assert not leftover, f"unreplaced placeholders: {leftover}"

        out = os.path.join(HERE, f"{theme}.html")
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        marker = "  (default)" if theme == build.DEFAULT_THEME else ""
        print(f"wrote examples/{theme}.html  ({len(html) / 1024:.0f}KB){marker}")

    # A/B for the display face: same theme, same content, different face.
    for display in build.displays():
        html = build.render(build.DEFAULT_THEME, display)
        html = re.sub(r"[^\S\n]*<!-- tr:attached.*?/tr:attached -->\n",
                      "", html, flags=re.S)
        for key, value in fields.items():
            html = html.replace("{{%s}}" % key, value)
        out = os.path.join(HERE, f"display-{display}.html")
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        print(f"wrote examples/display-{display}.html  ({len(html) / 1024:.0f}KB, {display})")

    build_index(build.themes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Render the README demo: one invented answer, in the default theme.

The question and the answer are fictional — they exist so the README can
show what an artifact looks like before anyone installs anything. They go
through the real pipeline (build.py's renderer, the real template, the
default theme), so the picture is of the actual output, not a mockup.

    python demo.py

Writes examples/demo.html, and examples/demo.png when Edge or Chrome is
installed (headless screenshot). Without a browser, only the HTML is written.
"""

import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(os.path.dirname(HERE), "skills", "tasty-response")
sys.path.insert(0, SKILL)

import build  # noqa: E402  (path has to be set first)

FIELDS = {
    "TITLE": "Index Skipped by date_trunc",
    "PROJECT_NAME": "shop-api",
    "PROJECT_PATH": "~/code/shop-api",
    "ASKED": "I added an index on orders(created_at) but this query still "
             "takes 4 seconds. Why isn't Postgres using it?",
    "CONTEXT": "The daily orders report started timing out after the table "
               "passed 12 million rows.",
    "ATTACHMENTS": "<li>EXPLAIN ANALYZE output (pasted)</li>",
    "TIMESTAMP": "25 Sep 2026, 10:12",
    "READTIME": "4 sections · ~3 min",
    "EYEBROW": "Diagnosis",
    "HEADLINE": "The index is fine — the query hides the column from it",
    "STANDFIRST": "Wrapping created_at in date_trunc() means Postgres would "
                  "have to compute the function for every row before it could "
                  "compare, so it reads all 12 million. Rewrite the filter as "
                  "a range and the same index answers it in milliseconds.",
    "META": "tasty-response · demo artifact (fictional answer)",
}

SECTIONS = """
  <section class="tr-section" data-accent="1">
    <p class="tr-kicker">The cause</p>
    <h2>A function around the column turns an index lookup into a full scan</h2>
    <p class="tr-lead">An index stores the raw values of <code>created_at</code>,
    sorted. Your filter asks about <code>date_trunc('day', created_at)</code> —
    a value the index has never seen.</p>
    <p>To find rows where the <em>truncated</em> date equals September 1st,
    Postgres has to truncate every row's timestamp first. The sorted order of
    the index cannot help with that, so the planner skips it. Your pasted plan
    says exactly this:</p>
    <pre>Seq Scan on orders  (cost=0.00..412893.20 rows=61204 width=96)
  Filter: (date_trunc('day', created_at) = '2026-09-01')
  Rows Removed by Filter: 12190331
Execution Time: 4127.551 ms</pre>
    <div class="tr-callout" data-kind="key">
      <span class="tr-callout-icon" aria-hidden="true">◆</span>
      <div>
        <span class="tr-callout-label">The rule</span>
        <p>A B-tree index can only be used when the indexed column appears
        <strong>bare</strong> on one side of the comparison. Any function,
        cast, or arithmetic on it hides it.</p>
      </div>
    </div>
  </section>

  <section class="tr-section" data-accent="2">
    <p class="tr-kicker">The fix</p>
    <h2>Ask for a range of raw timestamps instead</h2>
    <p class="tr-lead">"Truncates to September 1st" means the same thing as
    "falls between midnight on the 1st and midnight on the 2nd" — and the
    second form leaves the column bare.</p>
    <pre>-- before: 4.1 s, sequential scan
WHERE date_trunc('day', created_at) = '2026-09-01'

-- after: 3 ms, index scan on orders_created_at_idx
WHERE created_at &gt;= '2026-09-01'
  AND created_at &lt;  '2026-09-02'</pre>
    <p>Use <code>&lt;</code> on the upper bound, not <code>&lt;=</code> or
    <code>BETWEEN</code>: an order at exactly midnight on the 2nd belongs to
    the next day.</p>
  </section>

  <section class="tr-section" data-accent="3">
    <p class="tr-kicker">Same trap, other shapes</p>
    <h2>Three more filters that silently skip an index</h2>
    <p>Worth grepping the codebase for, since the report query is unlikely to
    be the only one.</p>
    <div class="tr-scroll">
      <table>
        <thead>
          <tr><th>Pattern</th><th>Example</th><th>Fix</th></tr>
        </thead>
        <tbody>
          <tr><td>Cast on the column</td><td><code>created_at::date = '2026-09-01'</code></td>
              <td>Same range rewrite as above</td></tr>
          <tr><td>Leading wildcard</td><td><code>email LIKE '%@acme.com'</code></td>
              <td>A trigram index (<code>pg_trgm</code>), or store the domain in its own column</td></tr>
          <tr><td>Case folding</td><td><code>lower(email) = 'ana@acme.com'</code></td>
              <td>An expression index on <code>lower(email)</code></td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="tr-section" data-accent="4">
    <p class="tr-kicker">Next</p>
    <h2>Change one line, then confirm with the plan, not the stopwatch</h2>
    <ol>
      <li>Replace the <code>date_trunc</code> filter in
      <code>reports/daily_orders.sql</code> with the range.</li>
      <li>Run <code>EXPLAIN ANALYZE</code> again and look for <code>Index Scan
      using orders_created_at_idx</code>.</li>
      <li>Leave the existing index as it is — it was never the problem.</li>
    </ol>
    <div class="tr-callout" data-kind="warn">
      <span class="tr-callout-icon" aria-hidden="true">▲</span>
      <div>
        <span class="tr-callout-label">Watch out</span>
        <p>If <code>created_at</code> is <code>timestamptz</code>, the date
        literals are read in the session's time zone. Pin it
        (<code>'2026-09-01 00:00+00'</code>) if the report must be in UTC.</p>
      </div>
    </div>
  </section>
"""

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def find_browser():
    for path in BROWSERS:
        if os.path.exists(path):
            return path
    for name in ("chromium", "chromium-browser", "google-chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    return None


def screenshot(html_path, png_path, width=1100, height=1500):
    browser = find_browser()
    if not browser:
        print("no Edge/Chrome found — skipped demo.png")
        return
    subprocess.run([
        browser, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=2", "--virtual-time-budget=5000", f"--window-size={width},{height}",
        f"--screenshot={png_path}", "file:///" + html_path.replace("\\", "/"),
    ], check=True, capture_output=True, timeout=60)
    print(f"wrote examples/demo.png  ({os.path.getsize(png_path) / 1024:.0f}KB)")


def main():
    html = build.render(build.DEFAULT_THEME)
    if not FIELDS["ATTACHMENTS"].strip():
        html = re.sub(r"[^\S\n]*<!-- tr:attached.*?/tr:attached -->\n",
                      "", html, flags=re.S)
    for key, value in dict(FIELDS, SECTIONS=SECTIONS).items():
        html = html.replace("{{%s}}" % key, value)
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", html)
    assert not leftover, f"unreplaced placeholders: {leftover}"

    out = os.path.join(HERE, "demo.html")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print(f"wrote examples/demo.html  ({len(html) / 1024:.0f}KB)")
    screenshot(out, os.path.join(HERE, "demo.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

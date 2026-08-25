#!/usr/bin/env python3
"""Audit every theme against WCAG AA contrast.

Parses themes/*.css directly, so it checks what actually ships rather than a
copy of the palette kept somewhere else. Any new theme must pass this before
it is offered as an option.

    python check-contrast.py

Exits non-zero on any failure, so it can gate a build.
"""

import glob
import os
import re
import sys

# Pairs that must be legible: (foreground token, background token, minimum).
# 4.5:1 is AA for body text. Accents are checked against both the page ground
# and their own tint, because the tint is what sits behind kickers, table
# headers, callout labels, and the docket project name.
BASE_PAIRS = [
    ("--fg", "--bg", 4.5),
    ("--fg-muted", "--bg", 4.5),
    ("--fg", "--surface", 4.5),
    ("--fg-muted", "--surface", 4.5),
    ("--fg", "--surface-2", 4.5),
    ("--fg-muted", "--bg-elevated", 4.5),
]


def luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def parse_blocks(css):
    """Return {selector: {token: hex}} for each top-level rule with colors."""
    blocks = {}
    for match in re.finditer(r"(:root[^{]*)\{([^}]*)\}", css):
        selector = match.group(1).strip()
        tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9A-Fa-f]{3,6})\s*;", match.group(2)))
        if tokens:
            blocks[selector] = tokens
    return blocks


def audit(path):
    css = open(path, encoding="utf-8").read()
    failures = []
    for selector, tokens in parse_blocks(css).items():
        mode = "light" if "light" in selector else "dark"
        pairs = list(BASE_PAIRS)
        for i in range(1, 6):
            pairs.append((f"--a{i}-fg", "--bg", 4.5))
            pairs.append((f"--a{i}-fg", f"--a{i}-tint", 4.5))
            pairs.append((f"--a{i}-fg", "--surface", 4.5))
        for fg, bg, minimum in pairs:
            if fg not in tokens or bg not in tokens:
                failures.append((mode, f"{fg} or {bg}", 0.0, minimum, "MISSING TOKEN"))
                continue
            r = ratio(tokens[fg], tokens[bg])
            if r < minimum:
                failures.append((mode, f"{fg} on {bg}", r, minimum,
                                 f"{tokens[fg]} on {tokens[bg]}"))
    return failures


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    paths = sorted(glob.glob(os.path.join(here, "themes", "*.css")))
    if not paths:
        print("no themes found", file=sys.stderr)
        return 1

    total = 0
    for path in paths:
        name = os.path.basename(path)
        failures = audit(path)
        total += len(failures)
        if failures:
            print(f"FAIL  {name}")
            for mode, pair, r, minimum, detail in failures:
                print(f"        {mode:5}  {pair:28}  {r:.2f} < {minimum}  ({detail})")
        else:
            print(f"ok    {name}")

    print()
    print(f"{len(paths)} themes checked, {total} failures")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

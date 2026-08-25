#!/usr/bin/env python3
"""Assemble templates/base.html from its parts.

The template is generated, never hand-edited: the font, the core styles, and
the theme each live in exactly one file, and this script is what guarantees
the copy inside base.html cannot drift from them.

    python build.py                      # default theme (patisserie)
    python build.py --theme cellar-gold  # any file in themes/
    python build.py --list               # show available themes
    python build.py --check              # verify base.html is up to date

Run check-contrast.py before shipping a new theme.
"""

import argparse
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_THEME = "patisserie"

PARTS = [
    ("TR:FONT", "fonts/tr-display.css"),
    ("TR:CORE", "styles/core.css"),
]


def read(rel):
    with open(os.path.join(HERE, rel), encoding="utf-8") as fh:
        return fh.read()


def themes():
    return sorted(
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(HERE, "themes", "*.css"))
    )


def render(theme):
    chunks = [read("templates/_head.html")]
    for marker, path in PARTS:
        chunks.append(f"/* ===== {marker} — from {path}, do not edit here ===== */\n")
        chunks.append(read(path))
        chunks.append("\n")
    chunks.append(f"/* ===== TR:THEME {theme} — from themes/{theme}.css ===== */\n")
    chunks.append(read(f"themes/{theme}.css"))
    chunks.append("/* ===== TR:THEME END ===== */\n")
    chunks.append(read("templates/_tail.html"))
    return "".join(chunks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theme", default=DEFAULT_THEME)
    parser.add_argument("--out", default="templates/base.html")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    available = themes()
    if args.list:
        for name in available:
            print(f"{name}{'  (default)' if name == DEFAULT_THEME else ''}")
        return 0

    if args.theme not in available:
        print(f"unknown theme {args.theme!r}; available: {', '.join(available)}", file=sys.stderr)
        return 1

    html = render(args.theme)
    out = os.path.join(HERE, args.out)

    if args.check:
        current = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
        if current == html:
            print(f"ok    {args.out} matches its sources")
            return 0
        print(f"STALE {args.out} differs from its sources — run build.py", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print(f"wrote {args.out}  ({len(html) / 1024:.0f}KB, theme: {args.theme})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

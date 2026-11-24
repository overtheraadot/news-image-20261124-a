#!/usr/bin/env python3
"""Front Page - Tuesday 24 November 2026: 35 stories, 7 regions.

The image is drawn by render.py (kept in this repo) and committed as
entry.png. This program only copies it to /output/entry.png, using the
standard library alone, so it runs with no network and is byte-for-byte
deterministic.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    if os.path.getsize(src) > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB gate")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())

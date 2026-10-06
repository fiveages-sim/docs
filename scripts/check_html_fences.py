#!/usr/bin/env python3
"""Fail if built HTML contains leaked Markdown fences (```).

Broken MyST nesting (especially inside admonitions) leaks fence markers
into ordinary page text. Examples inside <pre>/<code> are allowed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


PRE_RE = re.compile(r"<pre\b[^>]*>.*?</pre>", re.IGNORECASE | re.DOTALL)
CODE_RE = re.compile(r"<code\b[^>]*>.*?</code>", re.IGNORECASE | re.DOTALL)
SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.IGNORECASE | re.DOTALL)


def strip_allowed(html: str) -> str:
    html = SCRIPT_RE.sub("", html)
    html = STYLE_RE.sub("", html)
    html = PRE_RE.sub("", html)
    html = CODE_RE.sub("", html)
    return html


def find_literal_fences(html_root: Path) -> list[str]:
    hits: list[str] = []
    for path in sorted(html_root.rglob("*.html")):
        text = path.read_text(encoding="utf-8", errors="replace")
        cleaned = strip_allowed(text)
        if "```" not in cleaned:
            continue
        rel = path.as_posix()
        for i, line in enumerate(cleaned.splitlines(), 1):
            if "```" in line:
                snippet = re.sub(r"\s+", " ", line).strip()
                if len(snippet) > 160:
                    snippet = snippet[:157] + "..."
                hits.append(f"{rel}:{i}: {snippet}")
    return hits


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    html_root = Path(sys.argv[1]) if len(sys.argv) > 1 else repo / "build" / "html"
    if not html_root.exists():
        print(f"ERROR: HTML build directory not found: {html_root}")
        return 1
    hits = find_literal_fences(html_root)
    if hits:
        print("ERROR: literal ``` found in built HTML (broken Markdown/MyST fences):")
        for hit in hits[:50]:
            print(f"  {hit}")
        if len(hits) > 50:
            print(f"  ... and {len(hits) - 50} more")
        return 1
    print(f"OK: no literal ``` in HTML under {html_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

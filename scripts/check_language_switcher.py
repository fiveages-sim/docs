#!/usr/bin/env python3
"""Guard the UniLab-style sidebar language switcher.

1. Unit-test relative counterpart hrefs (en root ↔ zh_CN/).
2. If a HTML tree is given, require ``.sidebar-lang-switcher`` and reject
   domain-root ``/zh_CN/`` option values (missing GitHub Pages ``/docs``).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from language_switcher import switcher_hrefs  # noqa: E402

OPTION_RE = re.compile(
    r'<option\s+value="([^"]*)"[^>]*>',
    re.IGNORECASE,
)
SWITCHER_RE = re.compile(r'class="sidebar-lang-switcher__select"')
BAD_ROOT = re.compile(r"^/zh_CN(/|$)")


def _assert_hrefs() -> list[str]:
    issues: list[str] = []
    cases = [
        ("index", "en", {"en": "index.html", "zh_CN": "zh_CN/index.html"}),
        (
            "1-getting_started/2-install_environment",
            "en",
            {
                "en": "2-install_environment.html",
                "zh_CN": "../zh_CN/1-getting_started/2-install_environment.html",
            },
        ),
        (
            "1-getting_started/2-install_environment",
            "zh_CN",
            {
                "en": "../../1-getting_started/2-install_environment.html",
                "zh_CN": "2-install_environment.html",
            },
        ),
        ("index", "zh_CN", {"en": "../index.html", "zh_CN": "index.html"}),
    ]
    for pagename, lang, expected in cases:
        got = switcher_hrefs(pagename, lang)
        if got != expected:
            issues.append(f"hrefs({pagename!r}, {lang!r}) = {got} expected {expected}")
        for href in got.values():
            if BAD_ROOT.match(href) or href.startswith("/zh_CN"):
                issues.append(f"domain-root zh path: {href}")
    return issues


def _has_source_page(html_path: Path, html_root: Path) -> bool:
    rel = html_path.relative_to(html_root)
    parts = list(rel.parts)
    if parts and parts[0] == "zh_CN":
        parts = parts[1:]
    if not parts:
        return False
    stem = Path(*parts).with_suffix("")
    if stem.name in {"genindex", "search", "py-modindex"}:
        return False
    src_root = _SCRIPTS.parent / "source"
    return (src_root / f"{stem}.md").is_file() or (src_root / f"{stem}.rst").is_file()


def _check_html(root: Path) -> list[str]:
    issues: list[str] = []
    pages = sorted(root.rglob("*.html"))
    checked = 0
    for path in pages:
        if path.name in {"genindex.html", "search.html"}:
            continue
        if "searchindex" in path.name:
            continue
        if not _has_source_page(path, root):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "sidebar-tree" not in text and "sidebar-scroll" not in text:
            continue
        if not SWITCHER_RE.search(text):
            issues.append(f"{path}: missing sidebar language switcher")
            continue
        checked += 1
        for value in OPTION_RE.findall(text):
            if BAD_ROOT.match(value) or value == "/zh_CN/" or value.startswith("/zh_CN/"):
                issues.append(f"{path}: option value {value!r} is domain-root /zh_CN (missing /docs)")
    if checked == 0:
        issues.append(f"{root}: no HTML pages with a language switcher")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--html-root",
        type=Path,
        default=None,
        help="Built HTML root (e.g. build/html). Optional for href unit tests.",
    )
    args = parser.parse_args()

    issues = _assert_hrefs()
    if args.html_root is not None:
        issues.extend(_check_html(args.html_root))

    if issues:
        print("ERROR: language switcher checks failed:")
        for issue in issues:
            print(f"  {issue}")
        return 1
    print("OK: language switcher hrefs")
    if args.html_root is not None:
        print(f"OK: sidebar switcher present under {args.html_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

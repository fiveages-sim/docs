"""Language-switcher hrefs for sphinx-intl dual builds (en root + zh_CN/).

UniLab's switcher uses Sphinx ``pathto()`` because both language trees live in
one build. This site builds English and Chinese separately, so the other
locale is not in ``found_docs``. Counterpart URLs are therefore **relative**
paths on the combined site:

- English page ``foo/bar.html`` ↔ Chinese ``zh_CN/foo/bar.html``
- Resolved on GitHub Pages as ``/docs/...`` ↔ ``/docs/zh_CN/...``
  (never domain-root ``/zh_CN/``, which 404s on the project site).
"""

from __future__ import annotations

import os
from pathlib import PurePosixPath


def html_name(pagename: str) -> str:
    return f"{pagename}.html"


def rel_href(from_file: str, to_file: str) -> str:
    src_dir = PurePosixPath(from_file).parent
    start = "." if src_dir == PurePosixPath(".") else str(src_dir)
    rel = os.path.relpath(to_file, start=start)
    href = PurePosixPath(rel).as_posix()
    if href in (".", ""):
        return PurePosixPath(to_file).name
    return href


def switcher_hrefs(pagename: str, language: str) -> dict[str, str]:
    page = html_name(pagename)
    en_file = page
    zh_file = f"zh_CN/{page}"
    current = zh_file if language == "zh_CN" else en_file
    return {
        "en": rel_href(current, en_file),
        "zh_CN": rel_href(current, zh_file),
    }

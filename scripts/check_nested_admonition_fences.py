#!/usr/bin/env python3
"""Fail if source Markdown nests ``` fences inside ```{admonition}."""

from __future__ import annotations

import re
import sys
from pathlib import Path


FENCE_RE = re.compile(r"^(\s*)(`{3,})(.*)$")


def find_nested_admonition_fences(root: Path) -> list[str]:
    issues: list[str] = []
    for path in sorted(root.rglob("*.md")):
        if "_vendored" in path.parts:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        stack: list[tuple[str, int, int]] = []
        for n, line in enumerate(lines, 1):
            match = FENCE_RE.match(line.lstrip())
            if not match:
                continue
            fence, info = match.group(2), match.group(3).strip()
            if stack and len(fence) >= stack[-1][2] and info == "":
                stack.pop()
                continue
            kind = "admonition" if info.startswith("{admonition}") else (
                "directive" if info.startswith("{") else "code"
            )
            stack.append((kind, n, len(fence)))
            if kind == "code" and any(k == "admonition" for k, _, _ in stack[:-1]):
                opened = next(start for k, start, _ in reversed(stack[:-1]) if k == "admonition")
                rel = path.as_posix()
                issues.append(
                    f"{rel}:{n}: nested ``` inside ```{{admonition}} opened at line {opened}"
                )
    return issues


def main() -> int:
    root = Path(__file__).resolve().parent.parent / "source"
    issues = find_nested_admonition_fences(root)
    if issues:
        print("ERROR: nested Markdown fences inside MyST admonitions:")
        for issue in issues:
            print(f"  {issue}")
        print("Use colon fences (:::) when an admonition must contain a code block.")
        return 1
    print("OK: no nested ``` inside ```{admonition}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

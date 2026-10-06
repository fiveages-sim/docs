#!/usr/bin/env python3
"""Apply msgid -> msgstr JSON maps onto locale/zh_CN .po files."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def unescape_po(s: str) -> str:
    return (
        s.replace(r"\\", "\x00")
        .replace(r"\"", '"')
        .replace(r"\n", "\n")
        .replace(r"\t", "\t")
        .replace("\x00", "\\")
    )


def escape_po(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


def normalize_json_text(s: str) -> str:
    """Turn PO-style \\n sequences into real newlines when JSON kept them literal."""
    if "\n" not in s:
        s = s.replace("\\n", "\n")
    s = s.replace("\\t", "\t")
    return s


def is_code_like(text: str) -> bool:
    """Code, trees, and commands should keep msgid as msgstr."""
    s = text.strip()
    if not s:
        return True
    if s.startswith(
        ("```", "<input ", "http://", "https://", "<", "<?", "#:", "msgid ", "msgstr ")
    ):
        return True
    first = s.split("\n", 1)[0].lstrip()
    prefixes = (
        "./", "git ", "pip ", "sudo ", "colcon ", "ros2 ", "source ", "export ",
        "cd ", "make ", "cmake ", "python ", "python3 ", "apt ", "dpkg ", "ls ",
        "ln ", "ip ", "vim ", "cp ", "cat ", "echo ", "curl ", "from ", "import ",
        "def ", "class ", "docs/", "FaSim-Isaac/", "open-deploy-ws/",
        "fa-deploy-ws/", "workspace/",
    )
    if first.startswith(prefixes):
        return True
    code_tokens = (
        "├", "└", "│", "flowchart", "subgraph", "ros2 ", "git ", "sudo ",
        "colcon ", "source ", "export ", "./", ":=", "pip ", "apt ",
        "<plugin>", "<hardware>", "<ros2_control", "filename=", "prim_path=",
        "host=", "port=", "usd_path=",
    )
    if "\n" in s and any(tok in s for tok in code_tokens):
        return True
    if "\n" in s and (":\n" in s or s.endswith(":")) and not any(
        "\u4e00" <= ch <= "\u9fff" for ch in s
    ):
        return True
    return False


def wrap_msgstr(text: str) -> list[str]:
    escaped = escape_po(text)
    if "\\n" in escaped:
        lines = ["msgstr \"\""]
        parts = escaped.split("\\n")
        for i, part in enumerate(parts):
            if i < len(parts) - 1:
                lines.append(f"\"{part}\\n\"")
            elif part:
                lines.append(f"\"{part}\"")
        return lines
    if len(escaped) > 80:
        return ["msgstr \"\"", f"\"{escaped}\""]
    return [f"msgstr \"{escaped}\""]


def read_entries(lines: list[str]):
    i = 0
    while i < len(lines):
        if lines[i].startswith("msgid \""):
            start = i
            msgid = unescape_po(lines[i][7:-1] if lines[i].endswith('"') else lines[i][7:])
            i += 1
            while i < len(lines) and lines[i].startswith('"'):
                msgid += unescape_po(lines[i][1:-1] if lines[i].endswith('"') else lines[i][1:])
                i += 1
            if i < len(lines) and lines[i].startswith("msgstr \""):
                msgstr_start = i
                msgstr = unescape_po(lines[i][8:-1] if lines[i].endswith('"') else lines[i][8:])
                i += 1
                while i < len(lines) and lines[i].startswith('"'):
                    msgstr += unescape_po(lines[i][1:-1] if lines[i].endswith('"') else lines[i][1:])
                    i += 1
                yield start, msgstr_start, i, msgid, msgstr
                continue
        i += 1


def apply_map(po_path: Path, mapping: dict[str, str]) -> int:
    raw = po_path.read_text(encoding="utf-8")
    newline = "\n" if raw.endswith("\n") or "\n" in raw else "\n"
    lines = raw.splitlines()
    replacements = []
    changed = 0
    for start, ms_start, end, msgid, msgstr in read_entries(lines):
        if not msgid.strip():
            continue
        if is_code_like(msgid) or ("\n" in msgid and "\\n" in msgstr):
            if msgstr != msgid:
                replacements.append((ms_start, end, wrap_msgstr(msgid)))
                changed += 1
            continue
        if msgid not in mapping:
            continue
        new = mapping[msgid]
        if is_code_like(new):
            continue
        if new == msgstr:
            continue
        replacements.append((ms_start, end, wrap_msgstr(new)))
        changed += 1
    if not replacements:
        return 0
    out: list[str] = []
    idx = 0
    for ms_start, end, new_lines in replacements:
        out.extend(lines[idx:ms_start])
        out.extend(new_lines)
        idx = end
    out.extend(lines[idx:])
    text = newline.join(out)
    if raw.endswith("\n") and not text.endswith("\n"):
        text += "\n"
    po_path.write_text(text, encoding="utf-8")
    return changed


def load_maps(paths: list[Path]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            mapping.update(
                {
                    normalize_json_text(str(k)): normalize_json_text(str(v))
                    for k, v in data.items()
                    if k
                }
            )
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "msgid" in item and "msgstr" in item:
                    mapping[item["msgid"]] = item["msgstr"]
    return mapping


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    locale = repo / "locale" / "zh_CN" / "LC_MESSAGES"
    map_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else repo / "tmp_zh_out"
    paths = sorted(map_dir.glob("*.json"))
    if not paths:
        print(f"ERROR: no JSON maps in {map_dir}")
        return 1
    mapping = load_maps(paths)
    print(f"Loaded {len(mapping)} translations from {len(paths)} files")
    total = 0
    for po in sorted(locale.rglob("*.po")):
        n = apply_map(po, mapping)
        if n:
            print(f"  {po.relative_to(locale)}: {n} updated")
            total += n
    print(f"Updated {total} msgstr entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Fail on missing, fuzzy, untranslated, or mixed CN–EN zh_CN catalog entries.

Coverage % (check_zh_coverage.py) only counts non-empty msgstr. This checker
catches leftover English in reader-facing Chinese, stale fuzzy matches, and
empty translations.

Usage:
    python3 scripts/check_zh_mix.py
    python3 scripts/check_zh_mix.py --html-root build/html/zh_CN
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CJK_RE = re.compile(r"[\u4e00-\u9fff]")
BACKTICK_RE = re.compile(r"`[^`]*`")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]+\)")
URL_RE = re.compile(r"https?://\S+")
HTML_TAG_RE = re.compile(r"<[^>]+>")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9.+-]*")

# Tokens that may stay English inside otherwise-Chinese sentences.
ALLOW_WORDS = frozenset(
    w.lower()
    for w in """
        ros ros2 ocs2 wbc fsm mpc urdf xacro usd usda glb can gpu ram ssh adb
        usb vr eef ee api ci pr readme sku qos sdk cli yaml json xml html css
        deb apt rviz moveit colcon rosdep gazebo isaac isaacsim lerobot fasim
        fiveages sphinx myst furo ubuntu jazzy nvidia github git python linux
        docker home hold movej arx galbot dobot cr5 hightorque panthera ht
        acone dexcap pico lift lift2s gen1 gen2 gen3 w1 w2 w2r s2 s2r wce3
        int32 string jointstate posestamped mock_components hardware robot
        type launch skill skills deb humanoid composer webxr xrobotoolkit
        enterprise consumer app pc service overlay setup bash cmake
        std_msgs sensor_msgs geometry_msgs rclpy node pose stamped
        fishros unilab mermaid myst-parser sphinx-intl furo
        init_repo quick_start teleop_start run sh
        split_body full_body mock_components
        header publisher subscriber controller manager
        qos lifecycle
        meta quest
        ac one
        fa-deploy-ws open-deploy-ws fa-py-libraries
        left_type right_type robot_profile
        true false none
        vs
        hold home movej
        """.split()
)

# Extra identifiers / brands kept as-is (matched case-insensitively).
ALLOW_WORD_RE = re.compile(
    r"""(?ix)
    ^(?:
        [a-z]+(?:_[a-z0-9]+)+          # package / snake_case
        | [a-z][a-z0-9]*\.(?:py|sh|md|yaml|yml|xml|xacro|launch)
        | [A-Z][a-z]+(?:[A-Z][a-z0-9]+)+  # CamelCase type / class
        | [A-Z]{2,6}                      # HOME, HOLD, USB, GPU
        | v?\d+(?:\.\d+)+
        | /[A-Za-z0-9_./-]+
    )$
    """
)

CODE_LINE_PREFIXES = (
    "ros2 ",
    "sudo ",
    "source ",
    "colcon ",
    "git ",
    "pip ",
    "python",
    "dpkg",
    "make ",
    "cd ",
    "from ",
    "import ",
    "export ",
    "curl ",
    "apt ",
    "mkdir ",
    "ls ",
    "wget ",
    "gz ",
    "ssh ",
    "rosdep ",
    "nvidia-smi",
    "./",
    "uv ",
    "motion-generation",
    "#",
)

PYTHON_START_RE = re.compile(
    r"^\s*(?:from |import |async def |def |class )", re.MULTILINE
)

STATE_LABELS = frozenset(
    {
        "home",
        "hold",
        "movej",
        "ocs2",
        "idle",
        "stand",
        "walk",
    }
)

# Phrases that must not leak into Chinese prose outside backticks.
BANNED_PHRASES = (
    "split body",
    "full body",
    "do not invent",
    "does not invent",
    "this page does not",
    "do not treat",
)


@dataclass
class Entry:
    path: Path
    lineno: int
    fuzzy: bool
    msgid: str
    msgstr: str


@dataclass
class Finding:
    path: str
    lineno: int
    reason: str
    snippet: str


def unescape_po(s: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(nxt, nxt))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def parse_po(path: Path) -> list[Entry]:
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[Entry] = []
    i = 0
    n = len(lines)

    def parse_msg(start: int) -> tuple[str, int]:
        first = lines[start]
        rest = first.split(" ", 1)[1]
        parts = [rest[1:-1] if rest.endswith('"') else rest[1:]]
        j = start + 1
        while j < n and lines[j].startswith('"'):
            raw = lines[j]
            parts.append(raw[1:-1] if raw.endswith('"') else raw[1:])
            j += 1
        return unescape_po("".join(parts)), j

    while i < n:
        if lines[i].startswith("#~"):
            i += 1
            continue
        fuzzy = False
        while i < n and (
            lines[i].startswith("#")
            or lines[i] == ""
        ):
            if lines[i].startswith("#,"):
                flags = [x.strip() for x in lines[i][2:].split(",")]
                fuzzy = "fuzzy" in flags
            if lines[i] == "" and fuzzy:
                # blank after comments still belongs to this entry
                i += 1
                continue
            if lines[i] == "":
                i += 1
                continue
            i += 1
        if i >= n or not lines[i].startswith("msgid "):
            i += 1
            continue
        lineno = i + 1
        msgid, i = parse_msg(i)
        if i < n and lines[i].startswith("msgstr "):
            msgstr, i = parse_msg(i)
        else:
            continue
        entries.append(Entry(path, lineno, fuzzy, msgid, msgstr))
    return entries


def strip_protected(text: str) -> str:
    text = BACKTICK_RE.sub(" ", text)
    text = MD_LINK_RE.sub(lambda m: f" {m.group(1)} ", text)
    text = URL_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = BOLD_RE.sub(r"\1", text)
    return text


def is_allowed_word(word: str) -> bool:
    raw = word.strip(".,;:!?()[]{}<>\"'")
    if not raw:
        return True
    if raw.lower() in ALLOW_WORDS:
        return True
    if ALLOW_WORD_RE.match(raw):
        return True
    return False


MD_ONLY_RE = re.compile(
    r"^(?:\*\*)?(?:\[[^\]]+\]\([^)]+\)(?:\s+)?)+(\*\*)?$",
)
SENTENCE_HINTS = frozenset(
    {
        "the",
        "this",
        "that",
        "these",
        "those",
        "are",
        "is",
        "was",
        "were",
        "not",
        "with",
        "from",
        "when",
        "after",
        "before",
        "there",
        "their",
        "have",
        "has",
        "been",
        "into",
        "only",
        "also",
        "does",
        "do",
        "for",
    }
)


def looks_like_shell(text: str) -> bool:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return False
    hits = 0
    for ln in lines:
        if ln.startswith(CODE_LINE_PREFIXES) or ln.startswith("```") or ln.startswith(
            "from "
        ):
            hits += 1
        elif re.match(r"^[A-Za-z0-9_./${}=:-]+(\s+|$)", ln) and (
            "\\" in ln or ":=" in ln or ln.endswith("\\") or ln.startswith("-")
        ):
            hits += 1
    return hits / len(lines) >= 0.5


def is_code_or_identifier(text: str) -> bool:
    t = text.strip()
    if not t:
        return True
    if "├" in t or "└" in t or "│" in t or "↓" in t:
        return True
    if PYTHON_START_RE.search(t):
        return True
    if re.search(r"\w+\.\w+\(", t) and ("List[" in t or t.strip().startswith("#")):
        return True
    if looks_like_shell(t):
        return True
    compact = re.sub(r"\s+", " ", t)
    if MD_ONLY_RE.match(compact):
        return True
    if compact.lower().startswith("**repository:**"):
        return True
    lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
    if lines and all(
        ln.startswith(CODE_LINE_PREFIXES) or ln.startswith("```") for ln in lines
    ):
        return True
    words = WORD_RE.findall(t)
    if words and all(w.lower() in STATE_LABELS or is_allowed_word(w) for w in words):
        return True
    stripped = strip_protected(t)
    letters = re.sub(r"[^A-Za-z]+", "", stripped)
    slash_bits = [b.strip() for b in re.split(r"[/\n|]", stripped) if b.strip()]
    if slash_bits and all(
        len(WORD_RE.findall(b)) <= 2
        and all(
            is_allowed_word(w) or w.lower() in STATE_LABELS for w in WORD_RE.findall(b)
        )
        for b in slash_bits
    ):
        return True
    return len(letters) < 8


def is_prose(text: str) -> bool:
    if is_code_or_identifier(text):
        return False
    words = [w.lower() for w in WORD_RE.findall(strip_protected(text))]
    if len(words) < 6:
        return False
    return any(w in SENTENCE_HINTS for w in words)


def english_runs(text: str) -> list[str]:
    """Return 2+ word English runs in unprotected text."""
    runs: list[str] = []
    buf: list[str] = []
    for token in re.findall(r"[A-Za-z][A-Za-z0-9.+-]*|[\u4e00-\u9fff]+|.", text):
        if WORD_RE.fullmatch(token):
            buf.append(token)
            continue
        if len(buf) >= 2:
            runs.append(" ".join(buf))
        buf = []
    if len(buf) >= 2:
        runs.append(" ".join(buf))
    return runs


def leftover_mixed(msgid: str, msgstr: str) -> list[str]:
    if not CJK_RE.search(msgstr):
        return []
    plain = strip_protected(msgstr)
    hits: list[str] = []
    low_plain = plain.lower()
    for phrase in BANNED_PHRASES:
        if phrase in low_plain:
            hits.append(phrase)
    msgid_words = {w.lower() for w in WORD_RE.findall(strip_protected(msgid))}
    for run in english_runs(plain):
        words = run.split()
        kept = [w for w in words if not is_allowed_word(w)]
        if len(kept) < 2:
            continue
        # Only flag if the leftover run overlaps the English source.
        if any(w.lower() in msgid_words for w in kept):
            hits.append(run)
    return hits


def snippet(text: str, limit: int = 140) -> str:
    one = re.sub(r"\s+", " ", text).strip()
    if len(one) > limit:
        return one[: limit - 1] + "…"
    return one


def check_entries(entries: list[Entry]) -> list[Finding]:
    findings: list[Finding] = []
    for ent in entries:
        rel = str(ent.path)
        if not ent.msgid.strip():
            continue
        if not ent.msgstr.strip():
            findings.append(
                Finding(rel, ent.lineno, "empty msgstr", snippet(ent.msgid))
            )
            continue
        if ent.fuzzy:
            findings.append(
                Finding(rel, ent.lineno, "active fuzzy", snippet(ent.msgid))
            )
        if ent.msgid == ent.msgstr and is_prose(ent.msgid):
            findings.append(
                Finding(rel, ent.lineno, "untranslated prose", snippet(ent.msgid))
            )
        mixed = leftover_mixed(ent.msgid, ent.msgstr)
        if mixed:
            findings.append(
                Finding(
                    rel,
                    ent.lineno,
                    "mixed leftover English: " + ", ".join(mixed[:3]),
                    snippet(ent.msgstr),
                )
            )
    return findings


ARTICLE_RE = re.compile(
    r"<article\b[^>]*>(.*?)</article>", re.IGNORECASE | re.DOTALL
)
BLOCK_RE = re.compile(
    r"<(p|li|td|th|blockquote)\b[^>]*>(.*?)</\1>", re.IGNORECASE | re.DOTALL
)
SKIP_HTML_RE = re.compile(
    r"<(pre|code|script|style|nav|svg)\b[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)


def check_html(html_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not html_root.is_dir():
        return findings
    for path in sorted(html_root.rglob("*.html")):
        if "_static" in path.parts or "search.html" in path.name:
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        articles = ARTICLE_RE.findall(html) or [html]
        rel = str(path)
        for article in articles:
            cleaned = SKIP_HTML_RE.sub(" ", article)
            for _tag, body in BLOCK_RE.findall(cleaned):
                text = HTML_TAG_RE.sub(" ", body)
                text = re.sub(r"\s+", " ", text).strip()
                if len(text) < 80:
                    continue
                if is_code_or_identifier(text):
                    continue
                # Package names / types should not drown a short Chinese lead-in.
                prose = re.sub(r"[A-Za-z]+(?:[_./-][A-Za-z0-9]+)+", " ", text)
                prose = re.sub(r"\b[A-Z][a-z]+(?:[A-Z][a-z0-9]+)+\b", " ", prose)
                cjk = len(CJK_RE.findall(prose))
                letters = len(re.findall(r"[A-Za-z]", prose))
                if letters < 40:
                    continue
                denom = cjk + letters
                if denom and cjk / denom < 0.18:
                    findings.append(
                        Finding(
                            rel,
                            0,
                            "mostly-English HTML paragraph",
                            snippet(text),
                        )
                    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check zh_CN catalogs for missing, fuzzy, or mixed translations"
    )
    parser.add_argument(
        "--locale-dir",
        type=Path,
        default=None,
        help="Path to locale/zh_CN/LC_MESSAGES (default: <repo>/locale/zh_CN/LC_MESSAGES)",
    )
    parser.add_argument(
        "--html-root",
        type=Path,
        default=None,
        help="Optional built zh HTML root (default: <repo>/build/html/zh_CN if present)",
    )
    parser.add_argument(
        "--require-html",
        action="store_true",
        help="Fail if the zh HTML root is missing",
    )
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent.parent
    locale_dir = args.locale_dir or (repo / "locale/zh_CN/LC_MESSAGES")
    if not locale_dir.is_dir():
        print(f"ERROR: locale directory not found: {locale_dir}", file=sys.stderr)
        return 1

    findings: list[Finding] = []
    for po in sorted(locale_dir.rglob("*.po")):
        findings.extend(check_entries(parse_po(po)))

    html_root = args.html_root
    if html_root is None:
        candidate = repo / "build/html/zh_CN"
        if candidate.is_dir():
            html_root = candidate
    if html_root is not None:
        if not html_root.is_dir():
            if args.require_html:
                print(f"ERROR: zh HTML root not found: {html_root}", file=sys.stderr)
                return 1
        else:
            findings.extend(check_html(html_root))
    elif args.require_html:
        print("ERROR: --require-html set but no HTML root", file=sys.stderr)
        return 1

    print("zh_CN mix / QA report")
    print("=====================")
    print(f"Findings: {len(findings)}")
    print()
    for item in findings:
        loc = f"{item.path}:{item.lineno}" if item.lineno else item.path
        print(f"{loc}")
        print(f"  {item.reason}")
        print(f"  {item.snippet}")
        print()

    if findings:
        print(f"✗ FAIL: {len(findings)} must-fix finding(s)")
        return 1
    print("✓ PASS: no empty, fuzzy, untranslated-prose, or mixed leftover English")
    return 0


if __name__ == "__main__":
    sys.exit(main())

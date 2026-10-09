#!/usr/bin/env python3
"""Fetch pinned upstream Markdown into source/_vendored/.

Pins live in source/_vendored/SOURCES.json (repo + path + commit SHA).
This site vendors README.md only — never API_REFERENCE.md.
Ids currently include ros2_robot_interface, basic_joint_controller,
and adaptive_gripper_controller.

Usage:
    python3 scripts/vendor_upstream_md.py --sync
    python3 scripts/vendor_upstream_md.py --check
    python3 scripts/vendor_upstream_md.py --bump ros2_robot_interface
    python3 scripts/vendor_upstream_md.py --bump basic_joint_controller --sha <full-sha>

Bump writes the new SHA into SOURCES.json, re-fetches, and rewrites the
vendored file. Commit both SOURCES.json and the markdown together.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = REPO_ROOT / "source" / "_vendored" / "SOURCES.json"
USER_AGENT = "fiveages-sim-docs-vendor/1.0"

# Markdown images / HTML <img> whose src is not http(s) — relative or
# private paths that break the Sphinx HTML build.
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(
    r"<img\b[^>]*\bsrc\s*=\s*['\"]([^'\"]+)['\"][^>]*/?>",
    re.IGNORECASE,
)


def load_sources() -> dict[str, Any]:
    if not SOURCES_PATH.is_file():
        raise SystemExit(f"missing {SOURCES_PATH.relative_to(REPO_ROOT)}")
    return json.loads(SOURCES_PATH.read_text(encoding="utf-8"))


def save_sources(data: dict[str, Any]) -> None:
    SOURCES_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def raw_url(repo: str, sha: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repo}/{sha}/{path}"


def blob_url(repo: str, sha: str, path: str) -> str:
    return f"https://github.com/{repo}/blob/{sha}/{path}"


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.URLError as exc:
        raise SystemExit(f"fetch failed: {url}\n{exc}") from exc


def fetch_text(url: str) -> str:
    return fetch_bytes(url).decode("utf-8")


def latest_main_sha(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}/commits/main"
    payload = json.loads(fetch_text(url))
    sha = payload.get("sha")
    if not isinstance(sha, str) or len(sha) < 7:
        raise SystemExit(f"could not read commit SHA from {url}")
    return sha


def is_remote_url(src: str) -> bool:
    return src.strip().lower().startswith(("https://", "http://"))


def strip_broken_images(markdown: str) -> tuple[str, int]:
    """Drop relative / private images; keep absolute http(s) URLs."""
    removed = 0

    def drop_md(match: re.Match[str]) -> str:
        nonlocal removed
        src = match.group(1).strip()
        if is_remote_url(src):
            return match.group(0)
        removed += 1
        return ""

    def drop_html(match: re.Match[str]) -> str:
        nonlocal removed
        src = match.group(1).strip()
        if is_remote_url(src):
            return match.group(0)
        removed += 1
        return ""

    markdown = MD_IMAGE_RE.sub(drop_md, markdown)
    markdown = HTML_IMG_RE.sub(drop_html, markdown)
    return markdown, removed


def pin_header(entry: dict[str, Any]) -> str:
    repo = entry["repo"]
    sha = entry["sha"]
    path = entry["path"]
    return (
        f"<!-- vendored from {repo}@{sha} path={path} "
        f"blob={blob_url(repo, sha, path)} ; "
        f"bump: python3 scripts/vendor_upstream_md.py --bump "
        f"{entry['id']} -->\n"
    )


def parse_header_sha(text: str) -> str | None:
    match = re.search(r"<!-- vendored from \S+@([0-9a-f]{7,40}) ", text)
    return match.group(1) if match else None


def dest_path(entry: dict[str, Any]) -> Path:
    return REPO_ROOT / entry["dest"]


def write_vendored(entry: dict[str, Any], body: str, *, stripped: int) -> str:
    dest = dest_path(entry)
    dest.parent.mkdir(parents=True, exist_ok=True)
    cleaned, n_img = strip_broken_images(body)
    stripped += n_img
    text = pin_header(entry) + "\n" + cleaned
    if not text.endswith("\n"):
        text += "\n"
    dest.write_text(text, encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    rel = dest.relative_to(REPO_ROOT)
    extra = f", stripped {stripped} relative image(s)" if stripped else ""
    print(f"wrote {rel} ({entry['sha'][:12]}{extra})")
    return digest


def sync_entry(entry: dict[str, Any]) -> str:
    url = raw_url(entry["repo"], entry["sha"], entry["path"])
    body = fetch_text(url)
    digest = write_vendored(entry, body, stripped=0)
    entry["sha256"] = digest
    return digest


def check_entry(entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    dest = dest_path(entry)
    rel = dest.relative_to(REPO_ROOT)
    if not dest.is_file():
        return [f"missing vendored file {rel}"]
    text = dest.read_text(encoding="utf-8")
    header_sha = parse_header_sha(text)
    if header_sha != entry["sha"]:
        errors.append(
            f"{rel}: header SHA {header_sha!r} != SOURCES.json {entry['sha']!r}"
        )
    expected = entry.get("sha256")
    if expected:
        actual = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if actual != expected:
            errors.append(
                f"{rel}: sha256 mismatch (file was edited; re-run --sync)"
            )
    if "API_REFERENCE.md" in Path(entry["path"]).name:
        errors.append(f"{rel}: API_REFERENCE.md must not be vendored")
    return errors


def find_entry(data: dict[str, Any], ident: str) -> dict[str, Any]:
    for entry in data["sources"]:
        if entry["id"] == ident or entry["repo"].endswith("/" + ident) or ident in (
            entry["id"],
            entry["repo"].split("/")[-1],
        ):
            return entry
    known = ", ".join(e["id"] for e in data["sources"])
    raise SystemExit(f"unknown source {ident!r}; known: {known}")


def cmd_sync(data: dict[str, Any]) -> int:
    for entry in data["sources"]:
        sync_entry(entry)
    save_sources(data)
    return 0


def cmd_check(data: dict[str, Any]) -> int:
    errors: list[str] = []
    for entry in data["sources"]:
        errors.extend(check_entry(entry))
    if errors:
        print("ERROR: vendored upstream markdown pin check failed:")
        for err in errors:
            print(f"  {err}")
        print("Re-run: python3 scripts/vendor_upstream_md.py --sync")
        return 1
    print("OK: vendored pins match source/_vendored/SOURCES.json")
    return 0


def cmd_bump(data: dict[str, Any], ident: str, sha: str | None) -> int:
    entry = find_entry(data, ident)
    new_sha = sha or latest_main_sha(entry["repo"])
    old = entry["sha"]
    entry["sha"] = new_sha
    sync_entry(entry)
    save_sources(data)
    print(f"bumped {entry['id']}: {old} -> {new_sha}")
    print("Commit SOURCES.json and the vendored markdown together.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--sync",
        action="store_true",
        help="Fetch each pin in SOURCES.json and rewrite vendored files",
    )
    group.add_argument(
        "--check",
        action="store_true",
        help="Verify vendored files match SOURCES.json (no network)",
    )
    group.add_argument(
        "--bump",
        metavar="ID",
        help="Move one pin to --sha or latest main, then --sync that entry",
    )
    parser.add_argument(
        "--sha",
        help="Commit SHA to use with --bump (default: latest main)",
    )
    args = parser.parse_args()
    data = load_sources()
    if args.check:
        return cmd_check(data)
    if args.bump:
        return cmd_bump(data, args.bump, args.sha)
    return cmd_sync(data)


if __name__ == "__main__":
    sys.exit(main())

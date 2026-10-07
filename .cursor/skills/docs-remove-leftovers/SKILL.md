---
name: docs-remove-leftovers
description: >-
  After moving or merging Sphinx pages, delete the old file instead of leaving
  a stub. Use when consolidating docs, renaming a page, retiring a leftover,
  or when tempted to write “This page is merged into…”. 删除遗留、合并页面、stub
  redirect、hidden toctree、删旧页。
---

# Remove leftovers after a move

When content is **moved, merged, or rewritten**, delete the old page. Do **not** keep a stub that only points at the new URL.

Reader pages must stay product docs. This rule lives here (and in `docs-writing`) — not in Overview / How-To / Concepts / Reference.

## Never leave a stub

Do not add or keep pages whose only job is:

- “This page is merged into …”
- “Moved to …” / “Use that page” / “See instead”
- A hidden `{toctree}` entry “for old bookmarks”
- An HTML/Sphinx redirect, unless the **user explicitly** asks for URL compatibility

Example of what to delete (already gone): `source/4-reference/descriptions/5-fa_robots.md` was a two-line pointer at `4-fiveages_umbrella.md`.

## Checklist (every move)

1. **New canonical page** exists and has the real content.
2. **Delete** the old `source/**/*.md`.
3. **Remove** it from every `{toctree}` (including `:hidden:`). Prefer one visible toctree of real pages.
4. **Delete** the matching `locale/zh_CN/LC_MESSAGES/**/<old>.po` (and any other locale artifact).
5. **Retarget** inbound links (`rg` the old stem / path) to the new page. Drop “merged page” / “older pages are merged here” sentences once the stub is gone.
6. **Do not** invent APIs, flags, or private trees while rewriting the surviving page.
7. Builds: `make html`, `make html-zh_CN`, `python3 scripts/check_zh_coverage.py --threshold 95`, `python3 scripts/check_zh_mix.py`.

Obsolete `#~` strings in *other* `.po` files can stay; they are not reader pages.

## Scan for leftovers

After a merge, search `source/**/*.md`:

```bash
rg -n -i 'merged into|moved to|use that page|see instead|this page is merged' source
rg -n ':hidden:' source
```

If a hit is only a pointer (a few lines, no product facts), delete it the same way. Keep real pages that happen to say “this page explains …” or “this page stops at …” — those are scope sentences, not stubs.

## Related

- Writer facts / no agent-meta on reader pages: `.cursor/skills/docs-writing/SKILL.md`
- zh leftover English: `.cursor/skills/zh-translation-qa/SKILL.md`

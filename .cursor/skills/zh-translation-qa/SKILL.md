---
name: zh-translation-qa
description: >-
  Scan fiveages-sim/docs zh_CN for missing, fuzzy, or mixed Chinese–English
  reader text. Use when editing locale/zh_CN, after gettext/update-po, when a
  page looks bilingual, or when asked to 筛查翻译 / 中英文混杂 / fuzzy / leftover
  English. Coverage percent alone is not enough.
---

# zh_CN translation QA

`check_zh_coverage.py` only asks “is `msgstr` non-empty?”. Reader pages can still show English when:

- the entry is `#, fuzzy` (Sphinx falls back to `msgid`)
- `msgstr` copies English prose
- a Chinese sentence still contains leftover English from the old `msgid` (outside backticks)

## When to run

After any `source/**/*.md` edit that changes strings, after `make gettext` / `make update-po`, and before calling a zh page “done”.

```bash
python3 scripts/check_zh_coverage.py --threshold 95
python3 scripts/check_zh_mix.py
# after a zh HTML build (optional HTML pass):
make html-zh_CN
python3 scripts/check_zh_mix.py --html-root build/html/zh_CN --require-html
```

Exit non-zero = must-fix. Do not ship a page that still fails.

## What the checker reports

| Reason | Meaning | Fix |
|--------|---------|-----|
| `empty msgstr` | Non-empty `msgid`, empty translation | Write Chinese |
| `active fuzzy` | sphinx-intl rematch; HTML shows English | Align `msgstr` with the **current** `msgid`, then drop `#, fuzzy` |
| `untranslated prose` | `msgstr == msgid` and the string is prose | Translate. Keep code, topics, type names, FSM labels |
| `mixed leftover English` | Chinese sentence still has English words/phrases from `msgid` outside `` `code` `` | Rewrite in Chinese; keep allowlisted tokens |
| `mostly-English HTML paragraph` | Built `build/html/zh_CN` paragraph is almost all English | Same as above (often a fuzzy fallback) |

Skip obsolete `#~` entries. The PO **header** (`msgid ""`) may stay `#, fuzzy`.

## Keep English (do not “translate”)

- Backticked code, paths, launch args, `/topics`, message types
- Package / class / skill names
- FSM labels `HOME` / `HOLD` / `MOVEJ` (and `Home` / `Hold` / `MoveJ` in tables)
- Tokens such as ROS, OCS2, Gazebo, Isaac, LeRobot, FaSim, README, Pico, ARX

Product terms that **do** have Chinese in this site: **split body** → **分体** / **分体控制**; **full body** / whole-body → **全身** / **全身控制**; **driver layer** → **驱动层** (not 硬件接口). Do not leave `split body` / `full body` in Chinese sentences. Keep CLI `list_hardware_interfaces` and plugin class names in backticks.

## How to fill a hit

1. Read the current `msgid` (ignore `#~` and the old fuzzy guess).
2. Write positive reader Chinese. No “不要编造 / Do not invent / This page does not…”.
3. Unknown / private → “开通后见该仓库 README”.
4. Remove `#, fuzzy` (keep `python-brace-format` if present).
5. Re-run `check_zh_mix.py` until PASS.

Do not run `apply_zh_json.py` on all of `tmp_zh_out` (it overwrites unrelated catalogs).

## Related

- Writer constraints: `.cursor/skills/docs-writing/SKILL.md`
- Script: `scripts/check_zh_mix.py`

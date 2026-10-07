# Cursor skills for fiveages-sim/docs

Project skills live here so agents editing this Sphinx site can load them.

```
.cursor/skills/
  README.md
  <skill-name>/
    SKILL.md          # required
    reference.md      # optional
```

## Add a skill

1. Create `.cursor/skills/<name>/SKILL.md`.
2. `name` must be lowercase letters, numbers, and hyphens only.
3. `description` must say **what** it does and **when** to use it (include Chinese and English trigger terms).
4. Keep `SKILL.md` under 500 lines. Put long examples in `reference.md`.

Do not put skills in `~/.cursor/skills-cursor/` (Cursor internals).

## Skills

| Skill | Use when |
|-------|----------|
| [docs-writing](docs-writing/SKILL.md) | Writing or editing Sphinx/MyST pages in this repo — keep facts sourced, keep reader pages free of agent-meta phrasing |
| [docs-remove-leftovers](docs-remove-leftovers/SKILL.md) | After a move/merge — delete the old page, toctree, and `.po`; do not leave “merged into” stubs |
| [zh-translation-qa](zh-translation-qa/SKILL.md) | After gettext/update-po or when zh pages look mixed — scan fuzzy / leftover English (`check_zh_mix.py`; coverage % is not enough) |

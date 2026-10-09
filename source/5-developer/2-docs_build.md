# Documentation Build

Building and contributing to this documentation site.

## Technology Stack

- **Sphinx** — Documentation generator
- **Furo** — Theme
- **MyST** — Markdown parser
- **sphinx-intl** — Internationalization
- **sphinxcontrib-mermaid** — Diagram support

## Local Build

### Prerequisites

```bash
# Python 3.12
pip install -r requirements.txt
```

### Build English

```bash
make html
```

Output in `build/html/`.

### Build Chinese

```bash
make html-zh_CN
```

Output in `build/html/zh_CN/`.

### Build Both

```bash
make html-all
```

### View Locally

```bash
python -m http.server -d build/html 8000
```

Open `http://localhost:8000`. The Chinese tree is at `http://localhost:8000/zh_CN/`. The sidebar language dropdown stays on the same page when switching (`foo.html` ↔ `zh_CN/foo.html`).

## Language switcher

The Furo sidebar uses a UniLab-style `<select>` **below the brand, above search** (`source/_templates/sidebar/lang_switcher.html`).

This site stays on **sphinx-intl dual builds** (English at the HTML root, Chinese under `zh_CN/`). It does **not** use UniLab’s parallel `source/en/` + `source/zh_CN/` single-build tree. Counterpart URLs are therefore relative hrefs injected in `conf.py` (`html-page-context`), not `pathto()` of the other locale (that page is not in the same builder’s `found_docs`).

On GitHub Pages the site lives at `/docs/`. Relative hrefs resolve to `/docs/...` ↔ `/docs/zh_CN/...`. Do **not** link to domain-root `/zh_CN/` (404). `html_baseurl` is `https://fiveages-sim.github.io/docs/`.

## Translation Workflow

### Update Source Strings

After changing English content:

```bash
make gettext
sphinx-intl update -p build/gettext -l zh_CN
```

### Check translations

A non-empty `msgstr` is not enough. After filling catalogs:

```bash
python3 scripts/check_zh_coverage.py --threshold 95
python3 scripts/check_zh_mix.py
```

`check_zh_mix.py` fails on empty translations, active `#, fuzzy` entries, English prose copied into `msgstr`, and leftover English inside Chinese sentences. How to triage hits: `.cursor/skills/zh-translation-qa/SKILL.md`.

### Edit Translations

Edit files in `locale/zh_CN/LC_MESSAGES/*.po`:

```text
#: source/index.md:1
msgid "FiveAges Sim Documentation"
msgstr "FiveAges Sim 文档"
```

### Build Translated Version

```bash
make html-zh_CN
```

## File Structure

:::{code-block} none
docs/
├── source/
│   ├── conf.py              # Sphinx configuration
│   ├── index.md             # Landing page
│   ├── 0-overview/          # Overview section
│   ├── 1-getting_started/   # Getting started
│   ├── 2-how_to/            # How-to guides
│   ├── 3-concepts/          # Concepts
│   ├── 4-reference/         # Reference
│   ├── 5-developer/         # Developer guide
│   ├── _static/             # Static files (CSS, images)
│   ├── _templates/          # Custom templates
│   └── _vendored/           # Pinned upstream README copies (see below)
├── locale/
│   └── zh_CN/
│       └── LC_MESSAGES/     # Chinese translations
├── Makefile
└── requirements.txt
:::

## Writing Guidelines

Author constraints (what you may claim, how to handle private repos, keep agent-meta out of reader pages): `.cursor/skills/docs-writing/SKILL.md`.

### Markdown (MyST)

Use MyST-flavored Markdown. **Never nest `` ``` `` fences inside `` ```{admonition} ``** — that breaks zh_CN rendering. Use colon fences (`:::`) when an admonition must contain a code block, and wrap examples of fences in a 4-backtick outer fence:

````markdown
# Heading

Paragraph text.

## Subheading

- List item
- Another item

```bash
code block
```

:::{admonition} Note
:class: tip

Admonition content.
:::
````

### Code Blocks

Use fenced code blocks with a language tag (or `{code-block} none` for trees). Unlabeled `` ``` `` fences become RST `::` and zh_CN HTML can leak a bare `::`. Keep the matching `.po` `msgstr` **identical** to `msgid` for every code or tree block: a translated comment, extra line, or dropped line is re-parsed as RST `::`, and MyST `colon_fence` then drops the real block.

:::{code-block} none
Controllers
        ↓
Hardware
:::

Language-tagged examples:

````markdown
```bash
ros2 launch package launch.py
```

```python
from ros2_robot_interface import ROS2RobotInterface
```
````

### Admonitions

Use backtick fences only when the body has **no** nested ` ``` ` code fences:

````markdown
```{admonition} Warning
:class: warning

Warning content.
```

```{admonition} TODO
:class: warning

To be completed.
```
````

If the admonition body needs a fenced code block, use a colon fence instead:

````markdown
:::{admonition} Path Verification
:class: tip

Verify the binary exists:

```bash
ls ~/isaacsim/python.sh
```
:::
````

### Cross-References

```markdown
See [Architecture](../0-overview/1-architecture.md).

See {doc}`../0-overview/1-architecture`.
```

### Tables

```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
```

## Diagrams

Use Mermaid for diagrams:

````markdown
```{mermaid}
flowchart LR
    A --> B --> C
```
````

## Vendored upstream README

`source/_vendored/` holds **pinned commit** copies of public upstream Markdown so Sphinx can `{include}` a short slice. This site vendors **README.md** files only: `ros2_robot_interface`, plus `basic_joint_controller` and `adaptive_gripper_controller` from [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control). [ros2_robot_interface API_REFERENCE.md](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md) stays a GitHub link and is not copied into `_vendored/`.

Pins: `source/_vendored/SOURCES.json` (`repo`, `path`, full commit `sha`, `dest`).

```bash
# Re-fetch every pin in SOURCES.json
python3 scripts/vendor_upstream_md.py --sync
make vendor-upstream

# Verify header SHA / sha256 (CI; no network)
python3 scripts/vendor_upstream_md.py --check
make vendor-check

# Move one pin to latest main, or to a SHA
python3 scripts/vendor_upstream_md.py --bump ros2_robot_interface
python3 scripts/vendor_upstream_md.py --bump basic_joint_controller --sha <full-sha>
python3 scripts/vendor_upstream_md.py --bump adaptive_gripper_controller --sha <full-sha>
```

Commit `SOURCES.json` and the vendored markdown together. Relative / private images are stripped on fetch so the HTML build does not depend on missing files.

After a bump, recompute `{include}` **`:start-line:` / `:end-line:`** on the pages that slice a vendored README ([basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md), [gripper plugins](../4-reference/controllers/6-gripper_teleop_plugins.md), [ros2_robot_interface](../4-reference/python_apps/1-ros2_robot_interface.md)). Line numbers are 1-based. Set `:end-line:` to the last line of the slice — typically the blank line or `---` **before** the next heading — then rebuild and confirm that heading is not in the HTML.

Do **not** cut a slice with `:end-before:` / `:start-after:` against heading text. Those options truncate **mid-line**, so a marker such as `Demo Launch` against `## 7. Demo Launch` leaves `## 7.` as an empty-ish heading. You also cannot put `#` in those option values — Docutils treats `#` as a comment.

`conf.py` lists `_vendored/` in `exclude_patterns` so the copy is not a sidebar page.

## CI/CD

GitHub Actions builds documentation on:
- Push to main (deploy)
- Pull requests (check build)

CI fails when:
- vendored README pin in `source/_vendored/SOURCES.json` does not match the committed file
- zh_CN translation coverage is below 95%
- `check_zh_mix.py` finds empty, fuzzy, untranslated-prose, or mixed leftover English
- Source files nest `` ``` `` inside `` ```{admonition} ``
- Sphinx emits any warning (`SPHINXOPTS=-W`)
- Built HTML contains a literal `` ``` `` fence (broken MyST nesting)
- Language switcher uses domain-root `/zh_CN/` (missing GitHub Pages `/docs`)

Build must pass before merging.

## Contributing

1. Fork the docs repository
2. Make changes
3. Test locally with `make html-all`
4. Submit pull request

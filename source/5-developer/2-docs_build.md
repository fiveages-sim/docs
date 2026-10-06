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
│   └── _templates/          # Custom templates
├── locale/
│   └── zh_CN/
│       └── LC_MESSAGES/     # Chinese translations
├── Makefile
└── requirements.txt
:::

## Writing Guidelines

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

Use fenced code blocks with language. **Do not use unlabeled** `` ``` `` **fences** for ASCII diagrams or directory trees — sphinx-intl turns those into RST `::` and Chinese HTML leaks a bare `::`. Use a colon fence instead:

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
from ros2_robot_interface import RobotInterface
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

## CI/CD

GitHub Actions builds documentation on:
- Push to main (deploy)
- Pull requests (check build)

CI fails when:
- zh_CN translation coverage is below 95%
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

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
# Python 3.10+
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

Open `http://localhost:8000`.

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

```
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
```

## Writing Guidelines

### Markdown (MyST)

Use MyST-flavored Markdown:

```markdown
# Heading

Paragraph text.

## Subheading

- List item
- Another item

```bash
code block
```

```{admonition} Note
:class: tip

Admonition content.
```
```

### Code Blocks

Use fenced code blocks with language:

````markdown
```bash
ros2 launch package launch.py
```

```python
from ros2_robot_interface import RobotInterface
```
````

### Admonitions

```markdown
```{admonition} Warning
:class: warning

Warning content.
```

```{admonition} TODO
:class: warning

To be completed.
```
```

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

Build must pass before merging.

## Contributing

1. Fork the docs repository
2. Make changes
3. Test locally with `make html-all`
4. Submit pull request

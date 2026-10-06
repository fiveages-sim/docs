# FiveAges Sim Documentation

Public documentation for the [FiveAges Sim](https://github.com/fiveages-sim) robotics ecosystem.

**Live site:** https://fiveages-sim.github.io/docs/

## Building Locally

### Prerequisites

- Python 3.12
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Build English Documentation

```bash
make html
```

Output is in `build/html/`. Open `build/html/index.html` in a browser.

### Build Chinese Documentation

```bash
make html-zh_CN
```

Output is in `build/html/zh_CN/`.

### Build Both Languages

```bash
make html-all
```

### Local Preview Server

```bash
python -m http.server -d build/html 8000
```

Then open http://localhost:8000

## Translation Workflow

### Update Translatable Strings

After modifying English source files:

```bash
# Extract strings
make gettext

# Update .po files
sphinx-intl update -p build/gettext -l zh_CN
```

### Edit Translations

Edit files in `locale/zh_CN/LC_MESSAGES/*.po`:

```po
msgid "Original English text"
msgstr "翻译后的中文文本"
```

### Verify Build

```bash
make html-zh_CN
```

## Directory Structure

```
docs/
├── source/               # Documentation source (MyST Markdown)
│   ├── conf.py          # Sphinx configuration
│   ├── index.md         # Landing page
│   ├── 0-overview/      # Overview section
│   ├── 1-getting_started/
│   ├── 2-how_to/
│   ├── 3-concepts/
│   ├── 4-reference/
│   ├── 5-developer/
│   ├── _static/         # Static files (CSS)
│   └── _templates/      # Custom templates
├── locale/              # Translations
│   └── zh_CN/
│       └── LC_MESSAGES/ # Chinese .po files
├── build/               # Build output (gitignored)
├── Makefile
├── requirements.txt
└── README.md
```

## Technology Stack

- **[Sphinx](https://www.sphinx-doc.org/)** — Documentation generator
- **[Furo](https://pradyunsg.me/furo/)** — Theme
- **[MyST Parser](https://myst-parser.readthedocs.io/)** — Markdown support
- **[sphinx-intl](https://sphinx-intl.readthedocs.io/)** — Internationalization
- **[sphinxcontrib-mermaid](https://sphinxcontrib-mermaid-demo.readthedocs.io/)** — Diagram support
- **[sphinx-copybutton](https://sphinx-copybutton.readthedocs.io/)** — Code copy buttons

## Contributing

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Test locally with `make html-all`
5. Submit a pull request

See `source/5-developer/1-contributing.md` for guidelines.

## CI/CD

GitHub Actions automatically:
- Builds both languages on every push to `main`
- Checks the build on pull requests
- Deploys to GitHub Pages on merge to `main`

## License

Documentation content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

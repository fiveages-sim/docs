# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from language_switcher import switcher_hrefs  # noqa: E402

# -- Project information -----------------------------------------------------
project = 'FiveAges Sim'
copyright = '2024-2026, FiveAges'
author = 'FiveAges'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx_copybutton',
    'sphinxcontrib.mermaid',
]

templates_path = ['_templates']
# Vendored upstream README copies are included from other pages; they are
# not standalone Sphinx documents.
exclude_patterns = ['_vendored', '_vendored/**']

# Source file suffixes
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document
master_doc = 'index'

# -- MyST configuration ------------------------------------------------------
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'fieldlist',
    'substitution',
    'tasklist',
]
myst_heading_anchors = 3

# -- Mermaid configuration ---------------------------------------------------
mermaid_version = "10.6.1"
mermaid_init_js = "mermaid.initialize({startOnLoad:true, theme:'default'});"

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_title = 'FiveAges Sim Docs'
html_static_path = ['_static']

# Furo theme options
html_theme_options = {
    "source_repository": "https://github.com/fiveages-sim/docs",
    "source_branch": "main",
    "source_directory": "source/",
    "light_css_variables": {
        "color-brand-primary": "#2980b9",
        "color-brand-content": "#2980b9",
    },
    "sidebar_hide_name": False,
}

# Custom CSS
html_css_files = ['custom.css']

# Custom sidebar templates (UniLab order: brand, language dropdown, search, nav)
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/lang_switcher.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
    ],
}

# -- Internationalization ----------------------------------------------------
language = 'en'
locale_dirs = ['../locale/']
gettext_compact = False
gettext_uuid = True
gettext_additional_targets = ['literal-block', 'raw']

# -- Language switcher for Furo ----------------------------------------------
# GitHub Pages project site is served at /docs/, not the domain root.
# The sidebar dropdown uses *relative* counterpart hrefs so that:
#   https://fiveages-sim.github.io/docs/foo.html
#     ↔ https://fiveages-sim.github.io/docs/zh_CN/foo.html
# Domain-root ``/zh_CN/`` 404s (missing the /docs prefix). Absolute
# ``/docs/zh_CN/`` works on Pages but breaks local ``http.server`` previews.
html_baseurl = "https://fiveages-sim.github.io/docs/"


def _inject_language_switcher(
    app: Any,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: Any,
) -> None:
    lang = app.config.language or "en"
    if lang not in ("en", "zh_CN"):
        lang = "en"
    context["current_language"] = lang
    context["language_switcher_hrefs"] = switcher_hrefs(pagename, lang)


def setup(app: Any) -> dict[str, Any]:
    app.connect("html-page-context", _inject_language_switcher)
    return {"parallel_read_safe": True}

# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

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
exclude_patterns = []

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

# Custom sidebar templates
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/languages.html",
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
# GitHub Pages project site base URL (deployed at /docs/)
html_baseurl = "https://fiveages-sim.github.io/docs/"

# We use custom template to provide language switching
# Paths must include /docs/ prefix for GitHub Pages project site
html_context = {
    "languages": [
        ("English", "/docs/"),
        ("简体中文", "/docs/zh_CN/"),
    ],
}

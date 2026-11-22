"""Configuration for the theme's own documentation and kitchen-sink demo."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

project = "Carbon Sphinx Theme"
copyright = "2026, the sphinx-carbon-theme authors"
author = "the sphinx-carbon-theme authors"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

html_theme = "carbon"
html_title = project
html_theme_options = {
    "header_links": [
        {"name": "Docs", "doc": "index"},
        {"name": "Kitchen sink", "doc": "kitchen-sink/index"},
    ],
    "repository_url": "https://github.com/example/sphinx-carbon-theme",
}
html_last_updated_fmt = "%Y-%m-%d"

todo_include_todos = True
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
intersphinx_disabled_reftypes = ["*"]
autodoc_member_order = "bysource"

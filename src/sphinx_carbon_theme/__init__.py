"""A Sphinx theme implementing the IBM Carbon Design System."""

from __future__ import annotations

import hashlib
from functools import cache
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TYPE_CHECKING, Any

from sphinx.util import logging

if TYPE_CHECKING:
    from docutils.nodes import document
    from sphinx.application import Sphinx

try:
    __version__ = version("sphinx-carbon-theme")
except PackageNotFoundError:  # running from a source tree without installing
    __version__ = "0.0.0"

THEME_PATH = Path(__file__).parent / "theme" / "carbon"

#: Carbon theme zones that may be configured for light and dark mode.
CARBON_THEMES = ("white", "g10", "g90", "g100")

logger = logging.getLogger(__name__)


@cache
def _asset_query() -> str:
    """Return a cache-busting query string for the bundled JavaScript."""
    script = THEME_PATH / "static" / "scripts" / "carbon-sphinx.js"
    try:
        digest = hashlib.sha256(script.read_bytes()).hexdigest()[:12]
    except FileNotFoundError:
        msg = (
            f"{script} is missing. The theme's static assets have not been "
            "built; run `npm ci && npm run build` in the theme repository, or "
            "install a released wheel."
        )
        raise RuntimeError(msg) from None
    return f"?v={digest}"


def _theme_zone(context: dict[str, Any], option: str, default: str) -> str:
    value = str(context.get(f"theme_{option}", default)).strip()
    if value in CARBON_THEMES:
        return value
    logger.warning(
        "carbon theme: invalid %s %r, expected one of %s; using %r",
        option,
        value,
        ", ".join(CARBON_THEMES),
        default,
        type="carbon_theme",
        once=True,
    )
    return default


def _header_links(context: dict[str, Any]) -> list[dict[str, str]]:
    """Normalise the ``header_links`` option.

    Each entry is a mapping with ``name`` and either ``url`` (used as is)
    or ``doc`` (a document name resolved relative to the current page).
    """
    raw = context.get("theme_header_links") or []
    if isinstance(raw, str):
        if raw.strip():
            logger.warning(
                "carbon theme: header_links must be a list of dicts, not a string",
                type="carbon_theme",
                once=True,
            )
        return []
    links = []
    pathto = context["pathto"]
    for entry in raw:
        if not isinstance(entry, dict) or "name" not in entry:
            logger.warning(
                "carbon theme: ignoring header_links entry %r", entry, type="carbon_theme", once=True
            )
            continue
        if "doc" in entry:
            url = pathto(entry["doc"])
        else:
            url = entry.get("url", "#")
        links.append({"name": str(entry["name"]), "url": url})
    return links


def _html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: document | None,
) -> None:
    # Only act for the carbon theme (or a theme inheriting from it): those
    # are the only ones defining the carbon options.
    if "theme_light_theme" not in context or "theme_dark_theme" not in context:
        return
    context["carbon_version"] = __version__
    context["carbon_asset_query"] = _asset_query()
    context["carbon_light_theme"] = _theme_zone(context, "light_theme", "white")
    context["carbon_dark_theme"] = _theme_zone(context, "dark_theme", "g100")
    context["carbon_header_links"] = _header_links(context)


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_html_theme("carbon", str(THEME_PATH))
    app.connect("html-page-context", _html_page_context)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

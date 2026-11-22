"""Build tests: the demo docs build cleanly and the output has the theme's structure."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

DOCS = Path(__file__).parent.parent / "docs"


def build(srcdir: Path, outdir: Path) -> str:
    """Build HTML in a fresh process; return the warning output.

    A subprocess per build keeps Sphinx/docutils global state (registered
    nodes, directives) from leaking between builds.
    """
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "-E", "-q", str(srcdir), str(outdir)],
        capture_output=True,
        text=True,
        env={**os.environ, "NO_COLOR": "1"},
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stderr


@pytest.fixture(scope="module")
def demo(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("demo")
    warnings = build(DOCS, out)
    assert warnings == "", warnings
    return out


def soup(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def test_static_assets_copied(demo: Path) -> None:
    static = demo / "_static"
    assert (static / "scripts" / "carbon-sphinx.js").is_file()
    assert (static / "styles" / "carbon-sphinx.css").is_file()
    assert (static / "fonts" / "plex.css").is_file()
    assert (static / "fonts" / "IBMPlexSans-Regular.woff2").is_file()


def test_page_structure(demo: Path) -> None:
    page = soup(demo / "kitchen-sink" / "code.html")
    body = page.body
    assert "cds--white" in body["class"]
    assert body["data-light-theme"] == "white"
    assert body["data-dark-theme"] == "g100"
    assert page.find("cds-header") is not None
    assert page.find("cds-side-nav") is not None
    assert page.find("main", id="main-content") is not None
    assert page.select_one("article.carbon-article h1").get_text(strip=True).startswith("Code")
    # Current page is marked in the navigation.
    current = page.select_one("nav.carbon-nav a.current")
    assert current is not None and current.get_text(strip=True) == "Code"
    # Breadcrumbs and pager.
    assert page.select("nav.carbon-breadcrumb .cds--breadcrumb-item")
    assert page.select_one("a.carbon-pager__link--prev") is not None
    # Module script with cache-busting query.
    script = page.find("script", attrs={"type": "module"})
    assert "carbon-sphinx.js?v=" in script["src"]


def test_no_cdn_requests(demo: Path) -> None:
    """Everything is served locally; no third-party URLs in head."""
    page = soup(demo / "index.html")
    for tag in page.head.find_all(["link", "script"]):
        url = tag.get("href") or tag.get("src") or ""
        assert not url.startswith(("http://", "https://", "//")), url


def test_icons_inlined(demo: Path) -> None:
    page = soup(demo / "index.html")
    assert page.select("cds-header-global-action svg")


def test_search_page(demo: Path) -> None:
    page = soup(demo / "search.html")
    field = page.select_one("article .cds--search input[name=q]")
    assert field is not None


def test_options(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "conf.py").write_text(
        "html_theme = 'carbon'\n"
        "html_theme_options = {\n"
        "    'light_theme': 'g10',\n"
        "    'dark_theme': 'g90',\n"
        "    'header_prefix': 'IBM',\n"
        "    'header_links': [{'name': 'Home', 'doc': 'index'}, {'name': 'Ext', 'url': 'https://example.com'}],\n"
        "    'show_toc': False,\n"
        "}\n"
    )
    (src / "index.rst").write_text("Title\n=====\n\nSection\n-------\n\nText.\n")
    warnings = build(src, tmp_path / "out")
    assert warnings == "", warnings
    page = soup(tmp_path / "out" / "index.html")
    assert page.body["data-light-theme"] == "g10"
    assert page.body["data-dark-theme"] == "g90"
    assert page.find("cds-header-name")["prefix"] == "IBM"
    items = page.find_all("cds-header-nav-item")
    assert [i["href"] for i in items] == ["#", "https://example.com"]
    assert page.select_one(".carbon-toc") is None


def test_toc_depth(demo: Path) -> None:
    page = soup(demo / "kitchen-sink" / "api.html")
    toc = page.select_one("aside.carbon-toc")
    assert toc["data-depth"] == "1"
    # Label for assistive technology only.
    assert "carbon-visually-hidden" in toc.select_one("#carbon-toc-title")["class"]


def test_invalid_theme_zone_warns(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "conf.py").write_text(
        "html_theme = 'carbon'\nhtml_theme_options = {'dark_theme': 'purple'}\n"
    )
    (src / "index.rst").write_text("Title\n=====\n")
    warnings = build(src, tmp_path / "out")
    assert "invalid dark_theme 'purple'" in warnings
    page = soup(tmp_path / "out" / "index.html")
    assert page.body["data-dark-theme"] == "g100"

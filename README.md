# sphinx-carbon-theme

A [Sphinx](https://www.sphinx-doc.org/) theme implementing the
[IBM Carbon Design System](https://carbondesignsystem.com/).

```python
# conf.py
html_theme = "carbon"
```

## Design

- **Base theme:** Sphinx's built-in `basic`. Its templates ship with Sphinx
  itself, so they are the most stable thing a theme can build on.
  `layout.html` extends it and only replaces the page body; `<head>` stays
  Sphinx's.
- **Chrome:** Carbon UI shell web components (`@carbon/web-components`:
  `cds-header`, `cds-side-nav`, header actions and panel), bundled with
  esbuild. Only the components used are imported.
- **Content:** `@carbon/styles` compiled with Sass. Theme tokens are emitted
  as CSS custom properties for all four Carbon themes (white, g10, g90,
  g100), so light/dark mode is a class change on `<body>`. Sphinx's HTML is
  mapped onto Carbon tokens and type styles; where Carbon component markup
  fits (search field, breadcrumb, link) the component CSS is used as is.
- **Fonts and icons:** IBM Plex and `@carbon/icons`, copied into the theme at
  build time. Nothing is loaded from a CDN.
- **Navigation:** the Sphinx toctree is rendered as plain nested lists inside
  `cds-side-nav`, so it works at any depth and without JavaScript; JavaScript
  adds expand/collapse buttons.

## Building documentation

Install the released wheel; no Node.js is needed:

```console
pip install sphinx-carbon-theme
```

## Developing the theme

Node.js is needed only to build the theme itself.

```console
npm ci
npm run build          # or: npm run watch
uv venv && uv pip install -e . --group test
nox -s docs            # build the kitchen-sink demo
nox -s docs_live       # live-reloading demo
nox -s tests           # tests against several Sphinx versions
```

The compiled assets (`src/sphinx_carbon_theme/theme/carbon/static/` and
`partials/icons/`) are git-ignored and shipped in the wheel. Building a wheel
runs `npm run build` through a hatch build hook if they are missing.

### CI and releases

`.github/workflows/ci.yml` builds the sdist and wheel once, tests the wheel
against the oldest supported and current Sphinx releases (and Sphinx `main`,
non-blocking), and on a `v*` tag publishes those same files to PyPI.

To release, tag and push; the version comes from the tag:

```console
git tag v0.1.0
git push origin v0.1.0
```

Publishing uses [PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/),
so no API token is stored. One-time setup:

1. On PyPI, add a trusted publisher for project `sphinx-carbon-theme`
   (as a "pending publisher" before the first release): owner `imphil`,
   repository `sphinx-carbon-theme`, workflow `ci.yml`, environment `pypi`.
2. On GitHub, create the environment `pypi` (Settings → Environments).
   Optionally add yourself as a required reviewer so each upload needs a click.

Dependabot (`.github/dependabot.yml`) proposes updates to the Carbon packages,
build tools and the pinned actions.

### Updating Carbon

Bump the `@carbon/*` versions in `package.json`, run `npm install && npm run
build`, then review the kitchen-sink pages in all four themes.

## Licence

Apache-2.0. IBM Plex fonts are under the SIL Open Font License
(`static/fonts/LICENSE-IBM-Plex.txt`).

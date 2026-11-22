"""Development tasks. The theme assets must be built first (``npm run build``)."""

import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["tests"]

# Oldest supported, latest releases, and Sphinx's development branch.
SPHINX_VERSIONS = ["8.0", "8.2", "9.2", "main"]


def _install_sphinx(session: nox.Session, version: str) -> None:
    if version == "main":
        session.install("sphinx @ git+https://github.com/sphinx-doc/sphinx")
    else:
        session.install(f"sphinx=={version}.*")


@nox.session
@nox.parametrize("sphinx", SPHINX_VERSIONS)
def tests(session: nox.Session, sphinx: str) -> None:
    """Build the demo docs and check the output against a Sphinx version."""
    session.install("-e", ".", "--group", "test")
    _install_sphinx(session, sphinx)
    session.run("pytest", *session.posargs)


@nox.session
def docs(session: nox.Session) -> None:
    """Build the kitchen-sink demo into docs/_build/html."""
    session.install("-e", ".")
    # -E: theme/asset changes don't mark pages outdated, so always rebuild all.
    session.run(
        "sphinx-build", "-E", "-W", "--keep-going", "-b", "html", "docs", "docs/_build/html"
    )


@nox.session(name="docs_live")
def docs_live(session: nox.Session) -> None:
    """Serve the demo with live reload (run `npm run watch` alongside)."""
    session.install("-e", ".", "--group", "docs")
    session.run(
        "sphinx-autobuild",
        "--watch",
        "src/sphinx_carbon_theme",
        "docs",
        "docs/_build/html",
    )

"""Hatch build hook: compile the theme's static assets with Node.

Runs when building a wheel or an editable install. If the compiled assets
already exist (for example, they were built in an earlier CI step), Node is
not needed. Set ``CARBON_SPHINX_FORCE_ASSETS=1`` to rebuild anyway.

Users installing a released wheel never run this.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

ROOT = Path(__file__).parent
STATIC = ROOT / "src" / "sphinx_carbon_theme" / "theme" / "carbon" / "static"
REQUIRED = [
    STATIC / "scripts" / "carbon-sphinx.js",
    STATIC / "styles" / "carbon-sphinx.css",
    STATIC / "fonts" / "plex.css",
]


class AssetsBuildHook(BuildHookInterface):
    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict) -> None:
        if self.target_name == "sdist":
            return
        forced = os.environ.get("CARBON_SPHINX_FORCE_ASSETS") == "1"
        if not forced and all(p.is_file() for p in REQUIRED):
            return
        npm = shutil.which("npm")
        if npm is None:
            msg = (
                "Building sphinx-carbon-theme from source needs Node.js/npm to "
                "compile its static assets. Install Node.js, or install a "
                "released wheel instead."
            )
            raise RuntimeError(msg)
        if not (ROOT / "node_modules").is_dir():
            subprocess.run([npm, "ci", "--no-fund", "--no-audit"], cwd=ROOT, check=True)
        subprocess.run([npm, "run", "build"], cwd=ROOT, check=True)

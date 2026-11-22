Usage
=====

Installation
------------

.. code-block:: console

   $ pip install sphinx-carbon-theme

Then set the theme in ``conf.py``:

.. code-block:: python

   html_theme = "carbon"

Options
-------

All options go into ``html_theme_options``.

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Option
     - Default
     - Description
   * - ``light_theme``
     - ``"white"``
     - Carbon theme for light mode: ``white`` or ``g10``.
   * - ``dark_theme``
     - ``"g100"``
     - Carbon theme for dark mode: ``g90`` or ``g100``.
   * - ``header_prefix``
     - ``""``
     - Text shown before the project name in the header.
   * - ``header_links``
     - ``[]``
     - List of ``{"name": ..., "url": ...}`` or ``{"name": ..., "doc": ...}``.
   * - ``repository_url``
     - ``""``
     - Shows a repository link in the header.
   * - ``navigation_collapse``
     - ``False``
     - Only render the current branch of the navigation (for huge sites).
   * - ``navigation_depth``
     - ``-1``
     - Maximum depth of the side navigation.
   * - ``navigation_include_hidden``
     - ``True``
     - Include ``:hidden:`` toctrees in the side navigation.
   * - ``show_toc``
     - ``True``
     - Show the in-page contents column on wide screens.
   * - ``toc_depth``
     - ``1``
     - Heading levels shown in that column: ``1`` (sections only, as on the
       Carbon website), ``2`` or ``3``.
   * - ``show_breadcrumbs``
     - ``True``
     - Show breadcrumbs above the page title.
   * - ``show_prev_next``
     - ``True``
     - Show previous/next links at the bottom of the page.

Example:

.. code-block:: python

   html_theme_options = {
       "light_theme": "g10",
       "header_prefix": "IBM",
       "header_links": [
           {"name": "Guide", "doc": "guide/index"},
           {"name": "Blog", "url": "https://example.com/blog"},
       ],
   }

Light and dark mode
-------------------

The header's theme button cycles through *system*, *light* and *dark*. The
choice is stored in the browser. Without JavaScript the light theme is used.

Carbon Sphinx Theme
===================

A Sphinx theme implementing the `IBM Carbon Design System
<https://carbondesignsystem.com/>`_.

It uses Carbon's own packages: the UI shell web components for the header
and side navigation, and ``@carbon/styles`` design tokens, type scale and
component styles for the page content. Assets are compiled when the theme is
released, so building documentation needs nothing but Python.

.. code-block:: python

   # conf.py
   html_theme = "carbon"

.. toctree::
   :maxdepth: 2
   :caption: Using the theme

   usage

.. toctree::
   :maxdepth: 2
   :caption: Examples

   kitchen-sink/index

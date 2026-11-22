Code
====

Python
------

.. code-block:: python
   :caption: example.py
   :emphasize-lines: 3

   import dataclasses

   @dataclasses.dataclass
   class Point:
       """A point in 2D space."""

       x: float = 0.0
       y: float = 0.0

       def distance(self, other: "Point") -> float:
           # Euclidean distance
           return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

With line numbers:

.. code-block:: javascript
   :linenos:

   const greet = (name) => `Hello, ${name}!`;
   console.log(greet("Carbon"));

Console session:

.. code-block:: console

   $ pip install sphinx-carbon-theme
   Successfully installed sphinx-carbon-theme-0.1.0

Python interactive session:

>>> 1 + 1
2

A literal block::

   Plain literal text, no highlighting.

A very long line to check horizontal scrolling:

.. code-block:: text

   0123456789 0123456789 0123456789 0123456789 0123456789 0123456789 0123456789 0123456789 0123456789 0123456789

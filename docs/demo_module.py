"""A demo module for the API reference page."""

from __future__ import annotations

from dataclasses import dataclass

#: The default number of sides.
DEFAULT_SIDES = 4


@dataclass
class Shape:
    """A geometric shape.

    :param name: Human-readable name.
    :param sides: Number of sides.

    .. versionadded:: 0.1
    """

    name: str
    sides: int = DEFAULT_SIDES

    def describe(self, *, verbose: bool = False) -> str:
        """Return a description of the shape.

        Args:
            verbose: Include the number of sides.

        Returns:
            The description.

        Raises:
            ValueError: If the shape has no sides.
        """
        if self.sides <= 0:
            raise ValueError("a shape needs sides")
        return f"{self.name} ({self.sides} sides)" if verbose else self.name

    @property
    def is_polygon(self) -> bool:
        """Whether the shape is a polygon."""
        return self.sides >= 3


def area(width: float, height: float = 1.0) -> float:
    """Compute the area of a rectangle.

    :param width: The width.
    :param height: The height.
    :returns: ``width * height``.

    .. deprecated:: 0.2
       Use :meth:`Shape.describe` instead.
    """
    return width * height

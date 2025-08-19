from enum import Enum
from math import *


# ------------------------------------------------------
# Factory Method Pattern - Explained with Point class
# ------------------------------------------------------

# PROBLEM:
# Without factory methods, the constructor (__init__) has to handle
# multiple coordinate systems (Cartesian, Polar, etc.).
# This makes object creation:
#   - Confusing: Are the parameters (x, y) or (rho, theta)?
#   - Error-prone: Users must remember conversion math for Polar.
#   - Hard to extend: Adding new systems means modifying __init__.
#
# SOLUTION:
# Factory methods provide named methods that clearly express
# how an object should be created (Cartesian vs Polar).
# This makes code readable, safe, and easier to extend.


# Enum to define different coordinate systems
class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2


class Point:
    """
    Point class that can represent a point either in
    Cartesian coordinates (x, y) or in Polar coordinates (rho, theta).
    """

    def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
        if system == CoordinateSystem.CARTESIAN:
            # Cartesian: store values directly
            self.x = a
            self.y = b
        elif system == CoordinateSystem.POLAR:
            # Polar: convert (rho, theta) to Cartesian (x, y)
            self.x = a * cos(b)
            self.y = a * sin(b)

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

    # --------------------------------------------------
    # FACTORY METHODS
    # --------------------------------------------------

    @staticmethod
    def new_cartesian_point(x, y):
        """
        Factory method for Cartesian coordinates.
        Clearly shows that (x, y) are used directly.
        """
        return Point(x, y, CoordinateSystem.CARTESIAN)

    @staticmethod
    def new_polar_point(rho, theta):
        """
        Factory method for Polar coordinates.
        Handles the conversion internally so the caller
        doesn’t need to remember conversion formulas.
        """
        return Point(rho, theta, CoordinateSystem.POLAR)


# ------------------------------------------------------
# DEMONSTRATION
# ------------------------------------------------------
if __name__ == "__main__":
    # Without factory methods:
    # You need to pass the system explicitly,
    # which can be confusing for users.
    p1 = Point(2, 3, CoordinateSystem.CARTESIAN)

    # With factory methods:
    # Code is clearer and intent is obvious.
    p2 = Point.new_cartesian_point(3, 4)
    p3 = Point.new_polar_point(5, 1.57)  # rho=5, theta≈90°

    print(p1, p2, p3)


# ------------------------------------------------------
# SIGNIFICANCE OF FACTORY METHODS
# ------------------------------------------------------
# - Provide clarity: Creation intent is explicit (Cartesian vs Polar).
# - Reduce mistakes: Users don’t deal with conversion formulas.
# - Improve maintainability: __init__ stays simple, new systems
#   can be added through new factory methods instead of changing it.
# - Follow good design practice: Separate "how to create"
#   from "how to use".

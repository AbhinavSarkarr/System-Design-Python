from enum import Enum
from math import *


# ------------------------------------------------------
# FACTORY METHOD PATTERN - FULL GUIDE WITH POSSIBILITIES
# ------------------------------------------------------
# PROBLEM:
#   A Point can be defined either in Cartesian coordinates (x, y)
#   or in Polar coordinates (rho, theta).
#
#   If we only use __init__, it becomes:
#     - Confusing: are (a, b) = (x, y) or (rho, theta)?
#     - Error-prone: user has to remember conversion formulas.
#     - Rigid: if a new system is added, __init__ must be changed.
#
# SOLUTION:
#   Factory Methods provide clear, well-named ways of creating Points.
#   Instead of remembering conversions, we call descriptive methods:
#       Point.new_cartesian_point(x, y)
#       Point.new_polar_point(rho, theta)
#
#   This guide shows ALL the common ways to organize factory methods.


class CoordinateSystem(Enum):
    CARTESIAN = 1
    POLAR = 2


class Point:
    """
    A point in 2D space.
    Can be initialized using Cartesian or Polar coordinates.
    """

    def __init__(self, a, b, system=CoordinateSystem.CARTESIAN):
        if system == CoordinateSystem.CARTESIAN:
            self.x = a
            self.y = b
        elif system == CoordinateSystem.POLAR:
            self.x = a * cos(b)
            self.y = a * sin(b)

        # If we add a new system, we would have to change __init__
        # → violates Open/Closed Principle.
        # Factory methods solve this problem.

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

    # --------------------------------------------------
    # 1. FACTORY METHODS defined directly inside the class
    # --------------------------------------------------
    @staticmethod
    def new_cartesian_point(x, y):
        # Creates a point directly in Cartesian coordinates
        return Point(x, y, CoordinateSystem.CARTESIAN)

    @staticmethod
    def new_polar_point(rho, theta):
        # Creates a point from Polar coordinates
        return Point(rho, theta, CoordinateSystem.POLAR)

    # --------------------------------------------------
    # 2. NESTED FACTORY CLASS
    # --------------------------------------------------
    # Another way is to place all factory methods inside a
    # nested "Factory" class. This groups creation logic together.
    class Factory:
        @staticmethod
        def new_cartesian_point(x, y):
            return Point(x, y, CoordinateSystem.CARTESIAN)

        @staticmethod
        def new_polar_point(rho, theta):
            return Point(rho, theta, CoordinateSystem.POLAR)

    # --------------------------------------------------
    # 3. FACTORY INSTANCE (exposed as an attribute)
    # --------------------------------------------------
    # Instead of calling Point.Factory, we can expose
    # an instance of the factory for convenience:
    factory = Factory()


# ------------------------------------------------------
# 4. SEPARATE FACTORY CLASS
# ------------------------------------------------------
# Some prefer to keep factory methods completely outside the class.
# This way, the creation logic is entirely decoupled from Point.
class PointFactory:
    @staticmethod
    def new_cartesian_point(x, y):
        return Point(x, y, CoordinateSystem.CARTESIAN)

    @staticmethod
    def new_polar_point(rho, theta):
        return Point(rho, theta, CoordinateSystem.POLAR)


# ------------------------------------------------------
# DEMONSTRATION OF ALL FACTORY POSSIBILITIES
# ------------------------------------------------------
if __name__ == "__main__":
    # (A) Direct constructor (works, but unclear)
    p1 = Point(2, 3, CoordinateSystem.CARTESIAN)

    # (B) Using factory methods inside the class
    p2 = Point.new_cartesian_point(1, 2)
    p3 = Point.new_polar_point(5, 1.57)

    # (C) Using the nested Factory class
    p4 = Point.Factory.new_cartesian_point(3, 4)
    p5 = Point.Factory.new_polar_point(5, 1.57)

    # (D) Using the exposed factory instance
    p6 = Point.factory.new_cartesian_point(7, 8)

    # (E) Using the completely separate PointFactory class
    p7 = PointFactory.new_cartesian_point(9, 10)
    p8 = PointFactory.new_polar_point(6, 1.57)

    print("Constructor:   ", p1)
    print("Factory Method:", p2, p3)
    print("Nested Factory:", p4, p5)
    print("Factory Attr:  ", p6)
    print("Separate Class:", p7, p8)


# ------------------------------------------------------
# SUMMARY OF POSSIBILITIES
# ------------------------------------------------------
# 1. Factory methods inside the class
#    - Simple and convenient.
#    - Keeps creation logic close to the class itself.
#
# 2. Nested Factory class (Point.Factory)
#    - Groups all factory methods together in one place.
#    - Useful when there are many factory methods.
#
# 3. Exposed factory instance (Point.factory)
#    - Cleaner usage syntax (Point.factory.new_cartesian_point()).
#
# 4. Separate factory class (PointFactory)
#    - Decouples object creation from the class definition.
#    - Useful when factories become very large or shared across modules.
#
# Each approach has trade-offs, but they all serve the same purpose:
# Making object creation clear, safe, and extensible.

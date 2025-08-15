#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Liskov Substitution Principle (LSP) 

Definition:
    If S is a subtype of T, then you should be able to use an object of S
    wherever an object of T is expected — WITHOUT breaking the program.

Why it matters:
    - Lets us use polymorphism safely.
    - Prevents “surprise” behavior in subclasses.
    - Keeps hierarchies predictable and testable.

Classic pitfall:
    Making `Square` inherit from `Rectangle`. Mathematically a square is a
    rectangle, but in code a rectangle often *expects* width and height to be
    independent. A square can’t honor that expectation, so substituting Square
    where Rectangle is expected breaks behavior ⇒ LSP violation.

This file contains:
    1) A VIOLATION demo (Rectangle/Square with width/height setters).
    2) A CORRECT design #1: Use a common interface (Shape) and keep classes
       independent (no wrong inheritance).
    3) A CORRECT design #2: Model capabilities explicitly (advanced note).
    4) Runnable demos with clear PASS/FAIL output.

"""

from abc import ABC, abstractmethod

# =============================================================================
# 1) LSP VIOLATION — Rectangle <- Square
# =============================================================================
class Rectangle:
    """
    Rectangle with independently settable width and height.

    Contract (what callers reasonably expect):
        - width and height can be set independently.
        - setting height does NOT change width (and vice versa).
    """

    def __init__(self, width: int, height: int):
        self._width = int(width)
        self._height = int(height)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = int(value)

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = int(value)

    @property
    def area(self) -> int:
        return self._width * self._height

    def __repr__(self) -> str:
        return f"Rectangle(width={self._width}, height={self._height})" 


class Square(Rectangle):
    """
    Square that inherits from Rectangle.

    To keep all sides equal, we OVERRIDE the setters so setting *either*
    dimension changes BOTH dimensions.

    This BREAKS the Rectangle contract/expectation:
        - Callers of Rectangle think width and height are independent.
        - With Square, they're NOT independent anymore.
    """

    def __init__(self, size: int):
        super().__init__(size, size)

    @Rectangle.width.setter
    def width(self, value: int) -> None:
        v = int(value)
        self._width = v
        self._height = v  # ← coupling added here

    @Rectangle.height.setter
    def height(self, value: int) -> None:
        v = int(value)
        self._height = v
        self._width = v  # ← coupling added here


def use_rectangle(rc: Rectangle) -> None:
    """
    A function that expects a 'rectangle-like' object:
        - Reads the current width.
        - Sets the height to 10.
        - Expects width to stay the same.
        - Therefore expects area == (original_width * 10).

    If we pass a Square (subclass of Rectangle), this assumption fails,
    demonstrating an LSP violation.
    """
    original_width = rc.width
    rc.height = 10
    expected_area = original_width * 10
    actual_area = rc.area
    status = "PASS" if actual_area == expected_area else "FAIL (LSP violated)"
    print(
        f"[use_rectangle] rc={rc} | expected_area={expected_area} | "
        f"actual_area={actual_area} → {status}"
    )


# =============================================================================
# 2) CORRECT DESIGN #1 — Common Interface (Shape), No Wrong Inheritance
# =============================================================================
class Shape(ABC):
    """
    A minimal interface for shapes.
    We expose only what all shapes can *honestly* guarantee.

    Note:
        - There is NO 'set_width'/'set_height' here, because NOT ALL SHAPES
          support independent dimension changes. (Squares can't.)
        - Keeping the interface small prevents promising behavior that a
          subclass can't deliver.
    """

    @property
    @abstractmethod
    def area(self) -> int:
        """Return area of the shape."""
        raise NotImplementedError
 

class RectangleOK(Shape):
    """A rectangle that stands on its own (not a base for Square)."""

    def __init__(self, width: int, height: int):
        self._width = int(width)
        self._height = int(height)

    @property
    def area(self) -> int:
        return self._width * self._height

    def resize(self, *, width: int | None = None, height: int | None = None) -> None:
        """
        Optional capability for rectangles: independently resize each side.
        This method is specific to RectangleOK; it's NOT promised by Shape.
        """
        if width is not None:
            self._width = int(width)
        if height is not None:
            self._height = int(height)

    def __repr__(self) -> str:
        return f"RectangleOK(width={self._width}, height={self._height})"


class SquareOK(Shape):
    """A square with a single side length."""

    def __init__(self, side: int):
        self._side = int(side)

    @property
    def area(self) -> int:
        return self._side * self._side

    def set_side(self, side: int) -> None:
        """Squares resize by changing a single side value."""
        self._side = int(side)

    def __repr__(self) -> str:
        return f"SquareOK(side={self._side})"


def use_shape(shape: Shape) -> None:
    """
    A function that works with ANY Shape.
    It only relies on the *shared* contract: we can read .area.

    Because the contract is small and honest, both RectangleOK and SquareOK
    can be substituted here safely → LSP satisfied.
    """
    print(f"[use_shape] shape={shape} | area={shape.area} → PASS")


# =============================================================================
# 3) CORRECT DESIGN #2 — Model Capabilities Explicitly (Advanced Note)
# =============================================================================
# In some designs you may want to express "resizable in two independent
# dimensions" as a *separate capability* from just "I am a shape".
#
# In statically typed languages, you'd model this with interfaces.
# In Python, you could document it or use typing.Protocol for static tools.
#
# For runtime demo simplicity, we’ll just keep the idea in comments.
#
# Key takeaway:
#   - Only promise behaviors that all subtypes can *guarantee*.
#   - Use extra methods/capabilities on specific classes rather than forcing
#     them into a base type they can’t honestly implement.


# =============================================================================
# 4) DEMOS
# =============================================================================
def demo_violation() -> None:
    print("\n=== DEMO: LSP VIOLATION (Rectangle <- Square) ===")
    rc = Rectangle(2, 3)
    use_rectangle(rc)  # Expected OK

    sq = Square(5)
    use_rectangle(sq)  # Will FAIL because setting height changes width too


def demo_correct_design() -> None:
    print("\n=== DEMO: CORRECT DESIGN (Common Shape interface) ===")
    r = RectangleOK(4, 5)
    s = SquareOK(4)

    use_shape(r)  # OK
    use_shape(s)  # OK

    # Show rectangle's optional capability (not part of Shape contract)
    print("[extra] resizing RectangleOK independently (not promised by Shape)...")
    r.resize(width=10, height=2)
    use_shape(r)  # Still OK; we only rely on area in use_shape

    # Show square's way to resize
    print("[extra] resizing SquareOK by side (its honest capability)...")
    s.set_side(10)
    use_shape(s)


def main() -> None:
    print("Liskov Substitution Principle (LSP) — Runnable Examples")
    print("------------------------------------------------------")
    print("Rule of thumb:\n"
          "  Subclasses must honor the expectations/contracts of their base class.\n"
          "  Don’t inherit if you can’t keep the promises.\n")
    demo_violation()
    demo_correct_design()

    print("\nCheat Sheet:")
    print("  • Don’t make Square inherit Rectangle if Rectangle promises independent width/height.")
    print("  • Prefer small, honest base interfaces (e.g., Shape with .area).")
    print("  • Add extra capabilities on specific classes instead of forcing them into the base.")
    print("  • LSP heuristics:")
    print("      - Subclasses must not strengthen preconditions.")
    print("      - Subclasses must not weaken postconditions.")
    print("      - Subclasses must preserve class invariants.")


if __name__ == "__main__":
    main()

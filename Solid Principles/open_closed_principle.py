"""
Example: Open/Closed Principle (OCP) with the Specification Design Pattern

Open/Closed Principle says:
    "A class should be open for extension, but closed for modification."

What does that mean?
    - We should be able to add new features (extend behavior) without changing the existing, tested code.
    - This avoids breaking existing functionality when requirements change.

We will demonstrate this with a product filtering example.
We’ll filter products by color, size, or a combination of both — 
without having to rewrite the filtering code every time a new filter type is added.
"""

from enum import Enum


# ==============================
# STEP 1: ENUMS FOR FIXED VALUES
# ==============================
class Color(Enum):
    """Represents available colors for products."""
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    """Represents available sizes for products."""
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


# ==============================
# STEP 2: PRODUCT CLASS
# ==============================
class Product:
    """
    Represents a product with a name, color, and size.
    Example:
        Product("Apple", Color.RED, Size.SMALL)
    """

    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size


# ============================================
# STEP 3: SPECIFICATION (THE HEART OF THE OCP)
# ============================================
class Specification:
    """
    Base class for all specifications (criteria).
    Think of a specification as a "rule" or "condition"
    that an item must satisfy to be selected.
    """

    def is_satisfied(self, item):
        """
        Checks if the given item meets the condition.
        Must be overridden by child classes.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def __and__(self, other):
        """
        Enables combining two specifications using the '&' operator.
        Example:
            large_blue_spec = LargeSpecification(Size.LARGE) & ColorSpecification(Color.BLUE)
        This returns an AndSpecification instance.
        """
        return AndSpecification(self, other)


# =======================================
# STEP 4: FILTER BASE CLASS (ABSTRACTION)
# =======================================
class Filter:
    """
    Base filter class — defines the structure for filtering
    but does not implement the logic itself.
    """

    def filter(self, items, spec):
        """
        Filters items based on a given specification.
        Must be overridden by child classes.
        """
        raise NotImplementedError("Subclasses must override this method.")


# ==================================================
# STEP 5: SPECIFICATION IMPLEMENTATIONS (EXTENSIONS)
# ==================================================
class ColorSpecification(Specification):
    """Filters items by a specific color."""

    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color


class SizeSpecification(Specification):
    """Filters items by a specific size."""

    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size


class AndSpecification(Specification):
    """
    Combines multiple specifications and checks if ALL are satisfied.
    This is how we support multiple filtering conditions without changing existing code.
    """

    def __init__(self, *specifications):
        self.specifications = specifications

    def is_satisfied(self, item):
        return all(spec.is_satisfied(item) for spec in self.specifications)


# =======================================
# STEP 6: FILTER IMPLEMENTATION (EXTENDED)
# =======================================
class ProductFilter(Filter):
    """
    A concrete filter that applies any specification to a list of products.
    """

    def filter(self, items, spec):
        """
        Goes through all items and yields only those that satisfy the specification.
        """
        for item in items:
            if spec.is_satisfied(item):
                yield item


# =========================
# STEP 7: DEMONSTRATION
# =========================
if __name__ == "__main__":
    # Create some sample products
    apple = Product("Apple", Color.RED, Size.SMALL)
    tree = Product("Tree", Color.GREEN, Size.LARGE)
    room = Product("Room", Color.BLUE, Size.LARGE)

    products = [apple, tree, room]

    # Create a filter instance
    product_filter = ProductFilter()

    print("=== Filter by Color (GREEN) ===")
    green_spec = ColorSpecification(Color.GREEN)
    for p in product_filter.filter(products, green_spec):
        print(f"{p.name} is green.")

    print("\n=== Filter by Size (LARGE) ===")
    large_spec = SizeSpecification(Size.LARGE)
    for p in product_filter.filter(products, large_spec):
        print(f"{p.name} is large.")

    print("\n=== Filter by Size (LARGE) AND Color (BLUE) ===")
    large_blue_spec = large_spec & ColorSpecification(Color.BLUE)
    for p in product_filter.filter(products, large_blue_spec):
        print(f"{p.name} is large and blue.")

"""
Key Takeaways:
1. Without OCP:
    - We would have to keep adding new filter methods like filter_by_color, filter_by_size, etc., in the ProductFilter class.
    - Every time we add a new filtering requirement, we’d modify the existing filter code (risk of breaking old code).

2. With OCP + Specification Pattern:
    - We never touch the existing ProductFilter code.
    - We just create new Specification classes.
    - The filtering mechanism automatically works with any new specification.

3. Benefits:
    - Code is easier to maintain.
    - No risk of breaking tested code when adding features.
    - Very flexible — we can combine conditions easily.
"""

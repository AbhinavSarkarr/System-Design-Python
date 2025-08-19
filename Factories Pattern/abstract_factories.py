from abc import ABC
from enum import Enum, auto


# ------------------------------------------------------
# ABSTRACT FACTORY PATTERN - EXAMPLE WITH HOT DRINKS
# ------------------------------------------------------
# PROBLEM:
#   We want to create different types of hot drinks (Tea, Coffee).
#   Each drink has its own preparation steps.
#
#   If we hardcode "if drink == tea → prepare tea" everywhere,
#   the code becomes messy and violates OCP (Open/Closed Principle).
#
# SOLUTION:
#   Abstract Factory separates *object creation* (how drinks
#   are prepared) from *object use* (drinking).
#   - HotDrink defines the interface for drinks.
#   - Each HotDrinkFactory knows how to prepare a specific drink.
#   - HotDrinkMachine chooses the right factory at runtime.
#
#   This way, we can add new drinks by creating new factories
#   without changing core logic.


# ------------------------------------------------------
# Abstract Product
# ------------------------------------------------------
class HotDrink(ABC):
    def consume(self):
        pass


# Concrete Products
class Tea(HotDrink):
    def consume(self):
        print("This tea is nice but I'd prefer it with milk")


class Coffee(HotDrink):
    def consume(self):
        print("This coffee is delicious")


# ------------------------------------------------------
# Abstract Factory
# ------------------------------------------------------
class HotDrinkFactory(ABC):
    def prepare(self, amount):
        pass


# Concrete Factories
class TeaFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f"Put in tea bag, boil water, pour {amount}ml, enjoy!")
        return Tea()


class CoffeeFactory(HotDrinkFactory):
    def prepare(self, amount):
        print(f"Grind some beans, boil water, pour {amount}ml, enjoy!")
        return Coffee()


# ------------------------------------------------------
# HotDrinkMachine - uses factories
# ------------------------------------------------------
class HotDrinkMachine:
    # Enum of available drinks (NOTE: violates OCP,
    # because adding a new drink means modifying this enum)
    class AvailableDrink(Enum):
        COFFEE = auto()
        TEA = auto()

    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            # Dynamically create factory instances based on enum
            for d in self.AvailableDrink:
                # Example: COFFEE → "CoffeeFactory"
                name = d.name[0] + d.name[1:].lower()
                factory_name = name + "Factory"
                factory_instance = eval(factory_name)()
                self.factories.append((name, factory_instance))

    def make_drink(self):
        print("Available drinks:")
        for idx, f in enumerate(self.factories):
            print(f"{idx}: {f[0]}")

        s = input(f"Please pick drink (0-{len(self.factories)-1}): ")
        idx = int(s)
        s = input("Specify amount (ml): ")
        amount = int(s)
        return self.factories[idx][1].prepare(amount)


# ------------------------------------------------------
# Simple Factory (alternative quick approach)
# ------------------------------------------------------
# This is NOT abstract factory. It's just a simple factory
# function that hardcodes which factory to use.
def make_drink(type):
    if type == "tea":
        return TeaFactory().prepare(200)
    elif type == "coffee":
        return CoffeeFactory().prepare(50)
    else:
        return None


# ------------------------------------------------------
# DEMONSTRATION
# ------------------------------------------------------
if __name__ == "__main__":
    # Option A: Simple Factory (direct choice)
    # entry = input("What kind of drink would you like? ")
    # drink = make_drink(entry)
    # drink.consume()

    # Option B: Abstract Factory via HotDrinkMachine
    hdm = HotDrinkMachine()
    drink = hdm.make_drink()
    drink.consume()


# ------------------------------------------------------
# SIGNIFICANCE OF ABSTRACT FACTORY
# ------------------------------------------------------
# - Provides an interface for creating families of related objects.
#   (TeaFactory → Tea, CoffeeFactory → Coffee)
# - Keeps creation logic separate from business logic.
# - Makes it easier to extend: new drink = new factory.
# - Promotes consistency: factory guarantees correct product creation.
#
# TRADE-OFF:
# - The given implementation still has an OCP violation:
#   "AvailableDrink" enum must be updated when adding new drinks.
#   A more flexible design could use reflection, plugins, or
#   configuration files instead of hardcoding the enum.

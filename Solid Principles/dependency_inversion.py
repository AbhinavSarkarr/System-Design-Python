"""
Dependency Inversion Principle (DIP)

DIP states:
High-level modules should not depend on low-level modules.
Both should depend on abstractions.

This example first demonstrates the *problem* of tight coupling 
between high-level and low-level modules, and then shows the 
*solution* using abstractions.
"""

from enum import Enum
from abc import ABC, abstractmethod


# --------------------------
# PROBLEM: Tight Coupling
# --------------------------

class RelationshipType(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2

class Person:
    def __init__(self, name):
        self.name = name

# Low-level module (stores relationships)
class Relationship:
    def __init__(self):
        self.relations = []

    def add_parent_child(self, parent, child):
        self.relations.append((parent, child, RelationshipType.PARENT))
        self.relations.append((child, parent, RelationshipType.CHILD))

# High-level module (directly depends on low-level details)
class Research:
    def __init__(self, relationship: Relationship):
        # Accessing the low-level internal data structure directly
        for r in relationship.relations:
            if r[0].name == "John" and r[2] == RelationshipType.PARENT:
                print(f"{r[0].name} is a parent of {r[1].name}")

print("=== Problem: Tight coupling ===")
parent = Person("John")
child1 = Person("Jane")
child2 = Person("Doe")

relationship = Relationship()
relationship.add_parent_child(parent, child1)
relationship.add_parent_child(parent, child2)

research = Research(relationship)
print()


# --------------------------
# SOLUTION: Depend on Abstractions
# --------------------------

# Abstraction for browsing relationships
class RelationshipBrowser(ABC):
    @abstractmethod
    def find_all_children_of(self, name):
        pass

# Low-level module implementing the abstraction
class RelationshipV2(RelationshipBrowser):
    def __init__(self):
        self.relations = []

    def add_parent_child(self, parent, child):
        self.relations.append((parent, child, RelationshipType.PARENT))
        self.relations.append((child, parent, RelationshipType.CHILD))

    def find_all_children_of(self, name):
        return [r[1] for r in self.relations
                if r[0].name == name and r[2] == RelationshipType.PARENT]

# High-level module depending on the abstraction
class ResearchV2:
    def __init__(self, browser: RelationshipBrowser):
        for child in browser.find_all_children_of("John"):
            print(f"John is a parent of {child.name}")

print("=== Solution: Using abstractions ===")
parent = Person("John")
child1 = Person("Jane")
child2 = Person("Doe")

relationship_v2 = RelationshipV2()
relationship_v2.add_parent_child(parent, child1)
relationship_v2.add_parent_child(parent, child2)

research_v2 = ResearchV2(relationship_v2)


# --------------------------
# Explanation
# --------------------------

# All the implementation above works, but the first version has a serious problem:
# It is tightly coupled with the low-level module.
#
# If we want to change the way we store relationships, we will have to change the 
# high-level module as well.
#
# This happens because the high-level module is directly accessing the internal 
# storage mechanism of the low-level module.
#
# --------------------------
# How to tackle this situation?
# --------------------------
#
# First, we define an interface (or abstract base class) for the low-level module.
#
# The idea is that Research should not depend on the concrete implementation 
# of Relationships, but instead on an abstraction that can be swapped out later.
#
# --------------------------
# Dependency Inversion Principle
# --------------------------
#
# The DIP is different from Dependency Injection.
#
# DIP states that high-level classes or modules should not directly depend on
# low-level modules — they should depend on **abstractions**.
#
# In Python, these abstractions are typically abstract base classes 
# or classes with abstract methods.
#
# In short: you should depend on interfaces rather than concrete implementations.
# This way, you can swap one implementation for another without affecting the high-level logic.
#
# The second example demonstrates this:
# - RelationshipBrowser is the abstraction
# - RelationshipV2 implements it
# - ResearchV2 depends only on the abstraction

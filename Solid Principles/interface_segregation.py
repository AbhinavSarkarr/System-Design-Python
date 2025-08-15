"""
Interface Segregation Principle (ISP)

The Interface Segregation Principle states that no client should be forced to depend 
on methods it does not use. 

In other words, instead of creating large, monolithic interfaces 
with many methods, create smaller, more specific interfaces that are easier to implement.

This example first demonstrates the *problem* with large interfaces, and then 
shows the *solution* using smaller, granular interfaces.
"""

from abc import ABC, abstractmethod


# ====================================================
# 1. PROBLEM: Large interface forcing unwanted methods
# ====================================================

class Machine(ABC):
    """A large interface with methods for print, fax, and scan."""

    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def fax(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass


class MultiFunctionPrinter(Machine):
    """
    A modern printer that can print, fax, and scan.
    This class can implement all the methods without issue.
    """
    def print(self, document):
        print(f"Printing: {document}")

    def fax(self, document):
        print(f"Faxing: {document}")

    def scan(self, document):
        print(f"Scanning: {document}")


class OldFashionedPrinter(Machine):
    """
    An old-fashioned printer that can only print.
    The Machine interface forces it to implement fax() and scan(), 
    even though those operations are not supported.
    """
    def print(self, document):
        print(f"Printing (old-fashioned): {document}")

    def fax(self, document):
        raise NotImplementedError("Fax not supported.")

    def scan(self, document):
        raise NotImplementedError("Scan not supported.")


# PROBLEM: 
# OldFashionedPrinter now has to provide implementations for fax() and scan(),
# even though it can't actually perform those actions. 
# This violates the Interface Segregation Principle.


# ===========================================
# 2. SOLUTION: Granular, specific interfaces
# ===========================================

class Printer(ABC):
    """Interface for printing capability."""
    @abstractmethod
    def print(self, document):
        pass


class Scanner(ABC):
    """Interface for scanning capability."""
    @abstractmethod
    def scan(self, document):
        pass


class Fax(ABC):
    """Interface for faxing capability."""
    @abstractmethod
    def fax(self, document):
        pass


class MyPrinter(Printer):
    """A simple printer that only implements printing."""
    def print(self, document):
        print(f"Printing: {document}")


class Photocopier(Printer, Scanner):
    """A device that can both print and scan."""
    def print(self, document):
        print(f"Photocopier printing: {document}")

    def scan(self, document):
        print(f"Photocopier scanning: {document}")


class FaxMachine(Fax):
    """A device that only faxes documents."""
    def fax(self, document):
        print(f"Faxing: {document}")


# ==================
# 3. DEMONSTRATION
# ==================
if __name__ == "__main__":
    # Large interface example (problematic)
    print("=== Problem: Large Interface ===")
    modern_printer = MultiFunctionPrinter()
    modern_printer.print("Report.pdf")
    modern_printer.scan("Report.pdf")

    old_printer = OldFashionedPrinter()
    old_printer.print("Invoice.docx")
    try:
        old_printer.scan("Invoice.docx")  # This will raise NotImplementedError
    except NotImplementedError as e:
        print(f"Error: {e}")

    # Granular interfaces example (solution)
    print("\n=== Solution: Granular Interfaces ===")
    simple_printer = MyPrinter()
    simple_printer.print("Notes.txt")

    copier = Photocopier()
    copier.print("Document1.pdf")
    copier.scan("Document1.pdf")

    fax_machine = FaxMachine()
    fax_machine.fax("Letter.docx")

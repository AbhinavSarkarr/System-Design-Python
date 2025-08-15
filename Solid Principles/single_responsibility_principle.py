"""
Example: Single Responsibility Principle (SRP)

The SRP says:
    "A class should have only one reason to change."

In simpler words:
    - A class should do only ONE thing.
    - That one thing should be its sole responsibility.
    - If it needs to change, it should only be because its primary job changes.

We will demonstrate:
1. A Journal class that *follows* SRP (only manages journal entries).
2. How adding extra responsibilities *violates* SRP.
3. How to fix it using a separate PersistenceManager class.
4. How SRP helps avoid the "God Object" anti-pattern.
"""


# ======================================
# STEP 1: Journal Class (SRP Compliant)
# ======================================
class Journal:
    """
    Represents a personal journal.

    Responsibilities:
    - Store entries.
    - Add entries.
    - Remove entries.
    - Reindex entries after changes.
    """

    def __init__(self):
        self.entries = []  # Holds all journal entries as strings
        self.count = 0     # Keeps track of entry numbering

    def add_entry(self, thought):
        """
        Adds a new journal entry with an auto-incremented number.
        Example:
            1: I ate Poha today.
        """
        self.count += 1
        self.entries.append(f"{self.count}: {thought}")
        self._reindex()

    def remove_entry(self, index):
        """
        Removes an entry by its list index (0-based).
        """
        del self.entries[index]
        self._reindex()

    def _reindex(self):
        """
        Helper method (not intended to be called externally).
        Re-numbers entries after every change so numbering is always sequential.
        """
        self.entries = [
            f"{i+1}: {t if ':' not in t else t.split(': ', 1)[-1]}"
            for i, t in enumerate(self.entries)
        ]

    def __str__(self):
        """
        Returns the journal as a single string (each entry on a new line).
        """
        return '\n'.join(self.entries)


# ===========================================
# STEP 2: SRP Violation — Adding Persistence
# ===========================================
class JournalWithPersistence:
    """
    This version *violates SRP* because it does TWO jobs:
        1. Manage journal entries (business logic).
        2. Handle persistence (saving/loading to/from files/web).
    """

    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, thought):
        self.count += 1
        self.entries.append(f"{self.count}: {thought}")
        self._reindex()

    def remove_entry(self, index):
        del self.entries[index]
        self._reindex()

    def _reindex(self):
        self.entries = [
            f"{i+1}: {t if ':' not in t else t.split(': ', 1)[-1]}"
            for i, t in enumerate(self.entries)
        ]

    def __str__(self):
        return '\n'.join(self.entries)

    # SRP Violation: These belong to a separate class!
    def save(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self))

    def load(self, filename):
        pass  # Not implemented yet

    def load_from_web(self, uri):
        pass  # Not implemented yet


# =========================================
# STEP 3: SRP Fix — Separate Persistence
# =========================================
class PersistenceManager:
    """
    Handles persistence for objects (saving/loading data).

    Responsibilities:
    - Save an object to a file.
    - Load from a file.
    """

    @staticmethod
    def save_to_file(journal, filename):
        """
        Saves the journal object to a file.
        Relies on the journal's __str__ method.
        """
        with open(filename, 'w') as file:
            file.write(str(journal))

    @staticmethod
    def load_from_file(file_path):
        """
        Loads and returns raw data from a file.
        """
        with open(file_path, 'r') as file:
            return file.read()


# ======================================
# STEP 4: Demonstration
# ======================================
if __name__ == "__main__":
    # Create a new journal
    my_journal = Journal()
    my_journal.add_entry("I ate Poha today, it was very yummy.")
    my_journal.add_entry("Now I am learning System Design at the office.")
    my_journal.add_entry("I think I need to revise my OOP concepts.")

    # Remove the second entry (index 1)
    my_journal.remove_entry(1)

    print("=== Current Journal Entries ===")
    print(my_journal)

    # Save journal to file using PersistenceManager
    file_path = "journal.txt"
    PersistenceManager.save_to_file(my_journal, file_path)

    # Load file contents back
    loaded_data = PersistenceManager.load_from_file(file_path)
    print("\n=== Loaded from file ===")
    print(loaded_data)


"""
=======================
Why SRP Matters
=======================
- Without SRP:
    Journal class manages both entries and persistence.
    If we change how we store entries OR how we save to files,
    we have TWO reasons to modify the same class — violating SRP.

- With SRP:
    Journal only changes if entry-handling rules change.
    PersistenceManager only changes if saving/loading logic changes.

=======================
God Object Anti-Pattern
=======================
- A God Object is a single massive class that does EVERYTHING.
- It becomes too large, hard to maintain, and risky to change.
- SRP prevents this by forcing us to split responsibilities logically.

=======================
Key Takeaway:
=======================
SRP enforces that a class should have one reason to change,
making our code modular, maintainable, and easier to test.
"""

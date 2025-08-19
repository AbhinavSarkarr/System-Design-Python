
---

# Design Patterns (Gamma Categorization)

Design Patterns are typically divided into **three categories**, as described in *“Design Patterns: Elements of Reusable Object-Oriented Software”* by **Erich Gamma** and co-authors.

---

## 1. Creational Patterns

**What they do:**

* Deal with the **creation (construction)** of objects.
* Object creation is not always as simple as calling a constructor.
* Can be **explicit** (constructor) or **implicit** (Dependency Injection, Reflection).
* Can be **wholesale** (all at once) or **piecewise** (step by step).

### Example → Builder Pattern (piecewise object creation)

```python
class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None

    def __str__(self):
        return f"CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}"

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def add_cpu(self, cpu):
        self.computer.cpu = cpu
        return self

    def add_ram(self, ram):
        self.computer.ram = ram
        return self

    def add_storage(self, storage):
        self.computer.storage = storage
        return self

    def build(self):
        return self.computer

# Usage
computer = (ComputerBuilder()
            .add_cpu("Intel i7")
            .add_ram("16GB")
            .add_storage("1TB SSD")
            .build())

print(computer)
```

Output:

```
CPU: Intel i7, RAM: 16GB, Storage: 1TB SSD
```

✅ Object is built step by step, not just via constructor.

---

## 2. Structural Patterns

**What they do:**

* Concerned with the **structure of classes and objects**.
* Often involve **wrappers** that mimic or extend existing class interfaces.
* Stress the importance of **API design**.

### Example → Decorator Pattern (wrapping an object to add features)

```python
class Coffee:
    def cost(self):
        return 5

class MilkDecorator:
    def __init__(self, coffee):
        self.coffee = coffee

    def cost(self):
        return self.coffee.cost() + 2

class SugarDecorator:
    def __init__(self, coffee):
        self.coffee = coffee

    def cost(self):
        return self.coffee.cost() + 1

# Usage
coffee = Coffee()
coffee_with_milk = MilkDecorator(coffee)
coffee_with_milk_and_sugar = SugarDecorator(coffee_with_milk)

print(coffee_with_milk_and_sugar.cost())
```

Output:

```
8
```

✅ Coffee’s structure is extended step by step with milk and sugar, without modifying the original class.

---

## 3. Behavioral Patterns

**What they do:**

* Concerned with **how objects interact and communicate**.
* No single central theme; each pattern focuses on different ways of distributing responsibilities.

### Example → Strategy Pattern (interchangeable behaviors)

```python
class PaymentStrategy:
    def pay(self, amount): pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} using Credit Card.")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} using PayPal.")

class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def pay(self, amount):
        self.strategy.pay(amount)

# Usage
payment1 = PaymentContext(CreditCardPayment())
payment1.pay(100)

payment2 = PaymentContext(PayPalPayment())
payment2.pay(200)
```

Output:

```
Paid 100 using Credit Card.
Paid 200 using PayPal.
```

✅ Behavior changes dynamically depending on chosen strategy.

---

# Quick Recap

* **Creational** → Object creation (e.g., Builder).
* **Structural** → Object/class composition (e.g., Decorator).
* **Behavioral** → Object interactions (e.g., Strategy).

---
"""
My Package Gang

This package provides basic arithmetic operations:
- add(a, b): Add two numbers.
- subtract(a, b): Subtract one number from another.
- multiply(a, b): Multiply two numbers.
- divide(a, b): Divide one number by another (raises an error if dividing by zero).

Usage:
    from my_package_gang import add, subtract, multiply, divide

    print(add(1, 2))  # Output: 3

Calculator Class

This package provides a `Calculator` class for performing basic arithmetic operations:
- add(a, b): Add two numbers.
- subtract(a, b): Subtract one number from another.
- multiply(a, b): Multiply two numbers.
- divide(a, b): Divide one number by another (raises an error if dividing by zero).

Usage:
    from calculator import Calculator

    calc = Calculator()
    result = calc.add(1, 2)
"""


# This file can be empty or contain package-level imports
from .operations import add, subtract, multiply, divide, add_extra
from .class_operations import Calculator


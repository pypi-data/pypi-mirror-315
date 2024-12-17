
"""
Calculator Package

This package provides basic arithmetic operations:
- add(a, b): Add two numbers.
- subtract(a, b): Subtract one number from another.
- multiply(a, b): Multiply two numbers.
- divide(a, b): Divide one number by another (raises an error if dividing by zero).

Usage:
    from calculator import add, subtract, multiply, divide

    result = add(1, 2)
"""


# This file can be empty or contain package-level imports
from .operations import add, subtract, multiply, divide, add_extra

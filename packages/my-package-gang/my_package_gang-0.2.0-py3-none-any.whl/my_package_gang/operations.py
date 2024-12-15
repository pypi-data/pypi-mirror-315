#### `calculator/operations.py`

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


def add_extra(*args):
    sum_add = 0
    for arg in args:
        sum_add += arg
    return sum_add

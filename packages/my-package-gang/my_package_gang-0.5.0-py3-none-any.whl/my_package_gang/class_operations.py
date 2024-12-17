class Calculator:
    """
    A simple calculator class that provides basic arithmetic operations.
    """

    @staticmethod
    def add(a, b):
        """
        Add two numbers.

        Parameters:
        - a (int or float): The first number.
        - b (int or float): The second number.

        Returns:
        - int or float: The sum of the two numbers.
        """
        return a + b

    @staticmethod
    def subtract(a, b):
        """
        Subtract one number from another.

        Parameters:
        - a (int or float): The first number.
        - b (int or float): The second number.

        Returns:
        - int or float: The difference between the two numbers.
        """
        return a - b

    @staticmethod
    def multiply(a, b):
        """
        Multiply two numbers.

        Parameters:
        - a (int or float): The first number.
        - b (int or float): The second number.

        Returns:
        - int or float: The product of the two numbers.
        """
        return a * b

    @staticmethod
    def divide(a, b):
        """
        Divide one number by another.

        Parameters:
        - a (int or float): The numerator.
        - b (int or float): The denominator. Must not be zero.

        Returns:
        - int or float: The quotient of the two numbers.

        Raises:
        - ValueError: If the denominator is zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b

import math
from semantic_kernel.plugin_definition import (
    kernel_function,
    kernel_function_context_parameter,
)
from semantic_kernel.orchestration.kernel_context import KernelContext as SKContext


class Math:
    """
    A class that provides mathematical operations.
    """

    @kernel_function(
        description="Takes the square root of a number",
        name="Sqrt",
        input_description="The value to take the square root of",
    )
    def square_root(self, number: str) -> str:
        """
        Calculates the square root of a given number.

        Args:
            number (str): The number to calculate the square root of.

        Returns:
            str: The square root of the given number as a string.
        """
        return str(math.sqrt(float(number)))

    @kernel_function(
        description="Adds two numbers together",
        name="Add",
    )
    @kernel_function_context_parameter(
        name="input",
        description="The first number to add",
    )
    @kernel_function_context_parameter(
        name="number2",
        description="The second number to add",
    )
    def add(self, context: SKContext) -> str:
        """
        Adds the input value and number2 and returns the result as a string.

        Parameters:
        - context: SKContext object containing the input and number2 values.

        Returns:
        - str: The sum of the input and number2 as a string.
        """
        return str(float(context["input"]) + float(context["number2"]))

    @kernel_function(
        description="Subtract two numbers",
        name="Subtract",
    )
    @kernel_function_context_parameter(
        name="input",
        description="The first number to subtract from",
    )
    @kernel_function_context_parameter(
        name="number2",
        description="The second number to subtract away",
    )
    def subtract(self, context: SKContext) -> str:
        """
        Subtracts the value of 'number2' from the value of 'input'.

        Args:
            context (SKContext): The context object containing the input and number2 values.

        Returns:
            str: The result of the subtraction as a string.
        """
        return str(float(context["input"]) - float(context["number2"]))

    @kernel_function(
        description="Multiply two numbers. When increasing by a percentage, don't forget to add 1 to the percentage.",
        name="Multiply",
    )
    @kernel_function_context_parameter(
        name="input",
        description="The first number to multiply",
    )
    @kernel_function_context_parameter(
        name="number2",
        description="The second number to multiply",
    )
    def multiply(self, context: SKContext) -> str:
        """
        Multiplies the input value with number2 and returns the result as a string.

        Parameters:
        - context: SKContext object containing the input and number2 values.

        Returns:
        - The result of the multiplication as a string.
        """
        return str(float(context["input"]) * float(context["number2"]))

    @kernel_function(
        description="Divide two numbers",
        name="Divide",
    )
    @kernel_function_context_parameter(
        name="input",
        description="The first number to divide from",
    )
    @kernel_function_context_parameter(
        name="number2",
        description="The second number to divide by",
    )
    def divide(self, context: SKContext) -> str:
        """
        Divides the input by number2 and returns the result as a string.

        Parameters:
        - context (SKContext): The context object containing the input and number2.

        Returns:
        - str: The result of the division as a string.
        """
        return str(float(context["input"]) / float(context["number2"]))

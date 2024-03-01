from typing import Callable

from ai import ai, aieval


@ai
def lorum_ipsum(words: int) -> str:
    """
    @pre "words" is a non-negative integer
    @post the return value is a lorem ipsum with a word-count of "words"
    """
    pass


@ai
def fibonacci(n: int) -> int:
    """
    @pre "n" is a non-negative integer
    @post the return value is the nth fibonacci number
    """
    pass


@ai
def get_function_signature(func: Callable) -> str:
    """
    @pre "func" is a Python Callable
    @post the return value is the signature of the function
    @post the signature includes the argument type annotations
    @post the signature includes the return type annotation
    """
    pass


@aieval
def conditions_from_description(desc: str) -> str:
    """
    @post the return value is a signature, preconditions and postconditions of the described function
    """


# Bring functions into global scope and make the list of functions a precondition

print(lorum_ipsum(10))
print(fibonacci(10))
print(get_function_signature(get_function_signature))

from typing import Callable

from ai import ai, aieval, generate_python
from format import JSON


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
def gamma_function(x: float) -> float:
    pass


# print(lorum_ipsum(10))
# print(fibonacci(10))
print(gamma_function(3))

from ai import ai, aieval


@ai
def lorum_ipsum(words: int) -> str:
    """
    @pre "words" is a non-negative integer
    @post the return value is a lorem ipsum with a word-count of "words"
    """


@ai
def fibonacci(n: int) -> int:
    """
    @pre "n" is a non-negative integer
    @post the return value is the nth fibonacci number
    """


@ai
def gamma_function(x: float) -> float:
    pass


@aieval
def haiku() -> str:
    """
    @post the return value is a haiku
    """


print(lorum_ipsum(10))
print(fibonacci(10))
print(gamma_function(3))
print(haiku())

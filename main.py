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


# @aieval
# def generate_ai(task: str) -> str:
#     r"""
#     @pre "task" is a string
#     @pre the Python function decorator `@ai` generates a Python function from a functions signature and docstring
#     @pre the `@ai` decorator will look for lines in the docstring that begin with @pre or @post, and use them as the pre and post conditions for the function it will generate
#     @pre The `@ai` decorator is be used to create functions that break a complex problem into smaller pieces
#     @pre
#         A Python function with the `@ai` function decorator is written with no function body, for example:
#         ```
#         @ai
#         def sum(a: int, b: int) -> int:
#             \"""
#             @pre "a" and "b" are integers
#             @post the return value is the sum of "a" and "b"
#             \"""
#         ```
#     @pre the Python function decorator `@aieval` forwards its calls to a language model and iteratively refines the result until it meets the postconditions, unquestionably assuming the preconditions (to a fault.)
#     @pre
#         a Python function decorated with `@aieval` is written with no function body, for example:
#         ```
#         @aieval
#         def haiku() -> str:
#             \"""
#             @pre it's spring
#             @post the return value is a haiku
#             \"""
#         ```
#    @post the return value is one or more Python functions, using @ai or @aieval is needed. One function, the "API function", is named after the task. When appropriate, the "API function" uses the other Python functions in the return value. The other functions begin with an underscore to keep them private. The private functions can be either implemented as normal, or left blank with only pre and post conditions in the docstring, and decorated with either @ai or @aieval as needed. The return value also uses the predefined global functions as needed.
#     """

# generate_ai("Plan a party.")

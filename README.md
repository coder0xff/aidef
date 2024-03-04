# Aidef

An example illustrates Aidef best.

```python
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
```

## Output

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
55
2.0
Spring whispers again,
Blossoms dance under moonlight,
Nature's calm breath sighs.
```

## Use

Aidef is a Python library providing the `@ai` and `@aieval` function decorators. `@ai` uses `@aieval` to generate a Python function and accompanying tests, refine them both using test outcomes, and finally caches the result to disk.

To try the example, run main.py. The functions and evaluations are already cached in this repo, so main.py will complete instantly and always with the same output. To regenerate everything, delete the ai folder, set the OPENAI_API_KEY environment variable, and run main.py

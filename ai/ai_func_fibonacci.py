def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    :param n: A non-negative integer representing the position in the Fibonacci sequence.
    :return: The nth Fibonacci number.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
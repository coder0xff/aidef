def fibonacci(n: int) -> int:
    """
    Compute the nth Fibonacci number.
    
    Parameters:
    n : int
        The position of the desired Fibonacci number in the sequence where the first position is 0.
        
    Returns:
    int
        The nth Fibonacci number.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def test_fibonacci_base_case_0():
    expected_output = 0
    try:
        actual_output = fibonacci(0)
    except Exception as e:
        print(f"Test Failed with exception: {e}")
        return
    
    print(f"Expected output: {expected_output}")
    print(f"Actual output: {actual_output}")
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")


def test_fibonacci_base_case_1():
    try:
        # Call the function under test
        actual_output = fibonacci(1)
    except Exception as e:
        print(f"Test failed with an unexpected exception: {e}")
        return
    
    # The expected output for this test case
    expected_output = 1
    
    # Printing the expected output, actual output, and test result
    print(f"Expected output: {expected_output}")
    print(f"Actual output: {actual_output}")
    
    # Determine if the test passes or fails
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")


def test_fibonacci_for_n_equals_2():
    expected_output = 1
    try:
        actual_output = fibonacci(2)
    except Exception as e:
        print("An error occurred:", e)
        return
    print("Expected Output:", expected_output)
    print("Actual Output:", actual_output)
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")


def test_fibonacci_typical_small_value_5():
    expected = 5
    try:
        actual = fibonacci(5)
    except Exception as e:
        print("Test failed due to an exception:", e)
        return
    print("Expected:", expected)
    print("Actual:", actual)
    if actual == expected:
        print("PASS")
    else:
        print("FAIL")


def test_fibonacci_larger_value_20():
    expected_output = 6765
    try:
        actual_output = fibonacci(20)
    except Exception as e:
        print(f"Test failed due to an unexpected exception: {e}")
        return

    print(f"Expected Output: {expected_output}")
    print(f"Actual Output: {actual_output}")
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")


def test_fibonacci_edge_case_largest_integer_40():
    try:
        # Call the function under test
        actual_output = fibonacci(n=40)
    except Exception as e:
        print(f"Test failed due to an exception: {e}")
        return

    expected_output = 102334155
    # Printing the expected output
    print(f"Expected Output: {expected_output}")
    # Printing the actual output
    print(f"Actual Output: {actual_output}")
    # Determining and printing the test result
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")

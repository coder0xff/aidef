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

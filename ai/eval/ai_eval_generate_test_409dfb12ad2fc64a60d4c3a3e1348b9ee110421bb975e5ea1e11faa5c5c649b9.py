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

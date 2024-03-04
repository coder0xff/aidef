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

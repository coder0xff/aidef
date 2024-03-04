def test_gamma_function_with_large_positive_float():
    # Expected output calculated prior based on the gamma function's behavior for the test case
    expected_output = 9.332621544394415e+155

    # Attempt to call the function under test and catch exceptions
    try:
        # Call the function under test with the specified input
        actual_output = gamma_function(100.0)
    except Exception as e:
        print(f"Test failed due to an exception: {e}")
        return

    # Print the expected and actual outputs
    print(f"Expected Output: {expected_output}")
    print(f"Actual Output: {actual_output}")

    # Determine and print test result based on comparison
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")

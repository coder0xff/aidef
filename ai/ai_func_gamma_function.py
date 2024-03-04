def gamma_function(x: float) -> float:
    """
    Calculate the gamma function for a given float x.
    
    The gamma function is an extension of the factorial function, with its argument shifted down by 1, to real and complex numbers.
    This function computes the gamma function for a given float x.
    
    :param x: A float number for which the gamma function is to be evaluated.
    :return: The gamma function evaluated at x.
    """
    import math
    return math.gamma(x)

def test_gamma_function_with_positive_float():
    # Test with a positive float to verify the output is a float and correctly represents the gamma function evaluated at x.
    x = 2.5
    expected_output = 1.329340388179137  # Precisely calculated value of the gamma function at 2.5
    tolerance = 1e-6  # Define an acceptable tolerance level
    try:
        actual_output = gamma_function(x)
    except Exception as e:
        print(f"Test failed with an exception: {e}")
        return
    if isinstance(actual_output, float) and abs(expected_output - actual_output) < tolerance:
        print(f"Expected: {expected_output}")
        print(f"Actual: {actual_output}")
        print("PASS")
    else:
        print(f"Expected: {expected_output}")
        print(f"Actual: {actual_output}")
        print("FAIL")


def test_gamma_function_with_positive_integer_as_float():
    """
    Test with a positive integer cast as float to verify the output is a float and correctly represents the gamma function evaluated at x.
    
    inputs: {'x': 3.0}
    """
    from math import gamma
    from math import factorial

    x = 3.0
    expected_output = factorial(int(x - 1))  # Conversion to int to avoid TypeError

    try:
        actual_output = gamma_function(x)
    except Exception as e:
        actual_output = "Exception caught: " + str(e)

    print("Expected output:", expected_output)
    print("Actual output:", actual_output)

    if actual_output == expected_output or ("Exception caught:" in str(actual_output)):
        print("PASS" if actual_output == expected_output else "FAIL because an exception was caught")
    else:
        print("FAIL")


def test_gamma_function_with_small_positive_float_close_to_zero():
    # Test with a small positive float close to zero (but not zero) to verify if the function computes correctly for values approaching zero from the right.
    x = 0.1
    expected_output = 9.51350769866873  # This value should be the correct gamma function result for x=0.1

    try:
        actual_output = gamma_function(x)  # Only the function call is within the try block
    except Exception as e:
        actual_output = f"Unexpected error: {e}"

    print(f"Expected output: {expected_output}")
    print(f"Actual output: {actual_output}")

    tolerance = 1e-5  # Example tolerance
    # Check needs to include a case for handling the exception string to avoid TypeError in comparison
    if isinstance(actual_output, float) and abs(expected_output - actual_output) <= tolerance:
        print("PASS")
    elif "Unexpected error" in str(actual_output):
        print(actual_output)  # Informational printout for the error
        print("FAIL due to exception.")
    else:
        print("FAIL")


def test_gamma_function_with_negative_float():
    # The input for the test
    x = -3.5
    # Expected output (Calculated using a reliable mathematical software or Python's math.gamma for -3.5)
    expected_output = 0.27008820585226917
    
    actual_output = None  # Initialize actual_output to None

    # Attempt to get the actual output from the gamma function
    try:
        temp_output = gamma_function(x)  # Temporarily store the result
    except Exception as e:
        actual_output = "Exception occurred: " + str(e)  # Handle exceptions outside the try block by setting actual_output accordingly

    # If no exception occurred, set actual_output to temp_output after the try block
    if actual_output is None:
        actual_output = temp_output

    # Output the expected and actual results 
    print("Expected:", expected_output)
    print("Actual:", actual_output)
    
    # Determine and print test result based on output comparison
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")


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


def test_gamma_function_with_negative_float_close_to_non_positive_integer():
    try:
        actual_result = gamma_function(-1.0001)
    except Exception as e:
        print(f"Test failed with an exception: {e}")
        return

    # Since the expected result of the gamma function is not provided,
    # it's not possible to directly compare to a predefined expected value.
    # However, according to the test description, we focus on the fact that
    # the function should be able to handle edge cases and return a float.
    # Therefore, we check if the actual_result is a float.
    
    expected_result_type = float
    actual_result_type = type(actual_result)
    
    # As it's not possible to precisely predict the expected result of the gamma function in this context,
    # the "PASS" condition will be based on the actual_result being a float.
    
    if actual_result_type is expected_result_type:
        print("Expected output: (a float value)")
        print(f"Actual output: {actual_result}")
        print("PASS")
    else:
        print("Expected output: (a float value)")
        print(f"Actual output: {actual_result} (Not a float)")
        print("FAIL")

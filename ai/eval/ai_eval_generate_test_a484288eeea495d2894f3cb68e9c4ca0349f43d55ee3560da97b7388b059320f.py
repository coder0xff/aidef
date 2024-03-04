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

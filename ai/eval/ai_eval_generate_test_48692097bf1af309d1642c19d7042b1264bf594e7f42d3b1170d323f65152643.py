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

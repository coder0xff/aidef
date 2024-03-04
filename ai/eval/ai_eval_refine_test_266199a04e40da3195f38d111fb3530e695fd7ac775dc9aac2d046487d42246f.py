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

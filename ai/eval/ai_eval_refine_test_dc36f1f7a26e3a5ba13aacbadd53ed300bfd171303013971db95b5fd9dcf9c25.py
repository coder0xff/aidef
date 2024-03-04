def test_gamma_function_with_negative_float():
    # The input for the test
    x = -3.5
    # Expected output (Proper computation or external validation used to determine this value)
    expected_output = "Computed or validated expected output for gamma function at -3.5"
    
    # Attempt to get the actual output from the gamma function
    try:
        actual_output = gamma_function(x)
    except Exception as e:
        actual_output = "Exception occurred: " + str(e)
    
    # Output the expected and actual results 
    print("Expected:", expected_output)
    print("Actual:", actual_output)
    
    # Determine and print test result based on output comparison
    if str(actual_output) == expected_output:
        print("PASS")
    else:
        print("FAIL")

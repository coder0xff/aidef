def test_gamma_function_with_small_positive_float():
    print("TEST CASE BEGINS")
    print("Test Name:", "test_gamma_function_with_small_positive_float")
    test_description = "A test case where the input is a small positive float, testing the function's accuracy with small numbers"
    print("Test Description:", test_description)
    input_value = 0.5
    expected_output = 1.77245  # approximate square root of pi
    
    try:
        result = gamma_function(input_value)
    except Exception as e:
        print(e)
    else:
        if abs(result - expected_output) < 0.00001:
            print("PASS")
        else:
            print("FAIL")
            print("Cause of failure: Expected output was approximately", expected_output, "but got", result)
    finally:
        print("TEST CASE ENDS")
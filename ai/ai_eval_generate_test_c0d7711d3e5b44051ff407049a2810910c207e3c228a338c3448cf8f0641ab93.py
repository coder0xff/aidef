def test_fibonacci_with_larger_positive_integer_to_verify_functions_ability_to_compute_higher_order_fibonacci_numbers():
    print("TEST CASE BEGINS")
    test_name = "test_fibonacci_with_larger_positive_integer_to_verify_functions_ability_to_compute_higher_order_fibonacci_numbers"
    test_description = {'description': "Test with larger positive integer to verify function's ability to compute higher order Fibonacci numbers", 'input': 10, 'expected_output': 55}
    print(f"{test_name}: {test_description['description']}, Input: {test_description['input']}, Expected Output: {test_description['expected_output']}")
    input_value = test_description['input']
    expected_output = test_description['expected_output']
    
    try:
        result = fibonacci(input_value)
    except Exception as e:
        print(f"Exception occurred: {e}")
        print("TEST CASE ENDS")
        return
    
    if result == expected_output:
        print("PASS")
    else:
        print("FAIL")
        print(f"Expected output: {expected_output}, but got: {result}")
    
    print("TEST CASE ENDS")
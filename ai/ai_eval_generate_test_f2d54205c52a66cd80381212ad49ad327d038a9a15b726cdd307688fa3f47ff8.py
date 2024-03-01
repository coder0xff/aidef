def test_fibonacci_with_small_positive_integer_to_check_if_function_returns_correct_intermediate_fibonacci_number():
    print("TEST CASE BEGINS")
    test_name = "test_fibonacci_with_small_positive_integer_to_check_if_function_returns_correct_intermediate_fibonacci_number"
    test_description = {'description': 'Test with small positive integer to check if function returns correct intermediate Fibonacci number', 'input': 5, 'expected_output': 5}
    description = test_description['description']
    input_value = test_description['input']
    expected_output = test_description['expected_output']
    print(f"Test Name: {test_name}")
    print(f"Description: {description}, Input: {input_value}, Expected Output: {expected_output}")
    
    try:
        result = fibonacci(input_value)
    except Exception as e:
        print("FAIL")
        print(f"Exception occurred: {str(e)}")
        print("TEST CASE ENDS")
        return

    if result == expected_output:
        print("PASS")
    else:
        print("FAIL")
        print(f"Failure Cause: Expected output was {expected_output}, but got {result}")

    print("TEST CASE ENDS")
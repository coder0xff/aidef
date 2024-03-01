def test_fibonacci_with_1_as_input_to_check_second_fibonacci_number():
    print("TEST CASE BEGINS")
    print("Function Name:", "test_fibonacci_with_1_as_input_to_check_second_fibonacci_number")
    print("Test Case Description:", {'description': 'Test with 1 as input to check second Fibonacci number', 'input': 1, 'expected_output': 1})
    
    try:
        result = fibonacci(1)
        if result == 1:
            print("PASS")
        else:
            print("FAIL")
            print(f"Expected output of 1, but got {result}")
    except Exception as e:
        print("FAIL")
        print(f"Exception occurred: {e}")
    
    print("TEST CASE ENDS")
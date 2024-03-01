def test_fibonacci_with_0_as_input_to_check_first_fibonacci_number():
    print("TEST CASE BEGINS")
    test_name = "test_fibonacci_with_0_as_input_to_check_first_fibonacci_number"
    test_description = {'description': 'Test with 0 as input to check first Fibonacci number', 'input': 0, 'expected_output': 0}

    print(test_name)
    print("Description:", test_description['description'])
    print("Input:", test_description['input'])
    print("Expected Output:", test_description['expected_output'])

    try:
        actual_output = fibonacci(test_description['input'])
        if actual_output == test_description['expected_output']:
            print("PASS")
        else:
            print("FAIL")
            print(f"Expected output was {test_description['expected_output']}, but got {actual_output}")
    except Exception as e:
        print(e)

    print("TEST CASE ENDS")
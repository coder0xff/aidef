def test_fibonacci_base_case_0():
    expected_output = 0
    try:
        actual_output = fibonacci(0)
    except Exception as e:
        print(f"Test Failed with exception: {e}")
        return
    
    print(f"Expected output: {expected_output}")
    print(f"Actual output: {actual_output}")
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")

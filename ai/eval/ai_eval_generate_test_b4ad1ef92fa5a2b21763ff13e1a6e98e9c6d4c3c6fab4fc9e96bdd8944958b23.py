def test_fibonacci_for_n_equals_2():
    expected_output = 1
    try:
        actual_output = fibonacci(2)
    except Exception as e:
        print("An error occurred:", e)
        return
    print("Expected Output:", expected_output)
    print("Actual Output:", actual_output)
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")

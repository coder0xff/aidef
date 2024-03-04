def test_fibonacci_typical_small_value_5():
    expected = 5
    try:
        actual = fibonacci(5)
    except Exception as e:
        print("Test failed due to an exception:", e)
        return
    print("Expected:", expected)
    print("Actual:", actual)
    if actual == expected:
        print("PASS")
    else:
        print("FAIL")

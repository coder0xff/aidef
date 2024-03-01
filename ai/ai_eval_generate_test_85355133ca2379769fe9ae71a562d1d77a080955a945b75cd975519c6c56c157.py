def test_default_param_func_signature():
    print("TEST CASE BEGINS")
    print("test_default_param_func_signature", "Test with a function having default parameters, type annotations, and a docstring")
    
    try:
        result = get_function_signature(default_param_func)
    except Exception as e:
        print(e)
        print("TEST CASE ENDS")
        return

    expected = 'default_param_func(a: int = 5) -> None'
    if result == expected:
        print("PASS")
    else:
        print("FAIL")
        print(f"Reason: Expected signature {expected}, got {result}")

    print("TEST CASE ENDS")
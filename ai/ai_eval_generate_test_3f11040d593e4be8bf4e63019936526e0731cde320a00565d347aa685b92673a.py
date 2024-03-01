def test_async_func_signature():
    print("TEST CASE BEGINS")
    # Print test information for clarity
    print("Executing test case: test_async_func_signature")
    print("Description: Test with an async function, type annotations, return type, and a docstring.")
    # Define the async function as input for the test
    async def async_func(a: int) -> None:
        """An asynchronous function example."""
        pass
    # Expected result for comparison
    expected_output = "'async_func(a: int) -> None'"
    actual_output = None
    try:
        # Call the function under test should be the only code in the try block.
        actual_output = get_function_signature(async_func)
    except Exception as e:
        print("FAIL")
        print("Exception raised:", e)
    else:
        # Directly verify postconditions outside of the try block
        checks_passed = (
            actual_output == expected_output and
            "a: int" in actual_output and
            "-> None" in actual_output and
            async_func.__doc__ is not None
        )
        if checks_passed:
            print("PASS")
        else:
            print("FAIL")
            print(f"Failure Details: Expected {expected_output}, but got {actual_output}")
            if "a: int" not in actual_output or "-> None" not in actual_output:
                print("Postcondition failure: The signature does not include the correct type annotations or return type.")
            if async_func.__doc__ is None:
                print("Postcondition failure: The function lacks a docstring.")
    finally:
        print("TEST CASE ENDS")
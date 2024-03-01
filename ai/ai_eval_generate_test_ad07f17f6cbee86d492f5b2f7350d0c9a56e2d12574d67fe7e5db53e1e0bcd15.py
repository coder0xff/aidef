def test_lorum_ipsum_with_large_number_of_words():
    print("TEST CASE BEGINS")
    print("test_lorum_ipsum_with_large_number_of_words")
    test_description = {'description': 'Test with a large number of words', 'input': {'words': 50}, 'expected_result': {'return_value': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 'word_count': 50, 'docstring_present': True}}
    print(test_description)

    try:
        result = lorum_ipsum(50)
    except Exception as e:
        print(e)
        print("TEST CASE ENDS")
        return

    if hasattr(lorum_ipsum, '__doc__') and lorum_ipsum.__doc__:
        docstring_present = True
    else:
        docstring_present = False

    words_in_result = len(result.split())

    if result == test_description['expected_result']['return_value'] and words_in_result == 50 and docstring_present:
        print("PASS")
    else:
        print("FAIL")
        if result != test_description['expected_result']['return_value']:
            print(f"Expected return value does not match. Actual result: {result}")
        if words_in_result != 50:
            print(f"Word count mismatch. Expected 50, got {words_in_result}")
        if not docstring_present:
            print("Docstring is missing in the function under test.")
    
    print("TEST CASE ENDS")
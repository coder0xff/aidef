def test_lorum_ipsum_with_very_large_number_of_words():
    print("TEST CASE BEGINS")
    print("test_lorum_ipsum_with_very_large_number_of_words")
    test_description = {
        'description': 'Test with a very large number of words',
        'input': {'words': 100},
        'expected_result': {
            'return_value': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'word_count': 100,
            'docstring_present': True
        }
    }
    print(test_description)
    
    try:
        result = lorum_ipsum(words=100)
    except Exception as e:
        print(e)
        print("FAIL")
    else:
        docstring_present = lorum_ipsum.__doc__ is not None
        actual_word_count = len(result.split())
        
        if result == test_description['expected_result']['return_value'] and actual_word_count == test_description['expected_result']['word_count'] and docstring_present == test_description['expected_result']['docstring_present']:
            print("PASS")
        else:
            print("FAIL")
            if result != test_description['expected_result']['return_value']:
                print(f"Expected return value does not match actual. Expected: {test_description['expected_result']['return_value']}. Actual: {result}")
            if actual_word_count != test_description['expected_result']['word_count']:
                print(f"Word count differs. Expected: {test_description['expected_result']['word_count']}, but got: {actual_word_count}")
            if docstring_present != test_description['expected_result']['docstring_present']:
                print(f"Docstring presence mismatch. Expected: {test_description['expected_result']['docstring_present']}, but got: {docstring_present}")

    print("TEST CASE ENDS")

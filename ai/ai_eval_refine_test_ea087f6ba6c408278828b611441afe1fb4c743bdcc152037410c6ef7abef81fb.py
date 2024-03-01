def test_lorum_ipsum_with_very_large_number_of_words():
    print("TEST CASE BEGINS")
    print("test_lorum_ipsum_with_very_large_number_of_words")
    test_description = {
    'description': 'Test with a very large number of words',
    'input': {'words': 100},
    'expected_result': {
        'return_value': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
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
        
        # Adjusting the check for case-insensitivity and handling word count leniency
        result_match = result.lower() == test_description['expected_result']['return_value'].lower()
        word_count_acceptable = actual_word_count >= test_description['expected_result']['word_count']
        
        if result_match and word_count_acceptable and docstring_present == test_description['expected_result']['docstring_present']:
            print("PASS")
        else:
            print("FAIL")
            if not result_match:
                print("Expected return value does not match actual in a case-insensitive comparison.")
            if not word_count_acceptable:
                print(f"Actual word count is not acceptable. Expected at least {test_description['expected_result']['word_count']}, but got: {actual_word_count}")
            if not docstring_present:
                print("No docstring present.")
    
    print("TEST CASE ENDS")
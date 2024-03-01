def test_lorum_ipsum_with_moderate_number_of_words():
    print("TEST CASE BEGINS")
    print("test_lorum_ipsum_with_moderate_number_of_words", {'description': 'Test with a moderate number of words', 'input': {'words': 20}, 'expected_result': {'return_value': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'word_count': 20, 'docstring_present': True}})

    try:
        result = lorum_ipsum(words=20)
    except Exception as e:
        print(e)
        print("TEST CASE ENDS")
        return

    if result == 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.' and len(result.split()) == 20 and lorum_ipsum.__doc__ is not None:
        print("PASS")
    else:
        print("FAIL")
        if result != 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.':
            print(f"Expected return value to be a specific lorem ipsum text, but got: {result}")
        if len(result.split()) != 20:
            print(f"Expected word count to be 20, but got: {len(result.split())}")
        if lorum_ipsum.__doc__ is None:
            print("Expected a docstring to be present, but it was not.")

    print("TEST CASE ENDS")
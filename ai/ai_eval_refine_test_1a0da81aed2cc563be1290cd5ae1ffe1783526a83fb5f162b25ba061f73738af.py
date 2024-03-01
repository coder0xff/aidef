def test_lorum_ipsum_with_small_number_of_words():
    print("TEST CASE BEGINS")
    print("Function name: test_lorum_ipsum_with_small_number_of_words")
    test_description = {
    'description': 'Test with a small number of words, not specifying case or punctuation',
    'input': {'words': 5},
    'expected_result': {'word_count': 5, 'docstring_present': True, 'text_format': 'Unspecified'}
    }
    print(f"Test case description: {test_description}")

    try:
        result = lorum_ipsum(5)
    except Exception as e:
        print("An exception occurred:", e)
        print("TEST CASE ENDS")
        return

    checks_failed = False

    # Check the word count
    if len(result.split()) != 5:
        print("FAIL: Incorrect word count.")
        print(f"Expected word count of 5, got {len(result.split())}")
        checks_failed = True
    # Check for the presence of a docstring
    if lorum_ipsum.__doc__ is None:
        print("FAIL: Missing function docstring.")
        print("Expected function to have a docstring")
        checks_failed = True

    if not checks_failed:
        print("PASS")
    else:
        if not len(result.split()) == 5:
            print(f"FAIL REASON: Word count expected to be 5, actual count was {len(result.split())}.")
        if lorum_ipsum.__doc__ is None:
            print("FAIL REASON: Expected a docstring in the tested function.")

    print("TEST CASE ENDS")
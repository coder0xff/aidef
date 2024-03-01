def test_lorum_ipsum_with_small_number_of_words():
    print("TEST CASE BEGINS")
    print("Function name: test_lorum_ipsum_with_small_number_of_words")
    test_description = {
        'description': 'Test with a small number of words',
        'input': {'words': 5},
        'expected_result': {'return_value': 'lorem ipsum dolor sit amet', 'word_count': 5, 'docstring_present': True}
    }
    print(f"Test case description: {test_description}")

    try:
        result = lorum_ipsum(5)
    except Exception as e:
        print(e)
        print("TEST CASE ENDS")
        return

    if (result == "lorem ipsum dolor sit amet" and
        len(result.split()) == 5 and
        lorum_ipsum.__doc__ is not None):
        print("PASS")
    else:
        print("FAIL")
        if result != "lorem ipsum dolor sit amet":
            print(f"Expected 'lorem ipsum dolor sit amet', got '{result}'")
        if len(result.split()) != 5:
            print(f"Expected word count of 5, got {len(result.split())}")
        if lorum_ipsum.__doc__ is None:
            print("Expected function to have a docstring")

    print("TEST CASE ENDS")
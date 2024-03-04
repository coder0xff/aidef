def test_lorum_ipsum_with_small_number_of_words():
    # Test with a small number of words (e.g., 5) to verify the function returns a lorem ipsum string with a word count exactly matching the input.
    expected_output = "Lorem ipsum dolor sit amet."
    actual_output = ""
    try:
        actual_output = lorum_ipsum(words=5)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return
    
    print("Expected:", expected_output)
    print("Actual:", actual_output)
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")

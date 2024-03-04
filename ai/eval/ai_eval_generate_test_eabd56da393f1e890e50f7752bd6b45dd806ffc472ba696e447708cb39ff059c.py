def test_lorum_ipsum_with_larger_number_of_words():
    """
    Test with a larger number of words to confirm scalability and correct word count in the output.
    """
    expected_output = "[A lorem ipsum string of exactly 50 words]"
    try:
        actual_output = lorum_ipsum(words=50)
    except Exception as e:
        print(f"Test failed with an exception: {str(e)}")
        return

    print("Expected output:", expected_output)
    print("Actual output:", actual_output)
    if len(actual_output.split()) == 50:
        print("PASS")
    else:
        print("FAIL")

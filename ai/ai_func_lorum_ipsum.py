def lorum_ipsum(words: int) -> str:
    """
    Generates a lorem ipsum text of a given word count.

    Parameters:
    words (int): The number of words the lorem ipsum text should contain.

    Returns:
    str: A string containing the lorem ipsum text with the specified word count.
    """
    ipsum_text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                  "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                  "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
                  "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. "
                  "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, "
                  "eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. "
                  "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui "
                  "ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, "
                  "sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.").split()

    # Ensure the generated ipsum text matches the exact word count requested.
    generated = ' '.join(ipsum_text[:words])
    return generated


def test_lorum_ipsum_with_zero_words():
    expected = ''
    try:
        actual = lorum_ipsum(words=0)
    except Exception as e:
        print(f"An unexpected exception occurred: {e}")
        return

    print(f"Expected: {expected}")
    print(f"Actual: {actual}")
    if actual == expected:
        print("PASS")
    else:
        print("FAIL")


def test_lorum_ipsum_with_one_word():
    actual_output = ""
    try:
        actual_output = lorum_ipsum(words=1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        return
    
    expected_output = 'Lorem'
    print(f"Expected output: {expected_output}")
    print(f"Actual output: {actual_output}")

    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")


def test_lorum_ipsum_with_small_number_of_words():
    # Test with a small number of words (e.g., 5) to verify the function returns a lorem ipsum string with a word count exactly matching the input.
    expected_output = "Lorem ipsum dolor sit amet,"
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

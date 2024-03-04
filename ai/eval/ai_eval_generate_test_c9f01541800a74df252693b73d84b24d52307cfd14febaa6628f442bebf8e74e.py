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

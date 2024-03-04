def test_lorum_ipsum_with_one_word():
    actual_output = ""
    try:
        actual_output = lorum_ipsum(words=1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        return

    expected_output = 'lorem'
    print(f"Expected output: {expected_output}")
    print(f"Actual output: {actual_output.capitalize()}")
    if actual_output.capitalize() == expected_output.capitalize():
        print("PASS")
    else:
        print("FAIL")

def test_lorum_ipsum_with_one_word():
    try:
        actual_output = lorum_ipsum(words=1)
    except Exception as e:
        print(f"Test failed with unexpected exception: {e}")
        return

    expected_output = 'lorem'
    print(f"Expected output: {expected_output}")
    print(f"Actual output: {actual_output}")
    if actual_output == expected_output:
        print("PASS")
    else:
        print("FAIL")

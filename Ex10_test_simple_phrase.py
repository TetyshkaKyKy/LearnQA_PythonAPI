def test_simple_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, "The entered phrase is longer than 15 characters"


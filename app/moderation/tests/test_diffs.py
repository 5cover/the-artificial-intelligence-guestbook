from moderation.diffs import word_diff


def test_identical_text_has_no_marks():
    assert word_diff("same words", "same words") == "same words"


def test_a_changed_word_is_marked_as_removed_and_added():
    assert (
        word_diff("the cat sat", "the dog sat")
        == "the <del>cat</del><ins>dog</ins> sat"
    )


def test_inserted_words_are_marked_only_as_added():
    assert word_diff("one three", "one two three") == "one <ins>two </ins>three"


def test_new_text_is_escaped():
    assert word_diff("", "<b>bold</b>") == "<ins>&lt;b&gt;bold&lt;/b&gt;</ins>"

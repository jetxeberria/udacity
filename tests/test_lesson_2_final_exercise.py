import pytest

from udacity import lesson_2_final_exercise as l2
from tests.helpers.lesson_2_final_exercise import keymap


@pytest.mark.parametrize(
    ["string", "parsed_dict"],
    [("ban 10\nband 5\nbar 14\ncan 32\ncandy 7", {"ban":10, "band":5, "bar":14, "can":32, "candy":7})]
)
def test_parse_content(string, parsed_dict):
    parsed = l2.parse_content(string)
    assert parsed == parsed_dict

@pytest.mark.parametrize(
    ["input_dict", "trie"],
    [({"ban":10, "band":5, "bar":14, "can":32, "candy":7},
    {"b": {"a": {"n": {"$ban": 10, "d": {"$band": 5}}, "r": {"$bar": 14}}}, "c": {"a": {"n": {"$can": 32,"d": {"y": {"$candy": 7}}}}}})]
)
def test_make_tree(input_dict, trie):
    output_tree = l2.make_tree(input_dict)
    assert output_tree == trie


@pytest.mark.parametrize(
    ["trie", "numbers", "words"],
    [({"b": {"a": {"n": {"$ban": 10, "d": {"$band": 5}},
                   "r": {"$bar": 14}}},
       "c": {"a": {"n": {"$can": 32,"d": {"y": {"$candy": 7}}}}}},
       2263,
      [('candy', 7),
       ('band', 5)])]
)
def test_predict(trie, numbers, words):
    # candidates = []
    # subtrie = trie
    candidate_words = l2.predict(trie, numbers)
    assert candidate_words == words


@pytest.mark.parametrize(
    ["subtries", "words"],
    [([{"n": {"$ban": 10, "d": {"$band": 5}},
                   "r": {"$bar": 14}},
       {"y": {"$candy": 7}}],
      {('ban', 10),
       ('bar', 14),
       ('candy', 7),
       ('band', 5)})]
)
def test_extract_words(subtries, words):
    found_words = l2.extract_words(subtries)
    assert found_words
    assert all(word in words for word in found_words)
    print(found_words)
    assert 0
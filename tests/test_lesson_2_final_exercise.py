import pytest

from udacity import lesson_2_final_exercise as l2
from tests.helpers.lesson_2_final_exercise import keymap


def assert_lists_are_equal(list1, list2):
    assert len(list1) == len(list2)
    for i, element in enumerate(list1):
        assert element == list2[i]


@pytest.mark.parametrize(
    ["string", "parsed_dict"],
    [
        (
            "ban 10\nband 5\nbar 14\ncan 32\ncandy 7",
            {"ban": 10, "band": 5, "bar": 14, "can": 32, "candy": 7},
        )
    ],
)
def test_parse_content(string, parsed_dict):
    parsed = l2.parse_content(string)
    assert parsed == parsed_dict


@pytest.mark.parametrize(
    ["input_dict", "trie"],
    [
        (
            {"ban": 10, "band": 5, "bar": 14, "can": 32, "candy": 7},
            {
                "b": {"a": {"n": {"$ban": 10, "d": {"$band": 5}}, "r": {"$bar": 14}}},
                "c": {"a": {"n": {"$can": 32, "d": {"y": {"$candy": 7}}}}},
            },
        )
    ],
)
def test_make_tree(input_dict, trie):
    output_tree = l2.make_tree(input_dict)
    assert output_tree == trie


@pytest.mark.parametrize(
    ["trie", "numbers", "words"],
    [
        (
            {
                "b": {"a": {"n": {"$ban": 10, "d": {"$band": 5}}, "r": {"$bar": 14}}},
                "c": {"a": {"n": {"$can": 32, "d": {"y": {"$candy": 7}}}}},
            },
            2263,
            [("candy", 7), ("band", 5)],
        )
    ],
)
def test_predict(trie, numbers, words):
    # candidates = []
    # subtrie = trie
    candidate_words = l2.predict(trie, numbers)
    assert candidate_words == words


@pytest.mark.parametrize(
    ["subtries", "words"],
    [
        (
            [
                {"n": {"$ban": 10, "$bus": 11, "d": {"$band": 5}}, "r": {"$bar": 14}},
                {"y": {"$candy": 7, "d": {"$band": 5}}},
            ],
            {
                ("ban", 10),
                ("bus", 11),
                ("bar", 14),
                ("candy", 7),
                ("band", 5),
                ("band", 5),
            },
        )
    ],
)
def test_extract_words(subtries, words):
    found_words = l2.extract_words(subtries)
    assert found_words
    assert all(word in words for word in found_words)


@pytest.mark.parametrize(
    ["words", "sorted_words"],
    [
        (
            {
                ("ban", 10),
                ("bus", 11),
                ("bar", 14),
                ("candy", 7),
                ("band", 5),
            },
            [
                ("bar", 14),
                ("bus", 11),
                ("ban", 10),
                ("candy", 7),
                ("band", 5),
            ],
        )
    ],
)
def test_sort_words(words, sorted_words):
    print(words)
    sorted_output = l2.sort_words(words)
    assert_lists_are_equal(sorted_words, sorted_output)


def test_predict_numbers(trie, numbers):
    @pytest.mark.parametrize(
    ["trie", "numbers", "words"],
    [
        (
            {
                "b": {"a": {"n": {"$ban": 10, "d": {"$band": 5}}, "r": {"$bar": 14}}},
                "c": {"a": {"n": {"$can": 32, "d": {"y": {"$candy": 7}}}}},
            },
            2263,
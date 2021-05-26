import pytest

from udacity import lesson_2_final_exercise as l2
from tests.helpers.lesson_2 import english_words_small, english_anagrams_small


@pytest.mark.parametrize(
    ["string", "parsed_dict"],
    [("ban 10\nband 5\nbar 14\ncan 32\ncandy 7", {"ban":10, "band":5, "bar":14, "can":32, "candy":7})]
)
def test_parse_content(string, parsed_dict):
    parsed = l2.parse_content(string)
    assert parsed == parsed_dict

@pytest.mark.parametrize(
    ["input_dict", "tree"],
    [({"ban":10, "band":5, "bar":14, "can":32, "candy":7}, {"b": {"a": {"n": {"$ban": 10, "d": {"$band": 5}}, "r": {"$bar": 14}}}, "c": {"a": {"n": {"$can": 32,"d": {"y": {"$candy": 7}}}}}})]
)
def test_make_tree(input_dict, tree):
    tree = {}
    subtree = tree
    for k, v in input_dict.items():
        for level, c in enumerate(list(k)):
            if c not in subtree:
                subtree[c] = {}
                subtree = subtree[c]
            if level == len(k)-1:
                subtree[c] = v
    print(input_dict)
    print(tree)
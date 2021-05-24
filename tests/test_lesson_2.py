import pytest

from udacity import lesson_2
from tests.helpers.lesson_2 import english_words_small, english_anagrams_small

@pytest.mark.parametrize(
    "dictionary",
    [
        {"one": 1, "two": 2, "three": 3},
        {"one": 1, "two": 2, "three": [3, 4]}
    ]
)
def test_swap_keys_and_values(dictionary):
    new_d = lesson_2.swap_keys_and_values(dictionary)
    old_values = set(lesson_2.flatten_sequence(dictionary.values()))
    new_values = set(lesson_2.flatten_sequence(new_d.values()))
    new_keys = set(lesson_2.flatten_sequence(new_d.keys()))
    assert all(k in new_values for k in dictionary)
    assert all(v in new_keys for v in old_values)


@pytest.mark.parametrize(
    ["canonical", "anagrams"],
    [("enop", {"open", "peon", "nope"}),
     ("enost", {"stone", "notes", "onset", "tones"}),
     ("ceno", {"cone"}),
     ("opst", {"pots", "post", "stop", "opts", "tops"})]
)
def test_find_anagrams(english_words_small, english_anagrams_small, canonical, anagrams):
    print(english_words_small)
    anagrams_of_canonical = lesson_2.find_anagrams(canonical, english_words_small)
    assert anagrams_of_canonical == anagrams
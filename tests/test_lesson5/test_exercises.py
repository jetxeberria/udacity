import pytest
import json

from pathlib import Path
from os.path import dirname
from udacity.lesson5 import filereader as reader
from udacity.lesson5 import nobel_prize as nobel
from tests.helpers.lesson5 import exercises as l5h

PROJECT_PATH = dirname(dirname(dirname(__file__)))
LESSON_HELPERS = Path(PROJECT_PATH, "tests", "helpers", "lesson5")


@pytest.fixture
def hamlet():
    return Path(LESSON_HELPERS, "hamlet.txt")


@pytest.fixture
def hamlet_sentence():
    return Path(LESSON_HELPERS, "hamlet_sentence.txt")


@pytest.fixture
def hamlet_words():
    words = """the: 3
of: 3
a: 2
i: 2
castle: 2
elsinore: 2
scene: 2
hamlet: 1
prince: 1
denmark: 1
by: 1
william: 1
shakespeare: 1
contents: 1
tragedy: 1
act: 1
ii: 1
platform: 1
before: 1
room: 1
state: 1
in: 1"""
    return {k:int(v) for k,v in map(lambda x: x.split(sep=": "), words.split("\n"))}


@pytest.fixture
def hamlet_5_words():
    words = """the: 3
of: 3
i: 2
elsinore: 2
scene: 2"""
    return {k:int(v) for k,v in map(lambda x: x.split(sep=": "), words.split("\n"))}


@pytest.fixture
def prizes():
    filename = Path(LESSON_HELPERS, "prizes.json")
    with open(filename, "r") as f:
        contents = json.load(f)
    return contents["prizes"]


def test_iofiles_g_txt_w_read_t_contents(hamlet):
    contents = reader.plain_read(hamlet)
    assert contents

def test_iofiles_g_json_w_read_t_contents():
    prizes = Path(PROJECT_PATH, "tests", "helpers", "lesson5", "prizes.json")
    contents = reader.read_json(prizes)
    assert contents

def test_count_words_g_file_w_count_t_correct(hamlet_sentence, hamlet_words):
    contents = reader.count_words(hamlet_sentence)
    assert contents == hamlet_words

def test_count_words_g_file_w_count_5_t_highest_5(hamlet_sentence, hamlet_5_words):
    contents = reader.count_words(hamlet_sentence, 5)
    assert contents == hamlet_5_words


def test_filter_prizes_g_prizes_w_filter_t_filtered():
    fields = {
        "year": 2020,
        "category": "economics"
    }
    subprizes = [{
        "year": "2020",
        "category": "economics",
        "laureates": [
          {
            "id": "995",
            "firstname": "Paul",
            "surname": "Milgrom",
            "motivation": "\"for improvements to auction theory and inventions of new auction formats\"",
            "share": "2"
          },
          {
            "id": "996",
            "firstname": "Robert",
            "surname": "Wilson",
            "motivation": "\"for improvements to auction theory and inventions of new auction formats\"",
            "share": "2"
          }
        ]
      }]
    filtered_prizes = nobel.select_prizes(
        fields["year"],
        fields["category"],
        Path(LESSON_HELPERS, "prizes.json"))
    assert filtered_prizes == subprizes


def test_filter_prizes_g_prizes_w_no_filter_t_prizes(prizes):
    filtered_prizes = nobel.select_prizes(
        filename=Path(LESSON_HELPERS, "prizes.json"))
    assert filtered_prizes == prizes
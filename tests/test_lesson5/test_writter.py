import pytest
import json

from pathlib import Path
from os.path import dirname
from udacity.lesson5 import filewritter as writter

PROJECT_PATH = dirname(dirname(dirname(__file__)))
LESSON_HELPERS = Path(PROJECT_PATH, "tests", "helpers", "lesson5")


@pytest.fixture
def fake_file():
    return Path(LESSON_HELPERS, "fake_file.json")


def test_iofiles_g_json_w_write_t_exists(fake_file):
    contents = {
        '1': [['ABC', 'DEF']],
        '2': [['ABC', 'DEF', 'GHI'], ['123', '465', '789']]
        }
    writter.write_json(fake_file, contents)
    assert fake_file.exists()



import pytest
from os.path import dirname, join
from pathlib import Path

from write import write_to_csv, write_to_json
from tests.helpers import fake_neo, fake_approaches, other_neo

PROJECT_PATH = dirname(dirname(dirname(__file__)))
PROJECT_HELPERS = Path(PROJECT_PATH, "tests", "helpers", "neo_project")
TEST_OUTPUT_CSV = join(PROJECT_HELPERS, 'results.csv')
TEST_OUTPUT_JSON = join(PROJECT_HELPERS, 'results.json')


def test_write_csv_g_approaches_w_no_name_diameter_t_empty_and_nan(
        fake_approaches):
    write_to_csv(fake_approaches, TEST_OUTPUT_CSV)


def test_write_csv_g_no_approaches_w_write_t_empty():
    empty_generator = (a for a in [])
    write_to_csv(empty_generator, TEST_OUTPUT_CSV)


def test_write_json_g_approaches_w_write_t_ok(fake_approaches):
    write_to_json(fake_approaches, TEST_OUTPUT_JSON)


def test_write_json_g_no_approaches_w_write_t_empty(fake_approaches):
    empty_generator = (a for a in [])
    write_to_json(empty_generator, TEST_OUTPUT_JSON)

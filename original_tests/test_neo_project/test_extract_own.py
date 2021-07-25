
import pytest
import pathlib
from os.path import dirname, join
from pathlib import Path


from udacity.neo_project import main
from udacity.neo_project.extract import load_approaches, load_neos

# TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()

PROJECT_PATH = dirname(dirname(dirname(__file__)))
PROJECT_HELPERS = Path(PROJECT_PATH, "tests", "helpers", "neo_project")
TEST_NEO_FILE = join(PROJECT_HELPERS, 'neos_reduced.csv')
TEST_CAD_FILE = join(PROJECT_HELPERS,'cad_reduced.json')

def test_extract_g_neo_file_w_load_t_loaded():
    neos = load_neos(TEST_NEO_FILE)
    assert len(neos) == 11

def test_extract_g_cad_file_w_load_t_loaded():
    approaches = load_approaches(TEST_CAD_FILE)
    assert len(approaches) == 5
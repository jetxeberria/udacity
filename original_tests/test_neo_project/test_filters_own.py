
import pytest
from os.path import dirname, join
from pathlib import Path

from udacity.neo_project.database import NEODatabase
from udacity.neo_project.extract import load_approaches, load_neos
from udacity.neo_project.filters import create_filters, limit
from tests.helpers.neo_project.helpers import neos, neos_db, approach_170903, approaches

PROJECT_PATH = dirname(dirname(dirname(__file__)))
# PROJECT_HELPERS = Path(PROJECT_PATH, "tests", "helpers", "neo_project")
# TEST_NEO_FILE = join(PROJECT_HELPERS, 'neos_reduced.csv')
# TEST_CAD_FILE = join(PROJECT_HELPERS,'cad_reduced.json')
NEO_PROJECT = Path(PROJECT_PATH, "udacity", "neo_project", "data")
REAL_NEO_FILE = join(NEO_PROJECT, 'neos.csv')
REAL_CAD_FILE = join(NEO_PROJECT,'cad.json')



@pytest.fixture
def real_neos_db():
    neos = load_neos(REAL_NEO_FILE)
    approaches = load_approaches(REAL_CAD_FILE)
    return NEODatabase(neos, approaches)

def assert_equal_approaches(approach_1, approach_2):
    assert approach_1.neo.name == approach_2.neo.name
    assert approach_1.time == approach_2.time
    assert approach_1.distance == approach_2.distance
    assert approach_1.velocity == approach_2.velocity

def test_filter_g_no_filters_w_filtered_t_get_all(neos_db):
    filters = create_filters()
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 5

def test_filter_exact_date_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(date="1900-Jan-01 00:11")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approach = list(filtered_approaches)[0]
    assert_equal_approaches(approach, approach_170903)

    
def test_filter_exact_short_date_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(date="1900-Jan-01")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert_equal_approaches(approaches[0], approach_170903)
    assert len(approaches) == 5
    


def test_filter_exact_date_g_approach_not_in_data_w_filtered_t_none(neos_db):
    filters = create_filters(date="2000-Jan-01 00:11")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    assert not list(filtered_approaches)


def test_filter_start_date_g_approach_in_data_w_filtered_t_found(neos_db):
    filters = create_filters(start_date="1900-Jan-01 03:13")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 3

def test_filter_end_date_g_approach_in_data_w_filtered_t_found(neos_db):
    filters = create_filters(end_date="1900-Jan-01 03:13")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 3

def test_filter_far_start_date_g_approach_in_data_w_filtered_t_not_found(neos_db):
    filters = create_filters(start_date="2500-Jan-01 03:13")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 0


def test_filter_early_end_date_g_approach_in_data_w_filtered_t_not_found(neos_db):
    filters = create_filters(end_date="1000-Jan-01 03:13")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 0

def test_filter_date_range_g_approach_in_data_w_filtered_t_found(neos_db):
    filters = create_filters(start_date="1900-Jan-01 03:13", end_date="1900-Jan-01 05:01")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 2

def test_filter_max_distance_g_approach_in_data_w_filtered_t_found(neos_db):
    filters = create_filters(distance_max="0.39")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 4

def test_filter_min_distance_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(distance_min="0.388708125934362")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 2

def test_filter_max_velocity_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(velocity_max="16.7523040362574")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 4

def test_filter_min_velocity_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(velocity_min="16.7523040362574")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 2

def test_filter_max_diameter_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(diameter_max="1")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 0

def test_filter_min_diameter_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(diameter_min="1")
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 1

def test_filter_hazardous_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(hazardous=True)
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 2

def test_filter_not_hazardous_g_approach_in_data_w_filtered_t_found(neos_db, approach_170903):
    filters = create_filters(hazardous=False)
    filtered_approaches = neos_db._approaches
    for f in filters:
        filtered_approaches = filter(f, filtered_approaches)
    approaches = list(filtered_approaches)
    assert len(approaches) == 3


def test_limit_output_g_some_approaches_w_limited_t_reduced(neos_db, approach_170903):
    n = 3
    shorted = limit(neos_db._approaches, n)
    assert len(list(shorted)) == n

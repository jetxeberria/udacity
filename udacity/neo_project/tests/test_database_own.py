import pytest
from os.path import dirname, join
from pathlib import Path
from models import NearEarthObject, CloseApproach
from database import NEODatabase
from extract import load_approaches, load_neos
from filters import create_filters
from helpers import do_datetime

PROJECT_PATH = dirname(dirname(dirname(__file__)))
PROJECT_HELPERS = Path(PROJECT_PATH, "tests", "helpers", "neo_project")
TEST_NEO_FILE = join(PROJECT_HELPERS, 'neos_reduced.csv')
TEST_CAD_FILE = join(PROJECT_HELPERS, 'cad_reduced.json')
NEO_PROJECT = Path(PROJECT_PATH, "udacity", "neo_project", "data")
REAL_NEO_FILE = join(NEO_PROJECT, 'neos.csv')
REAL_CAD_FILE = join(NEO_PROJECT, 'cad.json')
TEST_NEO_PROJECT = Path(PROJECT_PATH, "neo_project", "tests")
TEST_NEO_FILE = join(TEST_NEO_PROJECT, 'test-neos-2020.csv')
TEST_CAD_FILE = join(TEST_NEO_PROJECT, 'test-cad-2020.json')


@pytest.fixture
def neos():
    neos = load_neos(TEST_NEO_FILE)
    return neos


@pytest.fixture
def approaches():
    approaches = load_approaches(TEST_CAD_FILE)
    return approaches


@pytest.fixture
def neos_db(neos, approaches):
    return NEODatabase(neos, approaches)


@pytest.fixture
def real_neos_db():
    neos = load_neos(REAL_NEO_FILE)
    approaches = load_approaches(REAL_CAD_FILE)
    return NEODatabase(neos, approaches)


def assert_approaches_in_range(
        filtered_approaches, start_date="2020-01-01", end_date="2020-12-31"):
    start_date = do_datetime(start_date)
    end_date = do_datetime(end_date)
    in_range = []
    for approach in filtered_approaches:
        if end_date >= approach.time.date() >= start_date:
            in_range.append(True)
        else:
            in_range.append(False)
    return all(in_range)


def test_db_g_matchable_data_w_build_t_all_approach_linked(neos, approaches):
    db = NEODatabase(neos, approaches)
    assert all(a.neo for a in db._approaches)


@pytest.mark.skip(reason="Using real data (big)")
def test_db_g_matchable_data_w_build_t_all_approach_linked(neos, approaches):
    neos = load_neos(REAL_NEO_FILE)
    approaches = load_approaches(REAL_CAD_FILE)
    db = NEODatabase(neos, approaches)
    assert all(a.neo for a in db._approaches)


@pytest.mark.skip(reason="Using real data (big)")
def test_searching_g_neos_w_search_by_name_t_found(real_neos_db):
    name = "Halley"
    neo = real_neos_db.get_neo_by_name(name)
    assert neo.name == name


def test_searching_g_neos_w_search_by_designation_t_found(neos_db):
    designation = "7088"
    neo = neos_db.get_neo_by_designation(designation)
    assert neo.designation == designation


def test_query_g_approaches_w_empty_query_t_nothing_found(neos_db):
    approaches = neos_db.query()
    assert not list(approaches)


def test_query_g_approaches_w_query_t_found(neos_db):
    filters = create_filters(hazardous=False)
    approaches = neos_db.query(filters)
    assert len(list(approaches)) == 3


def test_query_g_start_date_w_filtered_t_found(real_neos_db):
    filters = create_filters(start_date="2020-01-01", end_date="2020-12-31")
    filtered_approaches = real_neos_db.query(filters)
    assert_approaches_in_range(
        filtered_approaches, start_date="2020-01-01", end_date="2020-12-31")

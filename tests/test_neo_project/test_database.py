
import pytest
from os.path import dirname, join
from pathlib import Path

from udacity.neo_project import main
from udacity.neo_project.models import NearEarthObject, CloseApproach
from udacity.neo_project.database import NEODatabase
from udacity.neo_project.extract import load_approaches, load_neos

PROJECT_PATH = dirname(dirname(dirname(__file__)))
PROJECT_HELPERS = Path(PROJECT_PATH, "tests", "helpers", "neo_project")
TEST_NEO_FILE = join(PROJECT_HELPERS, 'neos_reduced.csv')
TEST_CAD_FILE = join(PROJECT_HELPERS,'cad_reduced.json')
NEO_PROJECT = Path(PROJECT_PATH, "udacity", "neo_project", "data")
REAL_NEO_FILE = join(NEO_PROJECT, 'neos.csv')
REAL_CAD_FILE = join(NEO_PROJECT,'cad.json')

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

def test_db_g_matchable_data_w_build_t_all_approach_linked(neos, approaches):
    db = NEODatabase(neos, approaches)
    assert all(a.neo for a in db._approaches)

def test_db_g_matchable_data_w_build_t_all_approach_linked(neos, approaches):
    neos = load_neos(REAL_NEO_FILE)
    approaches = load_approaches(REAL_CAD_FILE)
    db = NEODatabase(neos, approaches)
    assert all(a.neo for a in db._approaches)

def test_searching_g_neos_w_search_by_name_t_found(real_neos_db):
    name = "Halley"
    neo = real_neos_db.get_neo_by_name(name)
    assert neo.name == name

def test_searching_g_neos_w_search_by_designation_t_found(neos_db):
    designation = "7088"
    neo = neos_db.get_neo_by_designation(designation)
    assert neo.designation == designation

import pytest
from os.path import dirname, join
from pathlib import Path

from udacity.neo_project.database import NEODatabase
from udacity.neo_project.models import NearEarthObject, CloseApproach
from udacity.neo_project.extract import load_approaches, load_neos

PROJECT_PATH = dirname(dirname(dirname(dirname(__file__))))
PROJECT_HELPERS = Path(PROJECT_PATH, "udacity", "neo_project")
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
def neo_170903():
    return NearEarthObject(
        "170903", 
        None, 
        None, 
        True)

@pytest.fixture
def approach_170903(neo_170903):
    approach = CloseApproach(
        "170903", 
        "1900-Jan-01 00:11", 
        "0.0921795123769547", 
        "16.7523040362574")
    approach.neo = neo_170903
    return approach


@pytest.fixture
def fake_neo():
    return NearEarthObject("1", None, "100.0", True)

@pytest.fixture
def other_neo():
    return NearEarthObject("2", "20.0", None, True)

@pytest.fixture
def fake_approaches(other_neo, fake_neo):
    approach1 = CloseApproach(
        "fake1", 
        "1900-Jan-01 00:11", 
        "1", 
        "1")
    approach1.neo = fake_neo
    approach2 = CloseApproach(
        "fake2", 
        "2000-Jan-01 00:11", 
        "2", 
        "2")
    approach2.neo = other_neo
    return (a for a in [approach1, approach2])

@pytest.fixture
def neos_db(neos, approaches):
    return NEODatabase(neos, approaches)
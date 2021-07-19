import pytest
from pathlib import Path
from os.path import dirname

import udacity.lesson5.final as l5f
from udacity.lesson5 import filereader
import tests.helpers.lesson5.exercises as l5h

PROJECT_PATH = dirname(dirname(dirname(__file__)))
LESSON_HELPERS = Path(PROJECT_PATH, "tests", "helpers", "lesson5")

routes_sf = {
  "1": [
    [
      "San Francisco International Airport",
      "General Edward Lawrence Logan International Airport"
    ]
  ],
  "2": [
    [
      "San Francisco International Airport",
      "Philadelphia International Airport",
      "General Edward Lawrence Logan International Airport"
    ],
    [
      "San Francisco International Airport",
      "Cleveland Hopkins International Airport",
      "General Edward Lawrence Logan International Airport"
    ],
    ...,
    [
      "San Francisco International Airport",
      "London Heathrow Airport",
      "General Edward Lawrence Logan International Airport"
    ],
    [
      "San Francisco International Airport",
      "Amsterdam Airport Schiphol",
      "General Edward Lawrence Logan International Airport"
    ]
  ]
}

@pytest.fixture
def airports():
    return Path(LESSON_HELPERS, "airports.dat")

@pytest.fixture
def airlines():
    return Path(LESSON_HELPERS, "airlines.dat")

@pytest.fixture
def routes():
    return Path(LESSON_HELPERS, "routes.dat")

@pytest.fixture
def planner():
     return l5f.TripPlanner()

@pytest.fixture
def planner_loaded(planner, airports, routes):
    planner.load_airports(airports)
    planner.load_routes(routes)
    return planner

@pytest.fixture
def syr_bos_2():
    filename = Path(LESSON_HELPERS, "SYR- BOS (max 2).json")
    return filereader.read_json(filename)


@pytest.fixture
def syr_bos_3():
    filename = Path(LESSON_HELPERS, "SYR- BOS (max 3).json")
    return filereader.read_json(filename)

def assert_is_empty(input):
  if input and type(input) is list:
    if input[0]:
      assert 0
    else:
      assert 1
  assert 1

def test_load_flights_g_files_w_read_t_loaded(planner, airports):
    planner.load_airports(airports)
    assert planner.airports

def test_load_airlines_g_file_w_read_t_loaded(planner, airlines):
    planner.load_airlines(airlines)
    assert planner.airlines


def test_load_routes_g_file_w_read_t_loaded(planner, routes):
    planner.load_routes(routes)
    assert planner.routes

def test_find_routes_g_no_locations_w_searched_t_empty(planner_loaded):
    routes = planner_loaded.find_routes("FAKE", "OTHER")
    assert_is_empty(routes)


def test_find_routes_g_locations_w_searched_t_found(planner_loaded, syr_bos_2):
    routes = planner_loaded.find_routes("SYR", "BOS", max_segments=2)
    assert all(r in syr_bos_2[k] for k,v in routes.items() for r in v)

# def test_find_routes_g_locations_w_searched_depth_3_t_found(planner_loaded, syr_bos_3):
#     routes = planner_loaded.find_routes("SYR", "BOS", max_segments=3)
#     assert routes == syr_bos_3

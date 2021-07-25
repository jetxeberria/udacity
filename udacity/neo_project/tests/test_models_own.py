
import pytest

from models import NearEarthObject, CloseApproach
from helpers import InvalidInputDataError
from tests.helpers import fake_neo, fake_approaches, other_neo


@pytest.fixture
def valid_neo():
    args = {
        "designation": '433',
        "name": 'Eros',
        "diameter": 16.84,
        "hazardous": False
    }
    return args


@pytest.fixture
def invalid_neo():
    args = {
        "designation": None,
        "name": 433,
        "diameter": "16.84",
        "hazardous": "Don't know"
    }
    return args


@pytest.fixture
def valid_approach():
    args = {
        "designation": "170903",
        "time": "1900-Jan-01 00:11",
        "distance": 0.0921795123769547,
        "velocity": 16.7523040362574
    }
    return args


@pytest.fixture
def invalid_approach():
    args = {
        "time": 10,
        "distance": "a lot",
        "velocity": "hiperfast"
    }
    return args


def test_neo_creation_g_valid_attributes_w_create_t_all_attributes(valid_neo):
    neo = NearEarthObject(**valid_neo)
    assert neo.fullname == f"{valid_neo['designation']} ({valid_neo['name']})"


def test_neo_creation_g_invalid_attributes_w_create_t_type_error(invalid_neo):
    with pytest.raises(InvalidInputDataError):
        neo = NearEarthObject(**invalid_neo)


def test_approach_creation_g_valid_attributes_w_create_t_all_attributes(
        valid_approach):
    approach = CloseApproach(**valid_approach)
    assert approach.distance == valid_approach["distance"]


def test_approach_creation_g_invalid_distance_w_create_t_type_error(
        valid_approach):
    invalid_approach_distance = {**valid_approach}
    invalid_approach_distance["distance"] = "A lot"
    with pytest.raises(InvalidInputDataError):
        approach = CloseApproach(**invalid_approach_distance)


@pytest.mark.parametrize(
    "time", [10, "Four hours"]
)
def test_approach_creation_g_invalid_time_w_create_t_type_error(
        valid_approach, time):
    invalid_approach_time = {**valid_approach}
    invalid_approach_time["time"] = time
    with pytest.raises(InvalidInputDataError):
        approach = CloseApproach(**invalid_approach_time)


@pytest.mark.parametrize(
    "time", ["1900-Jan-01", "1900-01-01", "1900-01-01 00:11"]
)
def test_approach_creation_g_valid_time_w_create_t_type_error(
        valid_approach, time):
    valid = {**valid_approach}
    valid["time"] = time
    approach = CloseApproach(**valid)


def test_serialization_g_neo_w_serialize_t_relevant_dictionary(fake_neo):
    expected = {
        "designation": "1",
        "name": None,
        "diameter_km": 100.0,
        "potentially_hazardous": True,
        "approaches": []}
    serialized = fake_neo.serialize()
    assert serialized.items() == expected.items()


def test_serialization_g_approach_w_serialize_t_relevant_dictionary(
        fake_approaches, fake_neo):
    expected = {
        '_designation': 'fake1',
        'datetime_utc': "1900-Jan-01 00:11",
        'distance_au': 1.0,
        'velocity_km_s': 1.0,
        'neo': fake_neo}
    serialized = list(fake_approaches)[0].serialize()
    assert serialized.items() == expected.items()

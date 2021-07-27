"""Extract data on NEOs and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of
`NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the
command line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""

from typing import Union, List
from pathlib import Path

from models import NearEarthObject, CloseApproach
from helpers import read_csv, read_json


def load_neos(neo_csv_path: Union[Path, str]) -> List[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about
    near-Earth objects, well in Path-like or string format.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    neos_raw = read_csv(neo_csv_path, header=True)
    for neo in neos_raw:
        neos.append(NearEarthObject(
            neo["pdes"], neo["name"], neo["diameter"], neo["pha"]))

    return neos


def load_approaches(cad_json_path: Union[Path, str]) -> List[CloseApproach]:
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close
    approaches, well in Path-like or string format.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    approaches_raw = read_json(cad_json_path)
    fields = approaches_raw["fields"]
    des_index = fields.index("des")
    time_index = fields.index("cd")
    dist_index = fields.index("dist")
    vel_index = fields.index("v_rel")
    for approach in approaches_raw["data"]:
        approaches.append(CloseApproach(
            approach[des_index],
            approach[time_index],
            approach[dist_index],
            approach[vel_index]))

    return approaches

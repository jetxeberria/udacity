"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    fieldnames = (
        'datetime_utc',
        'distance_au',
        'velocity_km_s',
        'designation',
        'name',
        'diameter_km',
        'potentially_hazardous'
    )

    with open(filename, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            output = build_output(result)
            writer.writerow(output)


def build_output(result):
    """Return a selection of fields of an approach and its neo."""
    approach = result.serialize()
    neo = approach["neo"].serialize()
    del approach["_designation"]
    del approach["neo"]
    del neo["approaches"]

    return {**approach, **neo}


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is
    a list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    output = []
    with open(filename, "w") as f:
        for result in results:
            approach = result.serialize()
            neo = approach["neo"].serialize()
            del approach["_designation"]
            del approach["neo"]
            del neo["approaches"]
            line = {**approach, "neo": {**neo}}
            output.append(line)
        json.dump(output, f, indent=2, sort_keys=True)

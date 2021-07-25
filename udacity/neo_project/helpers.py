"""Convert datetimes to and from strings.

NASA's dataset provides timestamps as naive datetimes (corresponding to UTC).

The `cd_to_datetime` function converts a string, formatted as the `cd` field
of NASA's close approach data, into a Python `datetime`

The `datetime_to_str` function converts a Python `datetime` into a string.
Although `datetime`s already have human-readable string representations, those
representations display seconds, but NASA's data (and our datetimes!) don't
provide that level of resolution, so the output format also will not.
"""
import datetime
import json
import csv
from re import match

from errors import InvalidInputDataError


def cd_to_datetime(calendar_date):
    """Convert a NASA-formatted calendar date/time description into a
    datetime.

    NASA's format, at least in the `cd` field of close approach data, uses the
    English locale's month names. For example, December 31st, 2020 at noon is:

        2020-Dec-31 12:00

    This will become the Python object
    `datetime.datetime(2020, 12, 31, 12, 0)`.

    :param calendar_date: A calendar date in YYYY-bb-DD hh:mm format.
    :return: A naive `datetime` corresponding to the given calendar date and
    time.
    """
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")


def timestamp_to_datetime(timestamp):
    fmt = ''
    if len(timestamp) == 19:
        fmt = "%Y-%m-%d %H:%M:%S"
        return datetime.datetime.strptime(timestamp, fmt)
    elif len(timestamp) == 16:
        fmt = "%Y-%m-%d %H:%M"
        return datetime.datetime.strptime(timestamp, fmt)
    elif len(timestamp) == 11:
        fmt = "%Y-%b-%d"
    elif len(timestamp) == 10:
        fmt = "%Y-%m-%d"
    time = datetime.datetime.strptime(timestamp, fmt)
    return time.date()


def datetime_to_str(dt):
    """Convert a naive Python datetime into a human-readable string.

    The default string representation of a datetime includes seconds; however,
    our data isn't that precise, so this function only formats the year,
    month, date, hour, and minute values. Additionally, this function
    provides the date in the usual ISO 8601 YYYY-MM-DD format to avoid
    ambiguities with locale-specific month names.

    :param dt: A naive Python datetime.
    :return: That datetime, as a human-readable string without seconds.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")


def do_bool(value, allow_none=True):
    assertion_values = [
        "1", "True", "true", "TRUE", "Y", "y", "Yes", "yes", "YES", 1, True]
    negation_values = [
        "0", "False", "false", "FALSE", "N", "n", "No", "no", "NO", 0, False]
    if value in assertion_values:
        return True
    elif value in negation_values:
        return False
    elif value == '':
        return False
    elif allow_none and value is None:
        return None
    else:
        raise InvalidInputDataError(
            f"Given argument '{value}' can't be interpreted as boolean")


def do_float(value):
    try:
        return float(value) if value else float("nan")
    except (ValueError, TypeError) as exc:
        raise InvalidInputDataError(
            f"Given argument '{value}' can't be interpreted as float", exc)


def do_datetime(value):
    try:
        if value:
            if type(value) in [datetime.datetime, datetime.date]:
                return value
            return cd_to_datetime(value)
        return None
    except (ValueError, TypeError) as exc:
        try:
            return timestamp_to_datetime(value)
        except (ValueError, TypeError) as exc:
            raise InvalidInputDataError(
                f"Given argument '{value}' can't be interpreted as datetime",
                exc)


def read_json(filename):
    with open(filename, "r") as f:
        contents = json.load(f)
    return contents


def read_csv(filename, header=False):
    with open(filename, 'r') as f:
        contents = []
        if header:
            reader = csv.DictReader(f)
            contents = list(reader)
        else:
            reader = csv.reader(f)
            for line in reader:
                contents.append(line)
    return contents

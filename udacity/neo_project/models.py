"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from enum import Enum
from typing import Union, List
import datetime

from helpers import (do_bool, do_float, do_datetime)


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(
        self,
        designation: str,
        name: str,
        diameter: float,
        hazardous: bool
    ) -> None:
        """Create a new `NearEarthObject`.

        :param designation: Designation of NEO
        :param name: Name of NEO, optional
        :param diameter: Diameter of NEO in km
        :param hazardous: Whether the NEO is or not hazardous
        """
        self.designation = str(designation) if designation else ''
        self.name = str(name) if name else None
        self.diameter = do_float(diameter)
        self.hazardous = do_bool(hazardous)

        self.approaches: List[CloseApproach] = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            fullname = f"{self.designation} ({self.name})"
        else:
            fullname = self.designation
        return fullname

    def __str__(self):
        """Return `str(self)`."""
        hazardous = "is"
        if self.hazardous is False:
            hazardous = "is not"
        elif self.hazardous is None:
            hazardous = "there is no info about if it is"
        msg = f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km "
        hazardous_msg = f"and {hazardous} potentially hazardous."
        return msg + hazardous_msg

    def __repr__(self):
        """Return `repr(self)`.
        
        Return a computer-readable string representation of this object.
        """
        return (f"NearEarthObject(designation={self.designation!r}, "
                f"name={self.name!r}, diameter={self.diameter:.3f}, "
                f"hazardous={self.hazardous!r})")

    def serialize(self):
        """Return object attributes as a dictionary.
        
        Return a dictionary with the object attributes being their names
        the keys
        """
        serialized = {k: v for k, v in self.__dict__.items()}
        serialized["name"] = serialized["name"] if serialized["name"] else ''
        serialized["potentially_hazardous"] = serialized["hazardous"]
        del serialized["hazardous"]
        serialized["diameter_km"] = serialized["diameter"]
        del serialized["diameter"]
        return serialized


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach, the
    nominal approach distance in astronomical units, and the relative approach
    velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(
            self,
            designation: str,
            time: str,
            distance: float,
            velocity: float):
        """Create a new `CloseApproach`.

        :param designation: Designation of NEO that approaches
        :param time: Time of approach
        :param distance: Mean distance of approach
        :param velocity: Velocity of NEO when approach
        """
        self._designation = designation
        self.time = do_datetime(time)
        self.distance = do_float(distance)
        self.velocity = do_float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo: Union[NearEarthObject, None] = None

    @property
    def time_str(self):
        """Return a formatted representation of the approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return self.time.isoformat(sep=u"\u0020")[:-3]

    def __str__(self):
        """Return `str(self)`."""
        time_formatted = self.time_str
        hazardous = ""
        if self.neo.hazardous is False:
            hazardous = "not "
        elif self.neo.hazardous is None:
            hazardous = "no info about if it is "
        msg = f"On {self.time_str}, '{self.neo.fullname}' "
        hazardous_msg = f"({hazardous}a PHA neo) approaches "
        approach_msg = f"Earth at a distance of {self.distance:.2f} au"
        velocity_msg = f" and a velocity of {self.velocity:.2f} km/s."
        return msg + hazardous_msg + approach_msg + velocity_msg

    def __repr__(self):
        """Return `repr(self)`.
        
        Return a computer-readable string representation of this object.
        """
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """Return object attributes as a dictionary.
        
        Return a dictionary with the object attributes being their names
        the keys
        """
        serialized = {k: v for k, v in self.__dict__.items()}
        serialized["datetime_utc"] = serialized["time"].strftime(
            "%Y-%m-%d %H:%M")
        del serialized["time"]
        serialized["distance_au"] = serialized["distance"]
        del serialized["distance"]
        serialized["velocity_km_s"] = serialized["velocity"]
        del serialized["velocity"]
        return serialized

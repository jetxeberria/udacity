#!/usr/bin/env python

"""Tests for `udacity` package."""
import udacity

def test_package_publishes_version_info():
    """Tests that the `udacity` publishes the current verion"""

    assert hasattr(udacity, '__version__')

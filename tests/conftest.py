# -*- coding: utf-8 -*-
"""
The aim of this configuration is to avoid running certain tests
https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
"""

import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests")

#pylint: disable=C0201
def pytest_collection_modifyitems(config, items):
    """Modify test description at runtime"""

    skippable = {}
    if not config.getoption("--runslow"):
        skippable["slow"] = pytest.mark.skip(reason="need --runslow option to run")

    for item in items:
        for skip in skippable.keys():
            if skip in item.keywords:
                item.add_marker(skippable[skip])

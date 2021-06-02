import pytest

from udacity import lesson_3 as l3
from tests.helpers.lesson_3 import printer

def mocked_print():
    printer.fake_print()

@pytest.mark.parametrize(
    "name, surnames, details, printed",
    [
        (
        "Sam", 
        [],
        {},
        "Sam\n"
        ),
        (
        "Sam", 
        [],
        {"role": 'Instructor'},
        "Sam\nrole: Instructor\n"
        ),
        (
        "Martin", 
        ['Luther', 'King', 'Jr'],
        {"born": 1929, "died": 1968},
        "Martin Luther King Jr\nborn: 1929\ndied: 1968\n"
        ),
        (
        "Sebastian", 
        ['Thrun'],
        {"cofounded": "Udacity", "experience": "Stanford Professor"},
        "Sebastian Thrun\ncofounded: Udacity\nexperience: Stanford Professor\n"
        ),
    ]
)
def test_given_args_when_printing_then_printed(name, surnames, details, printed, capsys):
    l3.create_profile(name, *surnames, **details)
    captured = capsys.readouterr()
    assert captured.out == printed

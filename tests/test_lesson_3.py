import pytest

from udacity import lesson_3 as l3
from udacity import lesson_3_solutions as l3s
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

@pytest.fixture
def print_args():
    return ["one", "two", "three"]

@pytest.fixture
def print_kwargs():
    return {"sep": ":", "end": "\n\n"}

@pytest.fixture
def sum_args():
    return [1, 2, 3]

@pytest.mark.parametrize(
    "target_fn, fake_args, fake_kwargs, output_fn",
    [
        (
            sum, 
            [[1, 2, 3]],
            {},
            6
        ),
        (
            print, 
            ["one", "two", "three"],
            {"sep": ":", "end": "\n\n"},
            None
        )
    ]
)
def test_given_function_when_cached_then_skipped(target_fn, fake_args, fake_kwargs, output_fn):
    cacher = l3.Cacher()
    fn = l3.memoize(target_fn, cacher)
    out1 = fn(*fake_args, **fake_kwargs)
    out2 = fn(*fake_args, **fake_kwargs)
    out3 = fn(*fake_args, **fake_kwargs)
    assert all( o == output_fn for o in [out1, out2, out3])
    assert len(cacher.all_cached) == 1

def test_given_function_when_cached_then_skipped():
    cacher = l3.Cacher()
    sum_fn = l3.memoize(sum, cacher)
    print_fn = l3.memoize(print, cacher)
    print_env = {
        "args": ["one", "two", "three"],
        "kwargs": {"sep": ":", "end": "\n\n"},
        "out": None
    }
    sum_env = {
        "args": [[1, 2, 3]],
        "out": 6
    }
    sum_out1 = sum_fn(*sum_env["args"])
    sum_out2 = sum_fn(*sum_env["args"])
    print_out = print_fn(*print_env["args"], **print_env["kwargs"])
    assert all( o == sum_env["out"] for o in [sum_out1, sum_out2])
    assert print_env["out"] == print_out
    assert len(cacher.all_cached) == 2

def test_given_function_when_same_args_then_cach():
    cacher = l3.Cacher()
    sum_fn = l3.memoize(sum, cacher)
    list_fn = l3.memoize(list, cacher)
    sum_env = {
        "args": [[1, 2, 3]],
        "out": 6
    }
    list_env = {
        "args": [[1, 2, 3]],
        "out": [1, 2, 3]
    }
    sum_out = sum_fn(*sum_env["args"])
    list_out = list_fn(*list_env["args"])
    assert list_env["out"] == list_out
    assert sum_env["out"] == sum_out
    assert len(cacher.all_cached) == 2

@pytest.mark.skip(reason="Udacity solution is elegant but not versatile")
def test_given_solution_function_when_same_args_then_cach():
    # cacher = l3.Cacher()
    sum_fn = l3s.memoize(sum)
    list_fn = l3s.memoize(list)
    sum_env = {
        "args": [[1, 2, 3]],
        "out": 6
    }
    list_env = {
        "args": [[1, 2, 3]],
        "out": [1, 2, 3]
    }
    sum_out = sum_fn(*sum_env["args"])
    list_out = list_fn(*list_env["args"])
    assert list_env["out"] == list_out
    assert sum_env["out"] == sum_out
    assert len(cacher.all_cached) == 2

@pytest.mark.skip
def test_given_args_in_cache_when_searched_for_then_found(fake_args, fake_kwargs):
    l3.memoize.cached = []
    l3.are_in_cache(fake_args, fake_kwargs)
    assert 0

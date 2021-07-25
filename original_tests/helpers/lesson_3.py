import pytest

class FakePrinter():
    def __init__(self, tmp_path) -> None:
        self.printed_file = tmp_path / "printed.txt"
        self.printed_file.write_text("")
    
    def fake_print(self, *args):
        print("fake print")
        print(*args)
        self.printed_file.write_text(*args)

    def assert_is_printed(self, expected_output):
        assert self.printed_file.read_text() == expected_output            

@pytest.fixture
def printer(tmp_path):
    return FakePrinter(tmp_path)
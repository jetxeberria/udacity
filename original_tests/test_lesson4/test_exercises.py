import pytest
from udacity.lesson4 import exercises as l4e

@pytest.mark.parametrize(
    "name, password, message",
    [
        ("jim", "jam", "")
    ]
)
def test_g_god_credentials_w_create_account_t_ok(name, password, message, capsys):
    l4e.create_account(name, password)
    captured = capsys.readouterr()
    assert captured.out == message


@pytest.mark.parametrize(
    "name, password, message",
    [
        ('admin', 'password', "Password given is invalid\n"),
        ('guest', 'guest', "Password given is invalid\n"),
    ]
)
def test_g_bad_credentials_w_create_account_t_error(name, password, message, capsys):
    with pytest.raises(l4e.InvalidPasswordError):
        l4e.create_account(name, password)
    captured = capsys.readouterr()
    assert captured.out == message
"""Tests for credential storage.

These cover the guarantees the account system relies on: passwords are never
persisted or exposed in a readable form, and every stored hash is individually
salted.
"""
import pytest

from models import User
from utils import ValidationError, authenticate

PLAINTEXT = "correct horse battery"


@pytest.fixture
def user():
    return User(id=1, name="john", password=PLAINTEXT, email="john@example.com")


def test_password_is_not_stored_in_plaintext(user):
    assert user.password_hash != PLAINTEXT
    assert PLAINTEXT not in user.password_hash


def test_stored_value_is_a_recognised_hash(user):
    # Werkzeug hashes are self-describing: "<algorithm>:<params>$<salt>$<digest>".
    algorithm, _, remainder = user.password_hash.partition("$")
    assert algorithm.split(":")[0] in {"pbkdf2", "scrypt", "argon2"}
    assert remainder


def test_correct_password_is_accepted(user):
    assert user.check_password(PLAINTEXT) is True


def test_wrong_password_is_rejected(user):
    assert user.check_password("wrong") is False
    assert user.check_password(PLAINTEXT.upper()) is False
    assert user.check_password("") is False


def test_missing_hash_does_not_raise(user):
    # A row with no stored credential must fail closed rather than error.
    user.password_hash = None
    assert user.check_password(PLAINTEXT) is False


def test_identical_passwords_get_different_hashes():
    # Per-user salting: two accounts sharing a password must not share a hash,
    # otherwise a single precomputed table would crack both at once.
    a = User(id=1, name="a", password=PLAINTEXT, email="a@example.com")
    b = User(id=2, name="b", password=PLAINTEXT, email="b@example.com")

    assert a.password_hash != b.password_hash
    assert a.check_password(PLAINTEXT)
    assert b.check_password(PLAINTEXT)


def test_set_password_replaces_the_previous_credential(user):
    original = user.password_hash

    user.set_password("a brand new password")

    assert user.password_hash != original
    assert user.check_password("a brand new password") is True
    assert user.check_password(PLAINTEXT) is False


def test_to_dict_exposes_no_credential(user):
    # to_dict() is what gets written into the Flask session cookie, which is
    # signed but not encrypted - anything in here is readable by the client.
    payload = user.to_dict()

    assert "password" not in payload
    assert "password_hash" not in payload
    assert user.password_hash not in repr(payload)


def test_repr_exposes_no_credential(user):
    # repr() is what ends up in log files and tracebacks.
    assert user.password_hash not in repr(user)
    assert PLAINTEXT not in repr(user)


def test_authenticate_verifies_against_the_hash():
    users = [
        User(id=1, name="john", password="test1", email="john@example.com"),
        User(id=2, name="emma", password="test2", email="emma@example.com"),
    ]

    matched, error = authenticate("john", "test1", users)
    assert error is None
    assert matched.id == 1

    assert authenticate("john", "test2", users)[1] == ValidationError("password", "Wrong Password")
    assert authenticate("nobody", "test1", users)[1] == ValidationError(
        "username", "Wrong Username"
    )

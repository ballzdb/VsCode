# test_r6wins.py
import pytest
from r6wins import Attacker, Defender, get_operator_of_this_round  # ← change filename if needed

@pytest.fixture(autouse=True)
def reset():
    pass  # nothing to reset here


def test_ash():
    assert Attacker("Ash").name == "Ash"


def test_jager():
    assert Defender("Jäger").name == "Jäger"


def test_bad_name_crashes():
    with pytest.raises(ValueError):
        Attacker("lol")


def test_get_operator(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda p: "Ash")
    op = get_operator_of_this_round()
    assert op.name == "Ash"
    assert isinstance(op, Attacker)


def test_get_operator_wrong(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda p: "NotReal")
    with pytest.raises(ValueError):
        get_operator_of_this_round()
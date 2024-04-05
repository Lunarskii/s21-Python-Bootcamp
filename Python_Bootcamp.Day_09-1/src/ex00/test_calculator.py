from calculator import add, sub, mul, div
import pytest


def test_add():
    assert add(1, 2) == 3
    assert add(1.5, 1.5) == 3.0
    assert add(0, 2) == 2
    assert add(2, 2.5) == 4.5


def test_sub():
    assert sub(3, 2) == 1
    assert sub(4.5, 1.5) == 3.0
    assert sub(1, 2) == -1


def test_mul():
    assert mul(14, 21) == 294
    assert mul(1.5, 1.5) == 2.25
    assert mul(1, 0) == 0


def test_div():
    assert div(2, 4) == 0.5
    assert div(10, 10) == 1
    assert div(4.5, 1.5) == 3
    with pytest.raises(ZeroDivisionError):
        div(1, 0)

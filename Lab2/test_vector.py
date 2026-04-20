import pytest
from vector_math import Vector

def test_creation():
    v = Vector(1, 2, 3)
    assert v.coords == (1.0, 2.0, 3.0)
    assert len(v) == 3

def test_add():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    assert v1 + v2 == Vector(4, 6)

def test_add_dimension_mismatch():
    v1 = Vector(1, 2)
    v2 = Vector(1, 2, 3)
    with pytest.raises(ValueError):
        v1 + v2

def test_mul_scalar():
    v = Vector(1, 2, 3)
    assert v * 2 == Vector(2, 4, 6)
    assert 3 * v == Vector(3, 6, 9)

def test_dot_product():
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    assert v1 * v2 == 32.0

def test_norm():
    v = Vector(3, 4)
    assert v.norm == 5.0

def test_str_repr():
    v = Vector(1, 2.5, 3)
    assert str(v) == "Vector(1, 2.5, 3)"
    assert repr(v) == "Vector(1.0, 2.5, 3.0)"
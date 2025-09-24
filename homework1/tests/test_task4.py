from task4 import calculate_discount
import pytest

def test_discount_with_integers():
    assert calculate_discount(100, 10) == 90
    assert calculate_discount(200, 50) == 100
    assert calculate_discount(50, 0) == 50

def test_discount_with_floats():
    assert calculate_discount(100.0, 10.0) == 90.0
    assert calculate_discount(99.99, 5.5) == pytest.approx(94.49055)
    assert calculate_discount(250.75, 25.0) == pytest.approx(188.0625)

def test_mixed_types():
    assert calculate_discount(100, 12.5) == 87.5
    assert calculate_discount(150.5, 20) == pytest.approx(120.4)

def test_invalid_discount():
    with pytest.raises(ValueError):
        calculate_discount(100, -10)
    with pytest.raises(ValueError):
        calculate_discount(100, 110)
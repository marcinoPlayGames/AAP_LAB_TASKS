import pytest
from product import Product


@pytest.fixture
def product():
    return Product("Laptop", 2999.99, 10)


def test_is_available(product):
    assert product.is_available() == True


@pytest.mark.parametrize("amount, expected_quantity", [
    (5, 15),
    (0, 10),
    (2, 12),
])
def test_add_stock_parametrized(product, amount, expected_quantity):
    product.add_stock(amount)
    assert product.quantity == expected_quantity


def test_remove_stock_too_much_raises(product):
    with pytest.raises(ValueError):
        product.remove_stock(20)
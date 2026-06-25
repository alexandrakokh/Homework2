import pytest
from src.shop_models import Product, Category


def setup_function():
    """Сбрасываем глобальные счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


# --- Тесты для Product ---


def test_product_initialization():
    p = Product("Test Phone", "Описание теста", 1000.50, 10)
    assert p.name == "Test Phone"
    assert isinstance(p.price, float)
    assert p.price == 1000.5
    assert p.quantity == 10


def test_setter_valid_price():
    p = Product("Book", "Good book", 100.0, 5)
    old_price = p.price
    p.price = 200.5
    assert p.price == 200.5
    assert p.price != old_price


def test_setter_zero_price_rejected(capfd):
    p = Product("Book", "Good book", 100.0, 5)
    old_price = p.price
    p.price = 0
    assert p.price == old_price
    out, err = capfd.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in out


def test_setter_negative_price_rejected(capfd):
    p = Product("Book", "Good book", 100.0, 5)
    old_price = p.price
    p.price = -50
    assert p.price == old_price
    out, err = capfd.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in out


def test_new_product_from_dict():
    data = {"name": "Новый Товар", "description": "Создан через класс-метод", "price": 999, "quantity": 7}
    p = Product.new_product(data)
    assert isinstance(p, Product)
    assert p.price == 999.0


# --- Тесты для Category ---


def test_products_property_format():
    p1 = Product.new_product({"name": "Смартфон", "description": "Cool", "price": 80, "quantity": 15})
    cat = Category("Электроника", "Гаджеты", [p1])
    report = cat.products
    expected = "Смартфон, 80 руб. Остаток: 15 шт.\n"
    assert report == expected


def test_add_product_updates_counter():
    p = Product("Item", "Desc", 100, 5)
    cat = Category("Cat", "Desc")

    assert Category.product_count == 0

    cat.add_product(p)

    assert Category.product_count == 1
    assert cat.products == "Item, 100 руб. Остаток: 5 шт.\n"


def test_multiple_products_in_products_property():
    p1 = Product.new_product({"name": "A", "description": "", "price": 10, "quantity": 1})
    p2 = Product.new_product({"name": "B", "description": "", "price": 20, "quantity": 2})
    cat = Category("Test", "Test", [p1, p2])

    report = cat.products
    assert "A, 10 руб. Остаток: 1 шт.\n" in report
    assert "B, 20 руб. Остаток: 2 шт.\n" in report


def test_empty_products_returns_empty_string():
    cat = Category("Empty", "Empty")
    assert cat.products == ""


def test_multiple_categories_stats():
    p1 = Product("A", "A", 10, 1)
    p2 = Product("B", "B", 20, 1)
    c1 = Category("C1", "C1", [p1])
    c2 = Category("C2", "C2", [p2])

    assert Category.product_count == 2
    assert Category.category_count == 2

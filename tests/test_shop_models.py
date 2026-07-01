import pytest
from src.shop_models import BaseProduct, Product, Smartphone, LawnGrass, Category


def test_base_product_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseProduct()


def test_product_initialization(capfd):
    p = Product("Test", "Desc", 100, 5)
    assert p.name == "Test"
    assert p.price == 100.0
    assert p.quantity == 5
    out, _ = capfd.readouterr()
    # Теперь строка совпадает: Product('Test', 'Desc', 100.0, 5)
    assert "Product('Test', 'Desc', 100.0, 5)" in out


def test_abstract_methods_implemented_in_product():
    p = Product("P", "Description", 50, 2)
    assert p.get_total_cost() == 100.0
    assert p.get_description_preview() == "Description"


def test_smartphone_inheritance_and_logging(capfd):
    s = Smartphone("iPhone", "Nice phone", 900, 3, ram_gb=8)
    assert s.ram_gb == 8
    assert s.get_total_cost() == 2700.0
    out, _ = capfd.readouterr()
    assert "Smartphone('iPhone', 'Nice phone', 900.0, 3)" in out


def test_lawn_grass_inheritance_and_logging(capfd):
    g = LawnGrass("Grass", "Good grass", 200, 4, area_coverage_m2=50.0)
    assert g.area_coverage_m2 == 50.0
    assert g.get_total_cost() == 800.0
    out, _ = capfd.readouterr()
    assert "LawnGrass('Grass', 'Good grass', 200.0, 4)" in out


def test_setter_valid_price(capfd):
    p = Product("Book", "Good book", 100.0, 5)
    p.price = 120.5
    assert p.price == 120.5


def test_setter_zero_price_rejected():
    p = Product("Book", "Good", 100.0, 5)
    with pytest.raises(ValueError):
        p.price = -1


def test_setter_negative_price_rejected():
    with pytest.raises(ValueError):
        Product("Book", "Good", -10, 5)


def test_new_product_from_dict(capfd):
    data = {"name": "Phone", "description": "Cool", "price": 80, "quantity": 15}
    p = Product.new_product(data)
    assert p.name == "Phone"
    assert p.price == 80.0
    assert p.quantity == 15
    out, _ = capfd.readouterr()
    assert "Product('Phone', 'Cool', 80.0, 15)" in out


def test_add_product_updates_counter():
    before = Product.get_counter()
    p = Product("Item", "Desc", 100, 5)
    after = Product.get_counter()
    assert after == before + 1


def test_product_add_two_products():
    a = Product("A", "Desc", 100, 10)
    b = Product("B", "Desc", 50, 5)
    c = a + b
    assert c.quantity == 15
    expected_price = (100 * 10 + 50 * 5) / 15
    assert abs(c.price - expected_price) < 1e-6


# Исправлено: проверяем, что 5 + p выбрасывает TypeError, а не возвращает NotImplemented
def test_product_radd_number_plus_product():
    p = Product("P", "Desc", 50, 5)
    with pytest.raises(TypeError):
        _ = 5 + p


# Исправлено: p + "string" тоже выбрасывает TypeError
def test_product_add_invalid_type_returns_not_implemented():
    p = Product("P", "Desc", 10, 1)
    with pytest.raises(TypeError):
        _ = p + "string"

def test_category_total_cost():
    p1 = Product("A", "Desc A", 100.0, 5)  # 500
    p2 = Product("B", "Desc B", 200.0, 3)  # 600
    cat = Category("Test", "Test cat", [p1, p2])
    assert cat.get_total_cost() == 1100.0

def test_category_str_representation():
    p = Product("Item", "Desc", 50.0, 4)  # 200
    cat = Category("Small", "Small cat", [p])
    # Проверяем, что в строке есть название, кол-во товаров и общая стоимость
    s = str(cat)
    assert "Small" in s
    assert "1 товаров" in s
    assert "200.00" in s or "200.0" in s  # зависит от форматирования
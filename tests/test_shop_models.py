from src.shop_models import Product, Category

def setup_function():
    """Сбрасываем глобальные счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


# --- Product ---

def test_product_initialization():
    p = Product("Test", "Desc", 100, 5)
    assert p.name == "Test"
    assert p.price == 100.0
    assert p.quantity == 5


def test_setter_valid_price():
    p = Product("Book", "Good book", 100.0, 5)
    p.price = 200.5
    assert p.price == 200.5


def test_setter_zero_price_rejected(capfd):
    p = Product("Book", "Good", 100.0, 5)
    p.price = 0
    out, _ = capfd.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in out


def test_setter_negative_price_rejected(capfd):
    p = Product("Book", "Good", 100.0, 5)
    p.price = -50
    out, _ = capfd.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in out


def test_new_product_from_dict():
    data = {"name": "Phone", "description": "Cool", "price": 80, "quantity": 15}
    p = Product.new_product(data)
    assert p.name == "Phone"
    assert p.price == 80.0
    assert p.quantity == 15


# --- Category ---

def test_products_property_format():
    p1 = Product.new_product({"name": "Смартфон", "description": "Cool", "price": 80, "quantity": 15})
    cat = Category("Электроника", "Гаджеты", [p1])
    report = cat.products
    # Без \n в конце: join делает переносы только между элементами
    expected = "Смартфон, 80 руб. Остаток: 15 шт."
    assert report == expected


def test_add_product_updates_counter():
    p = Product("Item", "Desc", 100, 5)
    cat = Category("Cat", "Desc")

    assert Category.product_count == 0

    cat.add_product(p)

    assert Category.product_count == 1
    expected = "Item, 100 руб. Остаток: 5 шт."
    assert cat.products == expected


def test_multiple_products_in_products_property():
    p1 = Product.new_product({"name": "A", "description": "", "price": 10, "quantity": 1})
    p2 = Product.new_product({"name": "B", "description": "", "price": 20, "quantity": 2})
    cat = Category("Test", "Test", [p1, p2])

    report = cat.products

    # Ожидаем, что обе строки есть, и разделены \n, но в конце нет \n
    assert "A, 10 руб. Остаток: 1 шт." in report
    assert "B, 20 руб. Остаток: 2 шт." in report
    assert report.count("\n") == 1  # ровно один перенос между двумя товарами


def test_empty_products_returns_empty_string():
    cat = Category("Empty", "Empty")
    assert cat.products == ""


def test_multiple_categories_stats():
    p1 = Product("A", "A", 10, 1)
    p2 = Product("B", "B", 20, 1)
    c1 = Category("C1", "C1", [p1])
    c2 = Category("C2", "C2", [p2])

    stats = Category.get_stats()
    assert "Всего категорий: 2" in stats
    assert "Всего товаров: 2" in stats


# --- __str__ для Category ---

def test_category_str_total_quantity():
    p1 = Product("A", "Desc", 10, 2)
    p2 = Product("B", "Desc", 20, 3)
    cat = Category("Test", "Test", [p1, p2])
    expected = "Test, количество продуктов: 5 шт."
    assert str(cat) == expected


def test_category_str_empty():
    cat = Category("Empty", "Empty")
    expected = "Empty, количество продуктов: 0 шт."
    assert str(cat) == expected


# --- __add__ для Product ---

def test_product_add_two_products():
    a = Product("A", "Desc", 100, 10)   # 1000
    b = Product("B", "Desc", 200, 2)   # 400
    assert a + b == 1400.0


def test_product_add_with_number():
    p = Product("P", "Desc", 50, 5)     # 250
    assert p + 200 == 450.0


def test_product_radd_number_plus_product():
    p = Product("P", "Desc", 50, 5)     # 250
    assert 300 + p == 550.0


def test_product_add_invalid_type_returns_not_implemented():
    p = Product("P", "Desc", 10, 1)
    # Вызываем __add__ напрямую: так мы видим именно то, что вернул метод,
    # а не финальную ошибку, которую сформировал интерпретатор.
    result = p.__add__("string")
    assert result is NotImplemented

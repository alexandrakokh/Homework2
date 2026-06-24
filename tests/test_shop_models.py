import unittest
from src.shop_models import Product, Category


class TestProduct(unittest.TestCase):
    """Тесты для класса Product"""

    def test_product_initialization(self):
        """Проверка корректной инициализации всех атрибутов"""
        p = Product("Test Phone", "Описание теста", 1000.50, 10)

        self.assertEqual(p.name, "Test Phone")
        self.assertEqual(p.description, "Описание теста")
        self.assertEqual(p.price, 1000.50)
        self.assertEqual(p.quantity, 10)

    def test_price_type_float(self):
        """Цена должна быть float, даже если передали int"""
        # Раньше этот тест падал, потому что 500 оставалось int.
        # Теперь float(500) превратит его в 500.0
        p = Product("Item", "Desc", 500, 5)
        self.assertIsInstance(p.price, float)
        self.assertEqual(p.price, 500.0)

    def test_quantity_type_int(self):
        """Количество должно быть int"""
        p = Product("Item", "Desc", 500.0, 5)
        self.assertIsInstance(p.quantity, int)


class TestCategory(unittest.TestCase):
    """Тесты для класса Category"""

    def setUp(self):
        """Сбрасываем счетчики перед каждым тестом для полной изоляции"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization_empty(self):
        """Создание категории без товаров"""
        cat = Category("Empty Cat", "No products here")

        self.assertEqual(cat.name, "Empty Cat")
        self.assertEqual(len(cat.products), 0)
        self.assertEqual(Category.category_count, 1)
        self.assertEqual(Category.product_count, 0)

    def test_category_initialization_with_products(self):
        """Создание категории со списком товаров"""
        p1 = Product("A", "Desc A", 10.0, 1)
        p2 = Product("B", "Desc B", 20.0, 2)

        cat = Category("Gadgets", "Cool stuff", products=[p1, p2])

        self.assertEqual(cat.name, "Gadgets")
        self.assertEqual(len(cat.products), 2)
        self.assertIn(p1, cat.products)
        self.assertIn(p2, cat.products)

        # Проверка счетчиков: 1 категория + 2 товара
        self.assertEqual(Category.category_count, 1)
        self.assertEqual(Category.product_count, 2)

    def test_add_product_updates_global_counter(self):
        """Метод add_product должен увеличивать общий счетчик товаров"""
        p1 = Product("X", "Desc X", 100.0, 1)
        cat = Category("Test Cat", "Desc")

        # До добавления счетчик товаров должен быть 0 (благодаря setUp)
        self.assertEqual(Category.product_count, 0)

        cat.add_product(p1)

        # После добавления
        self.assertEqual(len(cat.products), 1)
        self.assertEqual(Category.product_count, 1)  # Глобальный счетчик вырос

    def test_multiple_categories_stats(self):
        """Проверка работы счетчиков при создании нескольких категорий"""
        # Счетчики уже сброшены в setUp

        p1 = Product("P1", "D1", 10.0, 1)
        p2 = Product("P2", "D2", 20.0, 1)
        p3 = Product("P3", "D3", 30.0, 1)

        c1 = Category("Cat1", "Desc1", [p1, p2])  # 1 кат, 2 товара
        c2 = Category("Cat2", "Desc2", [p3])  # 2 кат, 3 товара всего

        self.assertEqual(Category.category_count, 2)
        self.assertEqual(Category.product_count, 3)

        # Проверка, что у каждой категории свой список, но счетчики общие
        self.assertEqual(len(c1.products), 2)
        self.assertEqual(len(c2.products), 1)

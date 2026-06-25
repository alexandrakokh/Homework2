from typing import List, Optional, Dict


class Product:
    def __init__(self, name: str, description: str, price, quantity: int):
        self.name: str = name
        self.description: str = description
        self.quantity: int = quantity

        # Приватный атрибут цены
        self.__price: float = 0.0

        # Используем сеттер для установки цены (он проверит значение)
        self.price = price

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, value) -> None:
        """Сеттер для цены с проверкой на положительное значение."""
        new_price = float(value)
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = new_price

    @classmethod
    def new_product(cls, data: Dict[str, any]) -> "Product":
        """Класс-метод для создания продукта из словаря."""
        return cls(name=data["name"], description=data["description"], price=data["price"], quantity=data["quantity"])

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


class Category:
    # Класс-атрибуты (счётчики)
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        self.name: str = name
        self.description: str = description

        # Приватный список товаров
        self.__products: List[Product] = []

        if products is not None:
            for product in products:
                self.add_product(product)

        Category.category_count += 1

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счётчик продуктов."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Геттер для приватного списка товаров.
        Возвращает строку со всеми продуктами по шаблону:
        "Название продукта, X руб. Остаток: X шт.\n"
        """
        if not self.__products:
            return ""

        lines = []
        for p in self.__products:
            price_str = int(p.price) if p.price.is_integer() else p.price
            lines.append(f"{p.name}, {price_str} руб. Остаток: {p.quantity} шт.\n")
        return "".join(lines)

    @classmethod
    def get_stats(cls) -> str:
        return f"Всего категорий: {cls.category_count}, " f"Всего товаров: {cls.product_count}"

    def __repr__(self):
        return f"Category(name='{self.name}', products_count={len(self.__products)})"

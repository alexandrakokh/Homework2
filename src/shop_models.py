from typing import List, Optional


class Product:
    def __init__(self, name: str, description: str, price, quantity: int):
        self.name: str = name
        self.description: str = description
        # ИСПРАВЛЕНИЕ: Явно приводим цену к float.
        # Теперь и 500, и 500.5 станут типом float.
        self.price: float = float(price)
        self.quantity: int = quantity

    def __repr__(self):
        return (
            f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"
        )


class Category:
    # Атрибуты КЛАССА (общие для всех объектов)
    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: Optional[List[Product]] = None
    ):
        # Инициализация атрибутов ЭКЗЕМПЛЯРА
        self.name: str = name
        self.description: str = description

        # Если список не передан, создаем пустой
        self.products: List[Product] = products if products is not None else []

        # --- ЛОГИКА АВТОМАТИЧЕСКОГО ЗАПОЛНЕНИЯ АТРИБУТОВ КЛАССА ---

        # 1. Увеличиваем счетчик категорий при создании нового объекта Category
        Category.category_count += 1

        # 2. Увеличиваем общий счетчик товаров на количество товаров в текущем списке
        Category.product_count += len(self.products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию и обновляет глобальный счетчик товаров."""
        self.products.append(product)
        # При ручном добавлении товара тоже нужно обновить общий счетчик
        Category.product_count += 1

    @classmethod
    def get_stats(cls) -> str:
        """Вспомогательный метод для вывода статистики."""
        return (
            f"Всего категорий: {cls.category_count}, "
            f"Всего товаров: {cls.product_count}"
        )


def __repr__(self):
    return f"Category(name='{self.name}', products_count={len(self.products)})"

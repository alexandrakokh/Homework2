from typing import List, Optional, Dict, Union


class Product:
    def __init__(self, name: str, description: str, price, quantity: int):
        self.name: str = name
        self.description: str = description
        self.quantity: int = quantity

        self.__price: float = 0.0
        self.price = price

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value) -> None:
        new_price = float(value)
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = new_price

    @classmethod
    def new_product(cls, data: Dict[str, any]) -> 'Product':
        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"]
        )

    def _total_cost(self) -> float:
        return self.price * self.quantity

    def __add__(self, other: Union['Product', int, float]) -> Union[float, 'Product']:
        # Разрешаем складывать с числом
        if isinstance(other, (int, float)):
            return self._total_cost() + float(other)

        # Если другой объект — тоже Product, проверяем, что это ТОЧНО такой же класс
        if isinstance(other, Product):
            if type(self) is not type(other):
                raise TypeError(
                    f"Нельзя складывать товары разных типов: "
                    f"{type(self).__name__} и {type(other).__name__}"
                )
            return self._total_cost() + other._total_cost()

        return NotImplemented

    def __radd__(self, other: Union[int, float]) -> float:
        if isinstance(other, (int, float)):
            return float(other) + self._total_cost()
        return NotImplemented

    def __str__(self) -> str:
        price_str = int(self.price) if self.price.is_integer() else self.price
        return f"{self.name}, {price_str} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price,
        quantity: int,
        efficiency: str,
        model: str,
        memory: str,
        color: str
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency: str = efficiency
        self.model: str = model
        self.memory: str = memory
        self.color: str = color

    def __str__(self) -> str:
        base = super().__str__()
        return (f"{base} | Модель: {self.model}, "
                f"Память: {self.memory}, "
                f"Производительность: {self.efficiency}, "
                f"Цвет: {self.color}")

    def __repr__(self):
        return (f"Smartphone(name='{self.name}', model='{self.model}', "
                f"memory='{self.memory}', color='{self.color}')")


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price,
        quantity: int,
        country: str,
        germination_period: str,
        color: str
    ):
        super().__init__(name, description, price, quantity)
        self.country: str = country
        self.germination_period: str = germination_period
        self.color: str = color

    def __str__(self) -> str:
        base = super().__str__()
        return (f"{base} | Страна: {self.country}, "
                f"Срок прорастания: {self.germination_period}, "
                f"Цвет травы: {self.color}")

    def __repr__(self):
        return (f"LawnGrass(name='{self.name}', country='{self.country}', "
                f"germination_period='{self.germination_period}')")


class Category:
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None):
        self.name: str = name
        self.description: str = description
        self.__products: List[Product] = []

        if products is not None:
            for product in products:
                # Используем защищённый метод add_product
                self.add_product(product)

        Category.category_count += 1

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в категорию.
        Разрешено добавлять только экземпляры Product или его наследников.
        """
        # Проверка: product должен быть экземпляром Product (или его наследника)
        if not isinstance(product, Product):
            raise TypeError(
                f"В категорию можно добавлять только объекты типа Product "
                f"(или его наследников). Получен тип: {type(product).__name__}"
            )

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        if not self.__products:
            return ""
        lines = [str(product) for product in self.__products]
        return "\n".join(lines)

    def get_total_quantity(self) -> int:
        return sum(product.quantity for product in self.__products)

    @classmethod
    def get_stats(cls) -> str:
        return (f"Всего категорий: {cls.category_count}, "
                f"Всего товаров: {cls.product_count}")

    def __str__(self) -> str:
        total_qty = self.get_total_quantity()
        return f"{self.name}, количество продуктов: {total_qty} шт."

    def __repr__(self):
        return f"Category(name='{self.name}', products_count={len(self.__products)})"

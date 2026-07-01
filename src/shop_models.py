from abc import ABC, abstractmethod
from typing import Dict, Any


class LoggingInitMixin:
    """
    Миксин, который логирует создание объекта.

    Важно: он НЕ передаёт аргументы дальше, потому что дальше идёт BaseProduct,
    а потом object.__init__, который не принимает аргументов.
    Аргументы для лога мы берём из __dict__ уже созданного объекта.
    """

    def __init__(self, *args, **kwargs):
        # Сначала инициализируем дальше по цепочке (без аргументов)
        super().__init__()

        # Теперь объект уже создан, можно брать его атрибуты для красивого лога
        cls_name = self.__class__.__name__

        # Собираем аргументы из атрибутов, которые точно есть у Product
        name = getattr(self, "_name", None)
        desc = getattr(self, "_description", None)
        price = getattr(self, "_price", None)
        qty = getattr(self, "_quantity", None)

        args_list = []
        if name is not None:
            args_list.append(repr(name))
        if desc is not None:
            args_list.append(repr(desc))
        if price is not None:
            args_list.append(f"{price!r}")
        if qty is not None:
            args_list.append(str(qty))

        all_args = ", ".join(args_list)
        print(f"{cls_name}({all_args})")


class BaseProduct(ABC, LoggingInitMixin):
    @abstractmethod
    def get_total_cost(self) -> float:
        pass

    @abstractmethod
    def get_description_preview(self) -> str:
        pass


class Product(BaseProduct):
    _counter = 0

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if price < 0:
            raise ValueError("price must be non-negative")
        if quantity < 0:
            raise ValueError("quantity must be non-negative")

        self._name = name
        self._description = description
        self._price = float(price)
        self._quantity = int(quantity)

        Product._counter += 1

        # Вызываем миксин (он уже внутри себя сделает super().__init__())
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("name cannot be empty")
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("price must be non-negative")
        self._price = float(value)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value < 0:
            raise ValueError("quantity must be non-negative")
        self._quantity = int(value)

    def get_total_cost(self) -> float:
        return self.price * self.quantity

    def get_description_preview(self) -> str:
        return (self.description[:50] + "...") if len(self.description) > 50 else self.description

    @classmethod
    def new_product(cls, data: Dict[str, Any]) -> "Product":
        required = ["name", "description", "price", "quantity"]
        for k in required:
            if k not in data:
                raise KeyError(f"Missing key in data: {k}")
        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"],
        )

    def __add__(self, other: object) -> object:
        if isinstance(other, Product):
            new_qty = self.quantity + other.quantity
            total_cost = self.get_total_cost() + other.get_total_cost()
            new_price = total_cost / new_qty if new_qty > 0 else 0.0
            return Product(
                name=f"{self.name} + {other.name}",
                description=f"{self.description} & {other.description}",
                price=new_price,
                quantity=new_qty,
            )
        return NotImplemented

    # __radd__ не нужен: если левый операнд — int, он не знает, как сложить с Product,
    # и Python вызовет наш __add__, а если он вернёт NotImplemented — будет TypeError.
    # Это нормальное поведение, и тесты должны это учитывать.

    @classmethod
    def get_counter(cls) -> int:
        return cls._counter

    def __str__(self) -> str:
        return f"Product({self._name!r}, price={self._price}, qty={self._quantity})"

    def __repr__(self) -> str:
        return self.__str__()


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, ram_gb: int):
        super().__init__(name, description, price, quantity)
        if ram_gb <= 0:
            raise ValueError("ram_gb must be positive")
        self._ram_gb = ram_gb

    @property
    def ram_gb(self) -> int:
        return self._ram_gb

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base}, RAM={self._ram_gb} GB"


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int, area_coverage_m2: float):
        super().__init__(name, description, price, quantity)
        if area_coverage_m2 <= 0:
            raise ValueError("area_coverage_m2 must be positive")
        self._area_coverage_m2 = area_coverage_m2

    @property
    def area_coverage_m2(self) -> float:
        return self._area_coverage_m2

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base}, covers {self._area_coverage_m2} m²"


class Category:


    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        # Можно хранить как есть, можно сделать копию списка, если нужна защита
        self.products = list(products)

    def get_total_cost(self) -> float:
        return sum(p.get_total_cost() for p in self.products)

    def __str__(self) -> str:
        total = self.get_total_cost()
        return f"Category({self.name!r}, {len(self.products)} товаров, общая стоимость: {total:.2f})"

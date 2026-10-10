from abc import ABC, abstractmethod
from typing import Dict, Any, List


class LoggingInitMixin:
    """
    Миксин, который логирует создание объекта.
    """

    def __init__(self, *args, **kwargs):
        # Сначала инициализируем дальше по цепочке (до object)
        super().__init__()

        # Теперь объект уже создан, можно брать его атрибуты для красивого лога
        cls_name = self.__class__.__name__

        # Собираем аргументы из атрибутов
        name = getattr(self, "_name", None)
        desc = getattr(self, "_description", None)
        price = getattr(self, "_price", None)
        qty = getattr(self, "_quantity", None)

        # ИСПРАВЛЕНИЕ: теперь список сразу создаётся пустым
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
        # ЗАДАНИЕ 1: Проверка на нулевое количество
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        # Проверка на отрицательные значения
        if quantity < 0:
            raise ValueError("quantity must be non-negative")
        if price < 0:
            raise ValueError("price must be non-negative")

        self._name = name
        self._description = description
        self._price = float(price)
        self._quantity = int(quantity)

        Product._counter += 1

        # Вызываем миксин ПОСЛЕ создания атрибутов, чтобы он мог их прочитать
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
    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.products = list(products)

    def get_total_cost(self) -> float:
        return sum(p.get_total_cost() for p in self.products)

    # ЗАДАНИЕ 2: Расчет среднего ценника с обработкой ошибки деления на ноль
    def average_price(self) -> float:
        try:
            total = sum(p.price for p in self.products)
            count = len(self.products)
            return total / count
        except ZeroDivisionError:
            return 0.0

    def __str__(self) -> str:
        total = self.get_total_cost()
        return f"Category({self.name!r}, {len(self.products)} товаров, общая стоимость: {total:.2f})"

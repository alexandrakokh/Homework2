from src.shop_models import Category, Product, Smartphone, LawnGrass

if __name__ == "__main__":
    # --- Смартфоны ---
    s1 = Smartphone(
        name="Samsung Galaxy S23 Ultra", description="Флагман", price=180000.0, quantity=5,
        efficiency="Высокая", model="SM-S918B", memory="256GB", color="Серый"
    )
    s2 = Smartphone(
        name="Iphone 15", description="Современный смартфон", price=210000.0, quantity=8,
        efficiency="Очень высокая", model="A3102", memory="512GB", color="Gray space"
    )
    s3 = Smartphone(
        name="Xiaomi Redmi Note 11", description="Доступный смартфон", price=31000.0, quantity=14,
        efficiency="Средняя", model="2201117TG", memory="1024GB", color="Синий"
    )

    # --- Газонная трава ---
    g1 = LawnGrass(
        name="Газонная смесь 'Изумруд'", description="Для солнечных участков", price=1200.0, quantity=10,
        country="Россия", germination_period="7–14 дней", color="Тёмно‑зелёный"
    )
    g2 = LawnGrass(
        name="Газон 'Быстрый старт'", description="Быстрорастущая смесь", price=900.0, quantity=20,
        country="Польша", germination_period="5–10 дней", color="Ярко‑зелёный"
    )

    # --- Аксессуары (обычные Product) ---
    p1 = Product("Чехол силиконовый", "Универсальный", 500.0, 30)
    p2 = Product("Кабель USB-C", "1 м", 800.0, 20)

    print("--- Строковое представление товаров (разные типы) ---")
    print(str(s1))
    print(str(s2))
    print(str(g1))
    print(str(p1))
    print()

    smartphones_cat = Category("Смартфоны", "Мобильные устройства", [s1, s2, s3])
    grass_cat = Category("Газонные травы", "Семена", [g1, g2])
    accessories_cat = Category("Аксессуары", "Чехлы, кабели", [p1, p2])

    print("--- Категория и список товаров ---")
    print(smartphones_cat)
    print(smartphones_cat.products)
    print()

    print("--- Сложение продуктов (полная стоимость на складе) ---")
    # ✅ Теперь складываем только одинаковые типы — это работает
    print(f"s1 + s2 = {s1 + s2}")
    print(f"g1 + g2 = {g1 + g2}")
    print(f"p1 + p2 = {p1 + p2}")

    # ❌ Эту строку убираем: она вызывает ошибку, потому что типы разные
    # print(f"\ns1 + g1 + p1 = {s1 + g1 + p1}")

    print("\n--- Сложение с числом (работает для всех типов) ---")
    print(f"s1 + 5000 = {s1 + 5000}")
    print(f"10000 + s1 = {10000 + s1}")

    print("\n--- Общая стоимость по категориям (без смешивания типов) ---")
    total_smartphones = s1 + s2 + s3
    total_grass = g1 + g2
    total_accessories = p1 + p2

    print(f"Смартфоны: {total_smartphones}")
    print(f"Газонная трава: {total_grass}")
    print(f"Аксессуары: {total_accessories}")

    print("\n--- Безопасное смешанное сложение (через try/except) ---")
    mixed_items = [s1, g1, p1]
    total_value = 0.0
    for item in mixed_items:
        try:
            # Пытаемся прибавить к числу (это всегда работает)
            total_value += item._total_cost()
        except Exception as e:
            print(f"Не удалось сложить {type(item).__name__}: {e}")

    print(f"Общая стоимость всех товаров (сумма стоимостей каждого): {total_value}")

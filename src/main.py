from src.shop_models import Category, Product, Smartphone, LawnGrass

if __name__ == "__main__":
    # --- Смартфоны ---
    s1 = Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="Флагман",
        price=180000.0,
        quantity=5,
        ram_gb=12
    )
    s2 = Smartphone(
        name="Iphone 15",
        description="Современный смартфон",
        price=210000.0,
        quantity=8,
        ram_gb=8
    )
    s3 = Smartphone(
        name="Xiaomi Redmi Note 11",
        description="Доступный смартфон",
        price=31000.0,
        quantity=14,
        ram_gb=6
    )

    # --- Газонная трава ---
    g1 = LawnGrass(
        name="Газонная смесь 'Изумруд'",
        description="Для солнечных участков",
        price=1200.0,
        quantity=10,
        area_coverage_m2=50.0
    )
    g2 = LawnGrass(
        name="Газон 'Быстрый старт'",
        description="Быстрорастущая смесь",
        price=900.0,
        quantity=20,
        area_coverage_m2=75.0
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

    print("--- Сложение продуктов (одного типа) ---")
    # Работает: Product + Product
    print(f"s1 + s2 = {s1 + s2}")
    print(f"g1 + g2 = {g1 + g2}")
    print(f"p1 + p2 = {p1 + p2}")

    print("\n--- Общая стоимость по категориям (через сумму стоимостей) ---")
    total_smartphones = s1.get_total_cost() + s2.get_total_cost() + s3.get_total_cost()
    total_grass = g1.get_total_cost() + g2.get_total_cost()
    total_accessories = p1.get_total_cost() + p2.get_total_cost()

    print(f"Смартфоны: {total_smartphones:.2f} руб.")
    print(f"Газонная трава: {total_grass:.2f} руб.")
    print(f"Аксессуары: {total_accessories:.2f} руб.")

    print("\n--- Безопасное смешанное суммирование (все товары) ---")
    mixed_items = [s1, g1, p1]
    total_value = 0.0
    for item in mixed_items:
        total_value += item.get_total_cost()

    print(f"Общая стоимость всех товаров: {total_value:.2f} руб.")


from src.shop_models import Category, Product

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("--- Строковое представление товаров ---")
    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print("\n--- Категория и список товаров ---")
    print(str(category1))
    print(category1.products)

    print("\n--- Сложение продуктов (полная стоимость на складе) ---")
    print(f"product1 + product2 = {product1 + product2}")
    print(f"product1 + product3 = {product1 + product3}")
    print(f"product2 + product3 = {product2 + product3}")

    print("\n--- Сложение с числом ---")
    print(f"product1 + 5000 = {product1 + 5000}")
    print(f"10000 + product1 = {10000 + product1}")

    print("\n--- Общая стоимость всех товаров в категории (вручную) ---")
    total_value = product1 + product2 + product3
    print(f"Общая стоимость (product1 + product2 + product3) = {total_value}")
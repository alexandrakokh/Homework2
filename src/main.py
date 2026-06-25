from src.shop_models import Category, Product

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    # Теперь используем products (геттер), который возвращает строку по шаблону
    print(category1.products)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)

    print("\n--- После добавления телевизора ---\n")
    print(category1.products)

    # Обращаемся к счётчику через класс, как и положено для класс-атрибута
    print(f"\nВсего товаров в системе: {Category.product_count}")

    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    print(f"\nНовый товар: {new_product.name}")
    print(f"Цена: {new_product.price}")
    print(f"Количество: {new_product.quantity}")

    # Проверка валидации цены
    new_product.price = 800
    print(f"Новая цена: {new_product.price}")

    new_product.price = -100
    print(f"Попытка установить -100: цена осталась {new_product.price}")

    new_product.price = 0
    print(f"Попытка установить 0: цена осталась {new_product.price}")

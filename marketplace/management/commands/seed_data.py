import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Company
from marketplace.models import ProductCategory, Product, Inventory

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with test categories, products, companies, and inventories."

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Clearing old data...")

        Inventory.objects.all().delete()
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        Company.objects.all().delete()
        User.objects.filter(user_type="seller").delete()

        # -------------------------
        # 1. Create Sellers + Companies
        # -------------------------
        sellers = []
        companies = []

        for i in range(1, 4):
            user = User.objects.create_user(
                username=f"seller{i}",
                email=f"seller{i}@test.com",
                password="test1234",
                user_type="seller",
                is_verified=True,
                kyc_verified=True,
            )
            sellers.append(user)

            company = Company.objects.create(
                owner=user,
                name=f"Test Company {i}",
                description="A demo seller company",
                industry_type=random.choice(["Electronics", "Clothing", "Furniture", "Groceries"]),
                is_verified=True,
            )
            companies.append(company)

        self.stdout.write("✅ Created sellers and companies")

        # -------------------------
        # 2. Create Categories
        # -------------------------
        categories_data = [
            "Electronics",
            "Clothing",
            "Furniture",
            "Groceries",
            "Books",
            "Beauty & Personal Care",
        ]

        categories = []
        for name in categories_data:
            cat = ProductCategory.objects.create(name=name)
            categories.append(cat)

        self.stdout.write("✅ Created categories")

        # -------------------------
        # 3. Create Products
        # -------------------------
        product_names = [
            "Smartphone", "Laptop", "Headphones", "Smartwatch", "Bluetooth Speaker",
            "Men's T-Shirt", "Women's Jeans", "Sneakers", "Jacket", "Sunglasses",
            "Sofa Set", "Dining Table", "Office Chair", "Bed Frame", "Bookshelf",
            "Rice 5kg", "Cooking Oil 1L", "Pasta Pack", "Coffee Powder", "Green Tea",
            "Novel - Fiction", "Science Textbook", "Children's Storybook", "Comics", "Notebook Pack",
            "Shampoo", "Face Cream", "Perfume", "Lipstick", "Hand Sanitizer",
        ]

        # Duplicate products until we reach 50+
        while len(product_names) < 50:
            product_names += [f"Product {len(product_names)+1}"]

        products = []
        for name in product_names[:50]:
            category = random.choice(categories)
            product = Product.objects.create(
                name=name,
                description=f"This is a {name} description.",
                category=category,
                images=[f"https://picsum.photos/seed/{random.randint(1, 1000)}/400/400"],
            )
            products.append(product)

        self.stdout.write("✅ Created 50 products")

        # -------------------------
        # 4. Create Inventory (per product linked to a random company)
        # -------------------------
        for product in products:
            company = random.choice(companies)
            price = random.randint(100, 5000)

            Inventory.objects.create(
                product=product,
                company=company,
                stock_quantity=random.randint(10, 200),
                selling_price=price,
                min_selling_price=price * 0.9,
                max_selling_price=price * 1.2,
                is_available=True,
            )

        self.stdout.write(self.style.SUCCESS("🎉 Test data seeded successfully!"))

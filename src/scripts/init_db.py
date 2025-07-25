#!/usr/bin/env python3
"""
Database initialization script for Clean Architecture.
This script creates the database tables and initializes with sample data.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from src.config.database import db_config
from src.adapters.di.container import container
from src.entities.customer import Customer
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.value_objects.money import Money


def init_database():
    """Initialize the database with tables and basic data"""
    print(f"Connecting to database: {db_config}")

    try:
        repository = container.customer_repository

        # Get or create anonymous customer
        anonymous_customer = repository.get_anonymous_customer()
        print(f"Anonymous customer created/found: {anonymous_customer}")

        print("Database initialization completed successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)


def create_sample_customers():
    """Create sample customer data"""
    print("Creating sample data...")

    try:
        repository = container.customer_repository

        # Create sample customers
        sample_customers = [
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "document": "98765432100",
            }
        ]

        for customer_data in sample_customers:
            customer = Customer.create_registered(
                first_name=customer_data["first_name"],
                last_name=customer_data["last_name"],
                email=customer_data["email"],
                document=customer_data["document"],
            )
            saved_customer = repository.save(customer)
            print(f"Created customer: {saved_customer.full_name}")

        print("Sample data creation completed!")

    except Exception as e:
        print(f"Error creating sample data: {e}")
        sys.exit(1)


def create_sample_ingredients():
    """Create sample ingredient data"""
    print("Creating sample ingredients...")

    try:
        repository = container.ingredient_repository

        # Create sample ingredients
        sample_ingredients = [
            # Bread ingredients (for burgers)
            {
                "name": "Classic Bun",
                "price": Money.create(2.50),
                "is_active": True,
                "type": IngredientType.BREAD,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            {
                "name": "Whole Wheat Bun",
                "price": Money.create(3.00),
                "is_active": True,
                "type": IngredientType.BREAD,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            # Meat ingredients (for burgers)
            {
                "name": "Beef Patty",
                "price": Money.create(8.00),
                "is_active": True,
                "type": IngredientType.MEAT,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            {
                "name": "Chicken Breast",
                "price": Money.create(7.50),
                "is_active": True,
                "type": IngredientType.MEAT,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            {
                "name": "Veggie Patty",
                "price": Money.create(6.50),
                "is_active": True,
                "type": IngredientType.MEAT,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            # Cheese ingredients (for burgers)
            {
                "name": "Cheddar Cheese",
                "price": Money.create(1.50),
                "is_active": True,
                "type": IngredientType.CHEESE,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            {
                "name": "Swiss Cheese",
                "price": Money.create(1.75),
                "is_active": True,
                "type": IngredientType.CHEESE,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            # Vegetable ingredients (for burgers)
            {
                "name": "Lettuce",
                "price": Money.create(0.50),
                "is_active": True,
                "type": IngredientType.VEGETABLE,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            {
                "name": "Tomato",
                "price": Money.create(0.75),
                "is_active": True,
                "type": IngredientType.VEGETABLE,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            {
                "name": "Onion",
                "price": Money.create(0.50),
                "is_active": True,
                "type": IngredientType.VEGETABLE,
                "applies_to_burger": True,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            # Salad ingredients (for burgers and sides)
            {
                "name": "Mixed Greens",
                "price": Money.create(1.00),
                "is_active": True,
                "type": IngredientType.SALAD,
                "applies_to_burger": True,
                "applies_to_side": True,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            # Sauce ingredients (for burgers and sides)
            {
                "name": "Ketchup",
                "price": Money.create(0.25),
                "is_active": True,
                "type": IngredientType.SAUCE,
                "applies_to_burger": True,
                "applies_to_side": True,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            {
                "name": "Mustard",
                "price": Money.create(0.25),
                "is_active": True,
                "type": IngredientType.SAUCE,
                "applies_to_burger": True,
                "applies_to_side": True,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            {
                "name": "Mayonnaise",
                "price": Money.create(0.30),
                "is_active": True,
                "type": IngredientType.SAUCE,
                "applies_to_burger": True,
                "applies_to_side": True,
                "applies_to_drink": False,
                "applies_to_dessert": False,
            },
            # Ice ingredients (for drinks)
            {
                "name": "Ice Cubes",
                "price": Money.create(0.10),
                "is_active": True,
                "type": IngredientType.ICE,
                "applies_to_burger": False,
                "applies_to_side": False,
                "applies_to_drink": True,
                "applies_to_dessert": False,
            },
            # Milk ingredients (for drinks)
            {
                "name": "Whole Milk",
                "price": Money.create(1.00),
                "is_active": True,
                "type": IngredientType.MILK,
                "applies_to_burger": False,
                "applies_to_side": False,
                "applies_to_drink": True,
                "applies_to_dessert": False,
            },
            {
                "name": "Almond Milk",
                "price": Money.create(1.50),
                "is_active": True,
                "type": IngredientType.MILK,
                "applies_to_burger": False,
                "applies_to_side": False,
                "applies_to_drink": True,
                "applies_to_dessert": False,
            },
            # Topping ingredients (for desserts)
            {
                "name": "Chocolate Sprinkles",
                "price": Money.create(0.75),
                "is_active": True,
                "type": IngredientType.TOPPING,
                "applies_to_burger": False,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": True,
            },
            {
                "name": "Whipped Cream",
                "price": Money.create(0.50),
                "is_active": True,
                "type": IngredientType.TOPPING,
                "applies_to_burger": False,
                "applies_to_side": False,
                "applies_to_drink": False,
                "applies_to_dessert": True,
            },
        ]

        for ingredient_data in sample_ingredients:
            ingredient = Ingredient.create(
                name=ingredient_data["name"],
                price=ingredient_data["price"],
                is_active=ingredient_data["is_active"],
                type=ingredient_data["type"],
                applies_to_burger=ingredient_data["applies_to_burger"],
                applies_to_side=ingredient_data["applies_to_side"],
                applies_to_drink=ingredient_data["applies_to_drink"],
                applies_to_dessert=ingredient_data["applies_to_dessert"],
            )
            saved_ingredient = repository.save(ingredient)
            print(f"Created ingredient: {saved_ingredient.name} ({saved_ingredient.type}) - ${saved_ingredient.price}")

        print("Sample ingredients creation completed!")

    except Exception as e:
        print(f"Error creating sample ingredients: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Initialize database
    init_database()

    # Create sample data if requested
    if "--sample-data" in sys.argv:
        create_sample_customers()
        create_sample_ingredients()

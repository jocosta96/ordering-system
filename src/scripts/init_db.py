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


def create_sample_data():
    """Create sample customer data"""
    print("Creating sample data...")

    try:
        repository = container.customer_repository

        # Create sample customers
        sample_customers = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "document": "12345678901",
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "document": "98765432100",
            },
            {
                "first_name": "Bob",
                "last_name": "Johnson",
                "email": "bob.johnson@example.com",
                "document": "11122233344",
            },
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


if __name__ == "__main__":
    # Initialize database
    init_database()

    # Create sample data if requested
    if "--sample-data" in sys.argv:
        create_sample_data()

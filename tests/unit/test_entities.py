"""
Unit tests for Customer entity.

Tests cover:
- Customer creation and validation
- Business rules
- Factory methods
- Properties and methods
"""

import pytest
from src.entities.customer import Customer
from src.entities.value_objects.name import Name
from src.entities.value_objects.email import Email
from src.entities.value_objects.document import Document


class TestCustomerEntity:
    """Test cases for Customer entity"""

    def test_create_registered_customer(self):
        """Test creating a registered customer"""
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
            customer_id=1,
        )

        assert customer.id == 1
        assert customer.first_name.value == "John"
        assert customer.last_name.value == "Doe"
        assert customer.email.value == "john.doe@example.com"
        assert customer.document.value == "52998224725"  # Valid Brazilian CPF
        assert customer.is_anonymous is False
        assert customer.is_registered is True
        assert customer.full_name == "John Doe"

    def test_create_anonymous_customer(self):
        """Test creating an anonymous customer"""
        customer = Customer.create_anonymous()

        assert customer.id is None
        assert customer.first_name.value == "Anonymous"
        assert customer.last_name.value == "Customer"
        assert (
            customer.email.value == "anonymous@fastfood.local"
        )  # From test environment
        assert customer.document.value == ""
        assert customer.is_anonymous is True
        assert customer.is_registered is False
        assert customer.full_name == "Anonymous Customer"

    def test_customer_business_rules_anonymous_with_wrong_email(self):
        """Test that anonymous customer with wrong email raises error"""
        with pytest.raises(
            ValueError, match="Anonymous customers must have anonymous email"
        ):
            Customer(
                first_name=Name.create("Anonymous"),
                last_name=Name.create("Customer"),
                email=Email.create("wrong@email.com"),
                document=Document.create(""),
            )

    def test_customer_business_rules_registered_without_email(self):
        """Test that registered customer without email raises error"""
        with pytest.raises(ValueError, match="Registered customers must have an email"):
            Customer(
                first_name=Name.create("John"),
                last_name=Name.create("Doe"),
                email=Email.create(""),
                document=Document.create("52998224725"),  # Valid Brazilian CPF
            )

    def test_customer_can_place_order_anonymous(self):
        """Test that anonymous customer can place order"""
        customer = Customer.create_anonymous()
        assert customer.can_place_order() is True

    def test_customer_can_place_order_registered(self):
        """Test that registered customer can place order"""
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
        )
        assert customer.can_place_order() is True

    def test_customer_cannot_place_order_registered_without_email(self):
        """Test that registered customer without email cannot place order"""
        # This test should create a customer that violates business rules
        # The customer creation itself should fail, not the can_place_order method
        with pytest.raises(ValueError, match="Registered customers must have an email"):
            Customer.create_registered(
                first_name="John",
                last_name="Doe",
                email="",
                document="52998224725",  # Valid Brazilian CPF
            )

    def test_customer_get_display_name_anonymous(self):
        """Test get_display_name for anonymous customer"""
        customer = Customer.create_anonymous()
        assert customer.get_display_name() == "Anonymous Customer"

    def test_customer_get_display_name_registered(self):
        """Test get_display_name for registered customer"""
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
        )
        assert customer.get_display_name() == "John Doe"

    def test_customer_string_representation(self):
        """Test customer string representation"""
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
            customer_id=1,
        )

        expected_str = "Customer(id=1, name='John Doe', email='john.doe@example.com')"
        assert str(customer) == expected_str

    def test_customer_repr_representation(self):
        """Test customer repr representation"""
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
            customer_id=1,
        )

        # Check that repr contains all the important information
        repr_str = repr(customer)
        assert "Customer(" in repr_str
        assert "id=1" in repr_str
        assert "first_name=" in repr_str
        assert "last_name=" in repr_str
        assert "email=" in repr_str
        assert "document=" in repr_str

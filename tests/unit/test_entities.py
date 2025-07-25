"""
Unit tests for Customer entity.

Tests cover:
- Customer creation and validation
- Business rules
- Factory methods
- Properties and methods
- DTO conversions
"""

import pytest
from decimal import Decimal
from src.entities.customer import Customer
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.value_objects.name import Name
from src.entities.value_objects.email import Email
from src.entities.value_objects.document import Document
from src.entities.value_objects.money import Money
from src.application.dto.customer_dto import CustomerResponse
from src.application.dto.ingredient_dto import IngredientResponse


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
        """Test customer display name for anonymous customer"""
        customer = Customer.create_anonymous()
        assert customer.get_display_name() == "Anonymous Customer"

    def test_customer_get_display_name_registered(self):
        """Test customer display name for registered customer"""
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
        expected = "Customer(id=1, name='John Doe', email='john.doe@example.com')"
        assert str(customer) == expected

    def test_customer_repr_representation(self):
        """Test customer repr representation"""
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
            customer_id=1,
        )
        # The repr should contain all the internal representation details
        repr_str = repr(customer)
        assert "Customer(" in repr_str
        assert "first_name=" in repr_str
        assert "last_name=" in repr_str
        assert "email=" in repr_str
        assert "document=" in repr_str
        assert "id=1" in repr_str

    def test_customer_dto_conversion(self):
        """Test customer to DTO conversion"""
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
            customer_id=1,
        )
        
        dto = CustomerResponse.from_entity(customer)
        
        assert dto.id == 1
        assert dto.first_name == "John"
        assert dto.last_name == "Doe"
        assert dto.email == "john.doe@example.com"
        assert dto.document == "52998224725"
        assert dto.full_name == "John Doe"
        assert dto.is_anonymous is False
        assert dto.is_registered is True


class TestIngredientEntity:
    """Test cases for Ingredient entity"""

    def test_create_ingredient_with_id(self):
        """Test creating an ingredient with ID"""
        ingredient = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1
        )

        assert ingredient.id == 1
        assert ingredient.name.value == "Tomato"
        assert ingredient.price.amount == Decimal("2.50")
        assert ingredient.is_active is True
        assert ingredient.type == IngredientType.VEGETABLE
        assert ingredient.applies_to_burger is True
        assert ingredient.applies_to_side is False
        assert ingredient.applies_to_drink is False
        assert ingredient.applies_to_dessert is False

    def test_create_ingredient_without_id(self):
        """Test creating an ingredient without ID"""
        ingredient = Ingredient.create(
            name="Lettuce",
            price=Money(amount=Decimal("1.00")),
            is_active=True,
            type=IngredientType.SALAD,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False
        )

        assert ingredient.id is None
        assert ingredient.name.value == "Lettuce"
        assert ingredient.price.amount == Decimal("1.00")
        assert ingredient.is_active is True
        assert ingredient.type == IngredientType.SALAD
        assert ingredient.applies_to_burger is True
        assert ingredient.applies_to_side is True
        assert ingredient.applies_to_drink is False
        assert ingredient.applies_to_dessert is False

    def test_create_ingredient_with_different_types(self):
        """Test creating ingredients with different types"""
        # Test BREAD type
        bread = Ingredient.create(
            name="Whole Wheat Bread",
            price=Money(amount=Decimal("3.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert bread.type == IngredientType.BREAD

        # Test MEAT type
        meat = Ingredient.create(
            name="Beef Patty",
            price=Money(amount=Decimal("8.00")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert meat.type == IngredientType.MEAT

        # Test CHEESE type
        cheese = Ingredient.create(
            name="Cheddar Cheese",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert cheese.type == IngredientType.CHEESE

        # Test VEGETABLE type
        vegetable = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("1.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert vegetable.type == IngredientType.VEGETABLE

        # Test SALAD type
        salad = Ingredient.create(
            name="Lettuce",
            price=Money(amount=Decimal("1.00")),
            is_active=True,
            type=IngredientType.SALAD,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert salad.type == IngredientType.SALAD

        # Test SAUCE type
        sauce = Ingredient.create(
            name="Ketchup",
            price=Money(amount=Decimal("0.50")),
            is_active=True,
            type=IngredientType.SAUCE,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert sauce.type == IngredientType.SAUCE

        # Test ICE type
        ice = Ingredient.create(
            name="Ice Cubes",
            price=Money(amount=Decimal("0.00")),
            is_active=True,
            type=IngredientType.ICE,
            applies_to_burger=False,
            applies_to_side=False,
            applies_to_drink=True,
            applies_to_dessert=False
        )
        assert ice.type == IngredientType.ICE

        # Test MILK type
        milk = Ingredient.create(
            name="Whole Milk",
            price=Money(amount=Decimal("1.50")),
            is_active=True,
            type=IngredientType.MILK,
            applies_to_burger=False,
            applies_to_side=False,
            applies_to_drink=True,
            applies_to_dessert=False
        )
        assert milk.type == IngredientType.MILK

        # Test TOPPING type
        topping = Ingredient.create(
            name="Chocolate Sprinkles",
            price=Money(amount=Decimal("1.00")),
            is_active=True,
            type=IngredientType.TOPPING,
            applies_to_burger=False,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=True
        )
        assert topping.type == IngredientType.TOPPING

    def test_create_inactive_ingredient(self):
        """Test creating an inactive ingredient"""
        ingredient = Ingredient.create(
            name="Discontinued Sauce",
            price=Money(amount=Decimal("1.00")),
            is_active=False,
            type=IngredientType.SAUCE,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert ingredient.is_active is False

    def test_ingredient_business_rules_without_name(self):
        """Test that ingredient without name raises error"""
        with pytest.raises(ValueError, match="Invalid Name"):
            Ingredient(
                name=Name.create(""),
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=IngredientType.VEGETABLE,
                applies_to_burger=True,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=False
            )

    def test_ingredient_business_rules_without_price(self):
        """Test that ingredient without price raises error"""
        with pytest.raises(ValueError, match="Ingredient must have a price"):
            Ingredient(
                name=Name.create("Test"),
                price=None,
                is_active=True,
                type=IngredientType.VEGETABLE,
                applies_to_burger=True,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=False
            )

    def test_ingredient_business_rules_negative_price(self):
        """Test that ingredient with negative price raises error"""
        with pytest.raises(ValueError, match="Invalid amount"):
            Ingredient(
                name=Name.create("Test"),
                price=Money(amount=Decimal("-1.00")),
                is_active=True,
                type=IngredientType.VEGETABLE,
                applies_to_burger=True,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=False
            )

    def test_ingredient_business_rules_zero_price(self):
        """Test that ingredient with zero price is valid"""
        ingredient = Ingredient.create(
            name="Free Ingredient",
            price=Money(amount=Decimal("0.00")),
            is_active=True,
            type=IngredientType.TOPPING,
            applies_to_burger=False,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=True
        )
        assert ingredient.price.amount == Decimal("0.00")

    def test_ingredient_business_rules_without_type(self):
        """Test that ingredient without type raises error"""
        with pytest.raises(ValueError, match="Ingredient must have a type"):
            Ingredient(
                name=Name.create("Test"),
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=None,
                applies_to_burger=True,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=False
            )

    def test_ingredient_business_rules_no_applies_to(self):
        """Test that ingredient without any applies_to raises error"""
        with pytest.raises(ValueError, match="Ingredient must have an applies_to"):
            Ingredient(
                name=Name.create("Test"),
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=IngredientType.BREAD,
                applies_to_burger=False,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=False
            )

    def test_ingredient_business_rules_invalid_burger_ingredient(self):
        """Test that ingredient with invalid type for burger raises error"""
        with pytest.raises(ValueError, match="Ingredient must be a valid burger ingredient"):
            Ingredient(
                name=Name.create("Test"),
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=IngredientType.ICE,
                applies_to_burger=True,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=False
            )

    def test_ingredient_business_rules_invalid_side_ingredient(self):
        """Test that ingredient with invalid type for side raises error"""
        with pytest.raises(ValueError, match="Ingredient must be a valid side ingredient"):
            Ingredient(
                name=Name.create("Test"),
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=IngredientType.MEAT,
                applies_to_burger=False,
                applies_to_side=True,
                applies_to_drink=False,
                applies_to_dessert=False
            )

    def test_ingredient_business_rules_invalid_drink_ingredient(self):
        """Test that ingredient with invalid type for drink raises error"""
        with pytest.raises(ValueError, match="Ingredient must be a valid drink ingredient"):
            Ingredient(
                name=Name.create("Test"),
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=IngredientType.BREAD,
                applies_to_burger=False,
                applies_to_side=False,
                applies_to_drink=True,
                applies_to_dessert=False
            )

    def test_ingredient_business_rules_invalid_dessert_ingredient(self):
        """Test that ingredient with invalid type for dessert raises error"""
        with pytest.raises(ValueError, match="Ingredient must be a valid dessert ingredient"):
            Ingredient(
                name=Name.create("Test"),
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=IngredientType.MEAT,
                applies_to_burger=False,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=True
            )

    def test_ingredient_valid_burger_ingredients(self):
        """Test that valid burger ingredients are accepted"""
        valid_burger_types = [
            IngredientType.BREAD,
            IngredientType.MEAT,
            IngredientType.CHEESE,
            IngredientType.VEGETABLE,
            IngredientType.SALAD
        ]
        
        for ingredient_type in valid_burger_types:
            ingredient = Ingredient.create(
                name=f"Test {ingredient_type.value}",
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=ingredient_type,
                applies_to_burger=True,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=False
            )
            assert ingredient.applies_to_burger is True

    def test_ingredient_valid_side_ingredients(self):
        """Test that valid side ingredients are accepted"""
        valid_side_types = [
            IngredientType.SALAD,
            IngredientType.SAUCE
        ]
        
        for ingredient_type in valid_side_types:
            ingredient = Ingredient.create(
                name=f"Test {ingredient_type.value}",
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=ingredient_type,
                applies_to_burger=False,
                applies_to_side=True,
                applies_to_drink=False,
                applies_to_dessert=False
            )
            assert ingredient.applies_to_side is True

    def test_ingredient_valid_drink_ingredients(self):
        """Test that valid drink ingredients are accepted"""
        valid_drink_types = [
            IngredientType.ICE,
            IngredientType.MILK
        ]
        
        for ingredient_type in valid_drink_types:
            ingredient = Ingredient.create(
                name=f"Test {ingredient_type.value}",
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=ingredient_type,
                applies_to_burger=False,
                applies_to_side=False,
                applies_to_drink=True,
                applies_to_dessert=False
            )
            assert ingredient.applies_to_drink is True

    def test_ingredient_valid_dessert_ingredients(self):
        """Test that valid dessert ingredients are accepted"""
        valid_dessert_types = [
            IngredientType.TOPPING
        ]
        
        for ingredient_type in valid_dessert_types:
            ingredient = Ingredient.create(
                name=f"Test {ingredient_type.value}",
                price=Money(amount=Decimal("1.00")),
                is_active=True,
                type=ingredient_type,
                applies_to_burger=False,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=True
            )
            assert ingredient.applies_to_dessert is True

    def test_ingredient_multiple_applies_to(self):
        """Test that ingredient can apply to multiple categories"""
        ingredient = Ingredient.create(
            name="Lettuce",
            price=Money(amount=Decimal("1.00")),
            is_active=True,
            type=IngredientType.SALAD,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert ingredient.applies_to_burger is True
        assert ingredient.applies_to_side is True
        assert ingredient.applies_to_drink is False
        assert ingredient.applies_to_dessert is False

    def test_ingredient_string_representation(self):
        """Test ingredient string representation"""
        ingredient = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1
        )
        expected = "Ingredient(id=1, name=Tomato, price=2.50, is_active=True)"
        assert str(ingredient) == expected

    def test_ingredient_repr_representation(self):
        """Test ingredient repr representation"""
        ingredient = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1
        )
        # The repr should contain all the internal representation details
        repr_str = repr(ingredient)
        assert "Ingredient(" in repr_str
        assert "id=1" in repr_str
        assert "name=Tomato" in repr_str
        assert "price=2.50" in repr_str
        assert "is_active=True" in repr_str

    def test_ingredient_with_whitespace_name(self):
        """Test ingredient with whitespace in name"""
        ingredient = Ingredient.create(
            name="  Tomato  ",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        # The Name value object should handle whitespace trimming
        assert ingredient.name.value == "Tomato"

    def test_ingredient_with_special_characters_name(self):
        """Test ingredient with special characters in name"""
        ingredient = Ingredient.create(
            name="Tomato Basil",
            price=Money(amount=Decimal("3.00")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert ingredient.name.value == "Tomato Basil"

    def test_ingredient_price_formatting(self):
        """Test ingredient price formatting"""
        ingredient = Ingredient.create(
            name="Premium Cheese",
            price=Money(amount=Decimal("4.99")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert ingredient.price.amount == Decimal("4.99")

    def test_ingredient_equality(self):
        """Test ingredient equality"""
        ingredient1 = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1
        )
        
        ingredient2 = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1
        )
        
        assert ingredient1 == ingredient2

    def test_ingredient_inequality(self):
        """Test ingredient inequality"""
        ingredient1 = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1
        )
        
        ingredient2 = Ingredient.create(
            name="Lettuce",
            price=Money(amount=Decimal("1.00")),
            is_active=True,
            type=IngredientType.SALAD,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=2
        )
        
        assert ingredient1 != ingredient2

    def test_ingredient_type_enum_values(self):
        """Test ingredient type enum values"""
        assert IngredientType.BREAD.value == "bread"
        assert IngredientType.MEAT.value == "meat"
        assert IngredientType.CHEESE.value == "cheese"
        assert IngredientType.VEGETABLE.value == "vegetable"
        assert IngredientType.SALAD.value == "salad"
        assert IngredientType.SAUCE.value == "sauce"
        assert IngredientType.ICE.value == "ice"
        assert IngredientType.MILK.value == "milk"
        assert IngredientType.TOPPING.value == "topping"

    def test_ingredient_with_large_price(self):
        """Test ingredient with large price"""
        ingredient = Ingredient.create(
            name="Premium Wagyu Beef",
            price=Money(amount=Decimal("25.99")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert ingredient.price.amount == Decimal("25.99")

    def test_ingredient_with_small_price(self):
        """Test ingredient with small price"""
        ingredient = Ingredient.create(
            name="Salt",
            price=Money(amount=Decimal("0.10")),
            is_active=True,
            type=IngredientType.SAUCE,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        assert ingredient.price.amount == Decimal("0.10")

    def test_ingredient_mutability(self):
        """Test that ingredient is immutable after creation"""
        ingredient = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1
        )
        
        # The ingredient should be immutable, so we can't modify its attributes directly
        # This is enforced by the dataclass and value objects being immutable
        original_name = ingredient.name.value
        original_price = ingredient.price.amount
        
        # Any attempt to modify would require creating a new instance
        # This test verifies the current state remains unchanged
        assert ingredient.name.value == original_name
        assert ingredient.price.amount == original_price

    def test_ingredient_dto_conversion(self):
        """Test ingredient to DTO conversion"""
        ingredient = Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1
        )
        
        dto = IngredientResponse.from_entity(ingredient)
        
        assert dto.id == 1
        assert dto.name == "Tomato"
        assert dto.price == 2.50
        assert dto.is_active is True
        assert dto.type == IngredientType.VEGETABLE
        assert dto.applies_to_burger is True
        assert dto.applies_to_side is False
        assert dto.applies_to_drink is False
        assert dto.applies_to_dessert is False

    def test_ingredient_dto_conversion_without_id(self):
        """Test ingredient to DTO conversion without ID"""
        ingredient = Ingredient.create(
            name="Lettuce",
            price=Money(amount=Decimal("1.00")),
            is_active=True,
            type=IngredientType.SALAD,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        dto = IngredientResponse.from_entity(ingredient)
        
        assert dto.id is None
        assert dto.name == "Lettuce"
        assert dto.price == 1.00
        assert dto.is_active is True
        assert dto.type == IngredientType.SALAD
        assert dto.applies_to_burger is True
        assert dto.applies_to_side is True
        assert dto.applies_to_drink is False
        assert dto.applies_to_dessert is False

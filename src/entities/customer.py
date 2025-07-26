from dataclasses import dataclass
from typing import Optional
import uuid
from .value_objects.document import Document
from .value_objects.email import Email
from .value_objects.name import Name


@dataclass
class Customer:
    """
    Customer entity that represents a customer in the ordering system.

    This is an entity because:
    - It has an identity (id)
    - It can change over time while maintaining its identity
    - It contains business logic and rules
    - It's the aggregate root for customer-related operations
    """

    first_name: Name
    last_name: Name
    email: Email
    document: Document
    id: Optional[uuid.UUID] = None
    internal_id: Optional[int] = None

    def __post_init__(self):
        """Validate business rules during object creation"""
        self._validate_business_rules()

    def _validate_business_rules(self):
        """Validate domain business rules"""
        from src.config.app_config import app_config

        # Rule: Anonymous customers (empty document) must have anonymous email
        if (
            self.document.is_empty
            and not self.email.value == app_config.anonymous_email
        ):
            raise ValueError("Anonymous customers must have anonymous email")

        # Rule: Registered customers must have both document and email
        if not self.document.is_empty and self.email.value == "":
            raise ValueError("Registered customers must have an email")

    @property
    def full_name(self) -> str:
        """Get the customer's full name"""
        return f"{self.first_name.value} {self.last_name.value}".strip()

    @property
    def is_anonymous(self) -> bool:
        """Check if this is an anonymous customer"""
        return self.document.is_empty

    @property
    def is_registered(self) -> bool:
        """Check if this is a registered customer"""
        return not self.is_anonymous

    def can_place_order(self) -> bool:
        """Business rule: Check if customer can place an order"""
        # Anonymous customers can always place orders
        if self.is_anonymous:
            return True

        # Registered customers must have valid email and document
        return not self.email.value == "" and not self.document.is_empty

    def get_display_name(self) -> str:
        """Get display name for UI purposes"""
        if self.is_anonymous:
            return "Anonymous Customer"
        return self.full_name

    def __str__(self) -> str:
        return f"Customer(id={self.id}, name='{self.full_name}', email='{self.email}')"

    def __repr__(self) -> str:
        return f"Customer(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, document={self.document})"

    @classmethod
    def create_anonymous(cls, customer_id: Optional[uuid.UUID] = None, internal_id: Optional[int] = None) -> "Customer":
        """Factory method to create an anonymous customer"""
        from src.config.app_config import app_config

        return cls(
            first_name=Name.create("Anonymous"),
            last_name=Name.create("Customer"),
            email=Email.create(app_config.anonymous_email),
            document=Document.create(""),
            id=customer_id if customer_id else uuid.uuid4(),
            internal_id=internal_id,
        )

    @classmethod
    def create_registered(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        document: str,
        customer_id: Optional[uuid.UUID] = None,
        internal_id: Optional[int] = None,
    ) -> "Customer":
        """Factory method to create a registered customer"""
        return cls(
            first_name=Name.create(first_name),
            last_name=Name.create(last_name),
            email=Email.create(email),
            document=Document.create(document),
            id=customer_id if customer_id else uuid.uuid4(),
            internal_id=internal_id,
        )

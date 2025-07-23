from dataclasses import dataclass
from typing import Optional


@dataclass
class CustomerCreateRequest:
    """DTO for customer creation request"""

    first_name: str
    last_name: str
    email: str
    document: str


@dataclass
class CustomerUpdateRequest:
    """DTO for customer update request"""

    id: int
    first_name: str
    last_name: str
    email: str
    document: str


@dataclass
class CustomerResponse:
    """DTO for customer response"""

    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    document: str
    full_name: str
    is_anonymous: bool
    is_registered: bool

    @classmethod
    def from_entity(cls, customer):
        """Create DTO from Customer entity"""
        return cls(
            id=customer.id,
            first_name=customer.first_name.value,
            last_name=customer.last_name.value,
            email=customer.email.value,
            document=customer.document.value,
            full_name=customer.full_name,
            is_anonymous=customer.is_anonymous,
            is_registered=customer.is_registered,
        )


@dataclass
class CustomerListResponse:
    """DTO for customer list response"""

    customers: list[CustomerResponse]
    total_count: int

from dataclasses import dataclass
from typing import Optional
from src.entities.ingredient import IngredientType

@dataclass
class IngredientCreateRequest:
    """DTO for ingredient creation request"""

    name: str
    price: float
    is_active: bool
    type: IngredientType
    applies_to_burger: bool
    applies_to_side: bool
    applies_to_drink: bool
    applies_to_dessert: bool

@dataclass
class IngredientUpdateRequest:
    """DTO for ingredient update request"""

    id: int
    name: str
    price: float
    is_active: bool
    type: IngredientType
    applies_to_burger: bool
    applies_to_side: bool
    applies_to_drink: bool
    applies_to_dessert: bool

@dataclass
class IngredientResponse:
    """DTO for ingredient response"""

    id: Optional[int]
    name: str
    price: float
    is_active: bool
    type: IngredientType
    applies_to_burger: bool
    applies_to_side: bool
    applies_to_drink: bool
    applies_to_dessert: bool

    @classmethod
    def from_entity(cls, ingredient):
        """Create DTO from Ingredient entity"""
        return cls(
            id=ingredient.id,
            name=ingredient.name.value,
            price=ingredient.price.value,
            is_active=ingredient.is_active,
            type=ingredient.type,
            applies_to_burger=ingredient.applies_to_burger,
            applies_to_side=ingredient.applies_to_side,
            applies_to_drink=ingredient.applies_to_drink,
            applies_to_dessert=ingredient.applies_to_dessert,
        )

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "is_active": self.is_active,
            "type": self.type
        }

@dataclass
class IngredientListResponse:
    """DTO for ingredient list response"""

    ingredients: list[IngredientResponse]
    total_count: int

    def to_dict(self):
        return {
            "ingredients": [ingredient.to_dict() for ingredient in self.ingredients],
            "total_count": self.total_count,
        }

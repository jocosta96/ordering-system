from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.product import ProductCategory


class IngredientRepository(ABC):
    """
    Repository interface for Ingredient entity.

    In Clean Architecture:
    - This is part of the Application Business Rules layer
    - It defines the contract for ingredient data access
    - It's implemented by Interface Adapters layer
    - It's used by Use Cases in the Application layer
    """

    @abstractmethod
    def save(self, ingredient: Ingredient) -> Ingredient:
        """Save a ingredient and return the saved ingredient with ID"""
        pass

    @abstractmethod
    def find_by_id(self, ingredient_id: uuid.UUID) -> Optional[Ingredient]:
        """Find a ingredient by ID"""
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Ingredient]:
        """Find a ingredient by name"""
        pass

    @abstractmethod
    def find_by_type(self, type: IngredientType) -> List[Ingredient]:
        """Find ingredients by type"""
        pass

    @abstractmethod
    def find_by_applies_usage(
        self,
        category: ProductCategory
    ) -> List[Ingredient]:
        """Find ingredients by applies_to_burger, applies_to_side, applies_to_drink and applies_to_dessert"""
        pass

    @abstractmethod
    def find_all(self) -> List[Ingredient]:
        """Find all ingredients"""
        pass

    @abstractmethod
    def delete(self, ingredient_id: uuid.UUID) -> bool:
        """Delete a ingredient by ID, return True if deleted"""
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if an ingredient exists with the given name"""
        pass

    @abstractmethod
    def exists_by_type(self, type: IngredientType) -> bool:
        """Check if an ingredient exists with the given type"""
        pass

    @abstractmethod
    def find_all_active(self) -> List[Ingredient]:
        """Find all active ingredients"""
        pass
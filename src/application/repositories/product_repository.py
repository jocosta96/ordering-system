from abc import ABC, abstractmethod
from typing import List, Optional
from src.entities.product import Product, ProductCategory
from src.entities.value_objects.sku import SKU
import uuid

class ProductRepository(ABC):
    """
    Repository interface for Product entity.
    """

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Save a product and return the saved product with ID"""
        pass

    @abstractmethod
    def find_by_id(self, product_id: uuid.UUID) -> Optional[Product]:
        """Find a product by ID"""
        pass

    @abstractmethod
    def find_by_sku(self, sku: SKU) -> Optional[Product]:
        """Find a product by SKU"""
        pass

    @abstractmethod
    def find_all(self) -> List[Product]:
        """Find all products"""
        pass

    @abstractmethod
    def delete(self, product_id: uuid.UUID) -> bool:
        """Delete a product by ID"""
        pass

    @abstractmethod
    def exists_by_sku(self, sku: SKU) -> bool:
        """Check if a product exists by SKU"""
        pass

    @abstractmethod
    def exists_by_id(self, product_id: uuid.UUID) -> bool:
        """Check if a product exists by ID"""
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Check if a product exists by name"""
        pass

    @abstractmethod
    def exists_by_category(self, category: ProductCategory) -> bool:
        """Check if a product exists by category"""
        pass

    @abstractmethod
    def find_all_active(self) -> List[Product]:
        """Find all active products"""
        pass
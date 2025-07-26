from src.application.repositories.product_repository import ProductRepository
from src.application.repositories.ingredient_repository import IngredientRepository
from src.entities.product import Product, ProductCategory, ProductReceiptItem
from src.entities.value_objects.sku import SKU
from src.entities.value_objects.name import Name
from src.entities.value_objects.money import Money
from src.entities.ingredient import Ingredient, IngredientType
import uuid
from sqlalchemy.orm import declarative_base
from src.adapters.gateways.interfaces.database_interface import DatabaseInterface
from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from typing import List, Optional, Dict, Any
import json


# SQLAlchemy model
Base = declarative_base()

class ProductModel(Base):
    """SQLAlchemy model for Product table"""

    __tablename__ = "products"

    internal_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(36), nullable=False, unique=True, index=True)  # UUID as string
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(255), nullable=False)
    sku = Column(String(255), nullable=False)
    default_ingredient = Column(JSONB, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        Index('idx_product_id', 'id'),
        Index('idx_product_sku', 'sku'),
    )


class SQLProductRepository(ProductRepository):
    """
    SQL implementation of ProductRepository.
    
    In Clean Architecture:
    - This is part of the Interface Adapters layer (Gateway)
    - It implements the repository interface
    - It uses the database interface for ORM operations
    - It converts between database models and domain entities
    """

    def __init__(self, database: DatabaseInterface, ingredient_repository: Optional[IngredientRepository] = None):
        self.database = database
        self.ingredient_repository = ingredient_repository
        # Create tables
        self.database.create_tables(Base)

    def _get_session(self):
        """Get a SQLAlchemy session"""
        return self.database.get_session()

    def _to_entity(self, model: ProductModel) -> Product:
        """
        Convert a database model to an entity.
        
        Args:
            model: The database model to convert
            
        Returns:
            Product entity
            
        Raises:
            ValueError: If conversion fails due to invalid data
        """
        try:
            # Convert default_ingredient from JSONB to list of ProductReceiptItem
            default_ingredients = []
            if model.default_ingredient:
                for item_data in model.default_ingredient:
                    if isinstance(item_data, dict):
                        ingredient_id = item_data.get('ingredient_id')
                        quantity = item_data.get('quantity', 1)
                        
                        if ingredient_id and self.ingredient_repository:
                            # Convert string ingredient_id back to UUID for repository lookup
                            try:
                                ingredient_uuid = uuid.UUID(ingredient_id)
                                ingredient = self.ingredient_repository.find_by_id(ingredient_uuid)
                            except ValueError:
                                print(f"Warning: Invalid ingredient ID format: {ingredient_id}")
                                ingredient = None
                            if ingredient:
                                default_ingredients.append(ProductReceiptItem(ingredient, quantity))
                            else:
                                # Log warning about missing ingredient but continue
                                print(f"Warning: Ingredient with ID {ingredient_id} not found")
                        else:
                            # If no ingredient repository or no ingredient_id, skip this item
                            print(f"Warning: Cannot fetch ingredient for item {item_data}")
            
            # Check if we have any valid ingredients
            if not default_ingredients:
                raise ValueError("Product must have a default ingredient")

            return Product(
                id=uuid.UUID(model.id) if model.id else None,
                internal_id=model.internal_id,
                name=Name.create(model.name),
                price=Money(amount=model.price),
                category=ProductCategory(model.category),
                sku=SKU.create(model.sku),
                default_ingredient=default_ingredients,
                is_active=model.is_active,
            )
        except Exception as e:
            raise ValueError(f"Failed to convert model to entity: {str(e)}")

    def _to_model(self, product: Product) -> ProductModel:
        """
        Convert an entity to a database model.
        
        Args:
            product: The entity to convert
            
        Returns:
            ProductModel for database storage
            
        Raises:
            ValueError: If conversion fails
        """
        try:
            # Convert default_ingredient to JSONB format with only ingredient IDs
            default_ingredients_json = []
            for item in product.default_ingredient:
                if item.ingredient and item.ingredient.id:
                    default_ingredients_json.append({
                        'ingredient_id': str(item.ingredient.id),  # Convert UUID to string for JSON serialization
                        'quantity': item.quantity
                    })

            return ProductModel(
                id=str(product.id) if product.id else None,
                internal_id=product.internal_id,
                name=product.name.value,
                price=product.price.amount,
                category=product.category.value,
                sku=product.sku.value,
                default_ingredient=default_ingredients_json,
                is_active=product.is_active,
            )
        except Exception as e:
            raise ValueError(f"Failed to convert entity to model: {str(e)}")

    def save(self, product: Product) -> Product:
        """
        Save a product and return the saved product with ID.
        
        Args:
            product: The product to save
            
        Returns:
            The saved product with ID
            
        Raises:
            ValueError: If product with ID not found during update
        """
        session = self._get_session()
        try:
            if product.id:
                # Check if product exists in database
                db_product = self.database.find_by_field(
                    session, ProductModel, "id", str(product.id)
                )
                if db_product:
                    # Update existing product
                    db_product.name = product.name.value
                    db_product.price = product.price.amount
                    db_product.category = product.category.value
                    db_product.sku = product.sku.value
                    db_product.default_ingredient = self._to_model(product).default_ingredient
                    db_product.is_active = product.is_active
                    
                    self.database.update(session, db_product)
                else:
                    # Product has ID but doesn't exist in database, create new
                    db_product = self._to_model(product)
                    self.database.add(session, db_product)
            else:
                # Create new product
                db_product = self._to_model(product)
                self.database.add(session, db_product)

            self.database.commit(session)
            return self._to_entity(db_product)
        except Exception as e:
            self.database.rollback(session)
            raise e
        finally:
            self.database.close_session(session)

    def find_by_id(self, product_id: uuid.UUID, include_inactive: bool = False) -> Optional[Product]:
        """
        Find a product by ID.
        
        Args:
            product_id: The product ID to search for
            include_inactive: Whether to include inactive products
            
        Returns:
            Product entity if found, None otherwise
        """
        session = self._get_session()
        try:
            db_product = self.database.find_by_field(session, ProductModel, "id", str(product_id))
            if not db_product:
                return None
                
            # Filter by active status if not including inactive
            if not include_inactive and not db_product.is_active:
                return None
                
            try:
                return self._to_entity(db_product)
            except ValueError as e:
                print(f"Warning: Product {product_id} cannot be converted - {str(e)}")
                return None
        finally:
            self.database.close_session(session)

    def find_by_sku(self, sku: SKU, include_inactive: bool = False) -> Optional[Product]:
        """
        Find a product by SKU.
        
        Args:
            sku: The SKU object to search for
            include_inactive: Whether to include inactive products
            
        Returns:
            Product entity if found, None otherwise
        """
        session = self._get_session()
        try:
            db_product = self.database.find_by_field(session, ProductModel, "sku", sku.value)
            if not db_product:
                return None
                
            # Filter by active status if not including inactive
            if not include_inactive and not db_product.is_active:
                return None
                
            try:
                return self._to_entity(db_product)
            except ValueError as e:
                print(f"Warning: Product with SKU {sku.value} cannot be converted - {str(e)}")
                return None
        finally:
            self.database.close_session(session)

    def find_all(self, include_inactive: bool = False) -> List[Product]:
        """
        Find all products.
        
        Args:
            include_inactive: Whether to include inactive products
            
        Returns:
            List of all product entities
        """
        session = self._get_session()
        try:
            if include_inactive:
                db_products = self.database.find_all(session, ProductModel)
            else:
                # Filter only active products
                db_products = self.database.find_all_by_boolean_field(session, ProductModel, "is_active", True)
                
            products = []
            for db_product in db_products:
                try:
                    product = self._to_entity(db_product)
                    products.append(product)
                except ValueError as e:
                    # Log the error and skip products that can't be converted
                    print(f"Warning: Skipping product {db_product.id} - {str(e)}")
                    continue
            return products
        finally:
            self.database.close_session(session)

    def delete(self, product_id: uuid.UUID) -> bool:
        """
        Soft delete a product by ID (set is_active to False).
        
        Args:
            product_id: The product ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        session = self._get_session()
        try:
            db_product = self.database.find_by_field(session, ProductModel, "id", str(product_id))
            if not db_product:
                return False
                
            # Soft delete - set is_active to False
            db_product.is_active = False
            self.database.update(session, db_product)
            self.database.commit(session)
            return True
        except Exception as e:
            self.database.rollback(session)
            raise e
        finally:
            self.database.close_session(session)

    def exists_by_sku(self, sku: SKU, include_inactive: bool = False) -> bool:
        """
        Check if a product exists by SKU.
        
        Args:
            sku: The SKU object to check
            include_inactive: Whether to include inactive products
            
        Returns:
            True if exists, False otherwise
        """
        session = self._get_session()
        try:
            db_product = self.database.find_by_field(session, ProductModel, "sku", sku.value)
            if not db_product:
                return False
                
            # Check active status if not including inactive
            if not include_inactive and not db_product.is_active:
                return False
                
            return True
        finally:
            self.database.close_session(session)

    def exists_by_id(self, product_id: uuid.UUID, include_inactive: bool = False) -> bool:
        """
        Check if a product exists by ID.
        
        Args:
            product_id: The product ID to check
            include_inactive: Whether to include inactive products
            
        Returns:
            True if exists, False otherwise
        """
        session = self._get_session()
        try:
            db_product = self.database.find_by_field(session, ProductModel, "id", str(product_id))
            if not db_product:
                return False
                
            # Check active status if not including inactive
            if not include_inactive and not db_product.is_active:
                return False
                
            return True
        finally:
            self.database.close_session(session)

    def exists_by_name(self, name: str, include_inactive: bool = False) -> bool:
        """
        Check if a product exists by name.
        
        Args:
            name: The product name to check
            include_inactive: Whether to include inactive products
            
        Returns:
            True if exists, False otherwise
        """
        session = self._get_session()
        try:
            db_product = self.database.find_by_field(session, ProductModel, "name", name)
            if not db_product:
                return False
                
            # Check active status if not including inactive
            if not include_inactive and not db_product.is_active:
                return False
                
            return True
        finally:
            self.database.close_session(session)

    def exists_by_category(self, category: ProductCategory, include_inactive: bool = False) -> bool:
        """
        Check if a product exists by category.
        
        Args:
            category: The product category to check
            include_inactive: Whether to include inactive products
            
        Returns:
            True if exists, False otherwise
        """
        session = self._get_session()
        try:
            db_products = self.database.find_all_by_field(session, ProductModel, "category", category.value)
            if not db_products:
                return False
                
            # Check if any product in the category is active (if not including inactive)
            if not include_inactive:
                return any(product.is_active for product in db_products)
                
            return True
        finally:
            self.database.close_session(session)



    def find_by_name(self, name: str) -> Optional[Product]:
        """
        Find a product by name.
        
        Args:
            name: The product name to search for
            
        Returns:
            Product entity if found, None otherwise
        """
        session = self._get_session()
        try:
            db_product = self.database.find_by_field(session, ProductModel, "name", name)
            if not db_product:
                return None
            try:
                return self._to_entity(db_product)
            except ValueError as e:
                print(f"Warning: Product '{name}' cannot be converted - {str(e)}")
                return None
        finally:
            self.database.close_session(session)

    def find_by_category(self, category: ProductCategory) -> List[Product]:
        """
        Find products by category.
        
        Args:
            category: The product category to search for
            
        Returns:
            List of product entities in the specified category
        """
        session = self._get_session()
        try:
            db_products = self.database.find_all_by_field(session, ProductModel, "category", category.value)
            products = []
            for db_product in db_products:
                try:
                    product = self._to_entity(db_product)
                    products.append(product)
                except ValueError as e:
                    # Log the error and skip products that can't be converted
                    print(f"Warning: Skipping product {db_product.id} in category {category.value} - {str(e)}")
                    continue
            return products
        finally:
            self.database.close_session(session)

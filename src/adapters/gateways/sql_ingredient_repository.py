from typing import List, Optional
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from src.application.repositories.ingredient_repository import IngredientRepository
from src.entities.ingredient import Ingredient, IngredientType
from src.adapters.gateways.interfaces.database_interface import DatabaseInterface
from src.entities.value_objects.name import Name
from src.entities.value_objects.money import Money
from datetime import datetime


# SQLAlchemy model
Base = declarative_base()


class IngredientModel(Base):
    """SQLAlchemy model for Ingredient table"""

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)
    type = Column(String(100), nullable=False)
    applies_to_burger = Column(Boolean, default=False)
    applies_to_side = Column(Boolean, default=False)
    applies_to_drink = Column(Boolean, default=False)
    applies_to_dessert = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)


class SQLIngredientRepository(IngredientRepository):
    """
    SQL implementation of IngredientRepository.

    In Clean Architecture:
    - This is part of the Interface Adapters layer (Gateway)
    - It implements the repository interface
    - It uses the database interface for ORM operations
    - It converts between database models and domain entities
    """

    def __init__(self, database: DatabaseInterface):
        self.database = database
        # Create tables
        self.database.create_tables(Base)

    def _get_session(self):
        """Get a SQLAlchemy session"""
        return self.database.get_session()

    def _to_entity(self, model: IngredientModel) -> Ingredient:
        """Convert a database model to an entity"""
        return Ingredient(
            id=model.id,
            name=Name.create(model.name),
            price=Money(amount=model.price),
            is_active=model.is_active,
            type=IngredientType(model.type),
            applies_to_burger=model.applies_to_burger,
            applies_to_side=model.applies_to_side,
            applies_to_drink=model.applies_to_drink,
            applies_to_dessert=model.applies_to_dessert,
        )

    def _to_model(self, ingredient: Ingredient) -> IngredientModel:
        """Convert an entity to a database model"""
        return IngredientModel(
            id=ingredient.id,
            name=ingredient.name.value,
            price=ingredient.price.amount,
            is_active=ingredient.is_active,
            type=ingredient.type.value,
            applies_to_burger=ingredient.applies_to_burger,
            applies_to_side=ingredient.applies_to_side,
            applies_to_drink=ingredient.applies_to_drink,
            applies_to_dessert=ingredient.applies_to_dessert,
        )

    def save(self, ingredient: Ingredient) -> Ingredient:
        """Save an ingredient and return the saved ingredient with ID"""
        session = self._get_session()
        try:
            if ingredient.id:
                # Update existing ingredient
                db_ingredient = self.database.find_by_id(
                    session, IngredientModel, ingredient.id
                )
                if not db_ingredient:
                    raise ValueError(f"Ingredient with ID {ingredient.id} not found")

                db_ingredient.name = ingredient.name.value
                db_ingredient.price = ingredient.price.amount
                db_ingredient.is_active = ingredient.is_active
                db_ingredient.type = ingredient.type.value
                db_ingredient.applies_to_burger = ingredient.applies_to_burger
                db_ingredient.applies_to_side = ingredient.applies_to_side
                db_ingredient.applies_to_drink = ingredient.applies_to_drink
                db_ingredient.applies_to_dessert = ingredient.applies_to_dessert

                self.database.update(session, db_ingredient)
            else:
                # Create new ingredient
                db_ingredient = self._to_model(ingredient)
                self.database.add(session, db_ingredient)

            self.database.commit(session)
            return self._to_entity(db_ingredient)
        except Exception as e:
            self.database.rollback(session)
            raise e
        finally:
            session.close()

    def find_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        """Find an ingredient by ID"""
        session = self._get_session()
        try:
            db_ingredient = self.database.find_by_id(session, IngredientModel, ingredient_id)
            return self._to_entity(db_ingredient) if db_ingredient else None
        finally:
            session.close()

    def find_by_name(self, name: str) -> Optional[Ingredient]:
        """Find an ingredient by name"""
        session = self._get_session()
        try:
            db_ingredient = self.database.find_by_field(session, IngredientModel, "name", name)
            return self._to_entity(db_ingredient) if db_ingredient else None
        finally:
            session.close()

    def find_by_type(self, type: IngredientType) -> List[Ingredient]:
        """Find ingredients by type"""
        session = self._get_session()
        try:
            db_ingredients = session.query(IngredientModel).filter(IngredientModel.type == type.value).all()
            return [self._to_entity(db_ingredient) for db_ingredient in db_ingredients]
        finally:
            session.close()

    def find_by_applies_usage(
        self,
        applies_to_burger: bool,
        applies_to_side: bool,
        applies_to_drink: bool,
        applies_to_dessert: bool,
    ) -> List[Ingredient]:
        """Find ingredients by applies to usage"""
        session = self._get_session()
        try:
            db_ingredients = session.query(IngredientModel).filter(
                IngredientModel.applies_to_burger == applies_to_burger,
                IngredientModel.applies_to_side == applies_to_side,
                IngredientModel.applies_to_drink == applies_to_drink,
                IngredientModel.applies_to_dessert == applies_to_dessert,
            ).all()
            return [self._to_entity(db_ingredient) for db_ingredient in db_ingredients]
        finally:
            session.close()

    def find_all(self) -> List[Ingredient]:
        """Find all ingredients"""
        session = self._get_session()
        try:
            db_ingredients = self.database.find_all(session, IngredientModel)
            return [self._to_entity(db_ingredient) for db_ingredient in db_ingredients]
        finally:
            session.close()

    def delete(self, ingredient_id: int) -> bool:
        """Delete an ingredient by ID, return True if deleted"""
        session = self._get_session()
        try:
            db_ingredient = self.database.find_by_id(session, IngredientModel, ingredient_id)
            if not db_ingredient:
                return False

            self.database.delete(session, db_ingredient)
            self.database.commit(session)
            return True
        except Exception as e:
            self.database.rollback(session)
            raise e
        finally:
            session.close()

    def exists_by_name(self, name: str) -> bool:
        """Check if an ingredient exists with the given name"""
        session = self._get_session()
        try:
            return self.database.exists_by_field(session, IngredientModel, "name", name)
        finally:
            session.close()

    def exists_by_type(self, type: IngredientType) -> bool:
        """Check if an ingredient exists with the given type"""
        session = self._get_session()
        try:
            db_ingredient = self.database.find_by_field(session, IngredientModel, "type", type.value)
            return db_ingredient is not None
        finally:
            session.close()

from src.application.repositories.customer_repository import CustomerRepository
from src.application.repositories.ingredient_repository import IngredientRepository
from src.adapters.gateways.sql_customer_repository import SQLCustomerRepository
from src.adapters.gateways.sql_ingredient_repository import SQLIngredientRepository
from src.adapters.gateways.implementations.sqlalchemy_database import SQLAlchemyDatabase
from src.adapters.gateways.interfaces.database_interface import DatabaseInterface


class Container:
    """
    Dependency Injection Container.

    In Clean Architecture:
    - This wires up all the components
    - It's part of the Frameworks & Drivers layer
    - It creates the concrete implementations
    - It manages the dependency graph
    """

    def __init__(self, database_url: str = None):
        self.database_url = database_url
        self._database: DatabaseInterface = None
        self._customer_repository: CustomerRepository = None
        self._ingredient_repository: IngredientRepository = None

    @property
    def database(self) -> DatabaseInterface:
        """Get database instance"""
        if self._database is None:
            self._database = SQLAlchemyDatabase(self.database_url)
        return self._database

    @property
    def customer_repository(self) -> CustomerRepository:
        """Get customer repository instance"""
        if self._customer_repository is None:
            self._customer_repository = SQLCustomerRepository(self.database)
        return self._customer_repository

    @property
    def ingredient_repository(self) -> IngredientRepository:
        """Get ingredient repository instance"""
        if self._ingredient_repository is None:
            self._ingredient_repository = SQLIngredientRepository(self.database)
        return self._ingredient_repository

    def reset(self):
        """Reset all dependencies (useful for testing)"""
        self._database = None
        self._customer_repository = None
        self._ingredient_repository = None


# Global container instance
container = Container()

from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from src.application.repositories.customer_repository import CustomerRepository
from src.entities.customer import Customer
from src.entities.value_objects.email import Email
from src.entities.value_objects.name import Name
from src.entities.value_objects.document import Document
from src.adapters.gateways.interfaces.database_interface import DatabaseInterface


# SQLAlchemy model
Base = declarative_base()


class CustomerModel(Base):
    """SQLAlchemy model for Customer table"""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    document = Column(String(11), nullable=True, unique=True)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(String(50), nullable=True)  # For audit purposes


class SQLCustomerRepository(CustomerRepository):
    """
    SQL implementation of CustomerRepository.

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
        """Get database session"""
        return self.database.get_session()

    def _to_entity(self, model: CustomerModel) -> Customer:
        """Convert database model to domain entity"""
        return Customer(
            first_name=Name.create(model.first_name),
            last_name=Name.create(model.last_name),
            email=Email.create(model.email or ""),
            document=Document.create(model.document or ""),
            id=model.id,
        )

    def _to_model(self, customer: Customer) -> CustomerModel:
        """Convert domain entity to database model"""
        return CustomerModel(
            id=customer.id,
            first_name=customer.first_name.value,
            last_name=customer.last_name.value,
            email=customer.email.value if not customer.email.value == "" else None,
            document=customer.document.value
            if not customer.document.is_empty
            else None,
            is_anonymous=customer.is_anonymous,
        )

    def save(self, customer: Customer) -> Customer:
        """Save a customer and return the saved customer with ID"""
        session = self._get_session()
        try:
            if customer.id:
                # Update existing customer
                db_customer = self.database.find_by_id(
                    session, CustomerModel, customer.id
                )
                if not db_customer:
                    raise ValueError(f"Customer with ID {customer.id} not found")

                db_customer.first_name = customer.first_name.value
                db_customer.last_name = customer.last_name.value
                db_customer.email = (
                    customer.email.value if not customer.email.value == "" else None
                )
                db_customer.document = (
                    customer.document.value if not customer.document.is_empty else None
                )
                db_customer.is_anonymous = customer.is_anonymous

                self.database.update(session, db_customer)
            else:
                # Create new customer
                db_customer = self._to_model(customer)
                self.database.add(session, db_customer)

            self.database.commit(session)
            return self._to_entity(db_customer)
        except Exception as e:
            self.database.rollback(session)
            raise e
        finally:
            session.close()

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        """Find a customer by ID"""
        session = self._get_session()
        try:
            db_customer = self.database.find_by_id(session, CustomerModel, customer_id)
            return self._to_entity(db_customer) if db_customer else None
        finally:
            session.close()

    def find_by_document(self, document: str) -> Optional[Customer]:
        """Find a customer by document number"""
        session = self._get_session()
        try:
            db_customer = self.database.find_by_field(
                session, CustomerModel, "document", document
            )
            return self._to_entity(db_customer) if db_customer else None
        finally:
            session.close()

    def find_by_email(self, email: str) -> Optional[Customer]:
        """Find a customer by email"""
        session = self._get_session()
        try:
            db_customer = self.database.find_by_field(
                session, CustomerModel, "email", email
            )
            return self._to_entity(db_customer) if db_customer else None
        finally:
            session.close()

    def find_all(self) -> List[Customer]:
        """Find all customers"""
        session = self._get_session()
        try:
            db_customers = self.database.find_all(session, CustomerModel)
            return [self._to_entity(customer) for customer in db_customers]
        finally:
            session.close()

    def delete(self, customer_id: int) -> bool:
        """Delete a customer by ID, return True if deleted"""
        session = self._get_session()
        try:
            db_customer = self.database.find_by_id(session, CustomerModel, customer_id)
            if not db_customer:
                return False

            self.database.delete(session, db_customer)
            self.database.commit(session)
            return True
        except Exception as e:
            self.database.rollback(session)
            raise e
        finally:
            session.close()

    def get_anonymous_customer(self) -> Customer:
        """Get or create the anonymous customer"""
        session = self._get_session()
        try:
            # Try to find existing anonymous customer
            db_customer = self.database.find_by_field(
                session, CustomerModel, "is_anonymous", True
            )

            if not db_customer:
                # Create anonymous customer if it doesn't exist
                anonymous_customer = Customer.create_anonymous()
                db_customer = self._to_model(anonymous_customer)
                self.database.add(session, db_customer)
                self.database.commit(session)

            return self._to_entity(db_customer)
        except Exception as e:
            self.database.rollback(session)
            raise e
        finally:
            session.close()

    def exists_by_document(self, document: str) -> bool:
        """Check if a customer exists with the given document"""
        session = self._get_session()
        try:
            return self.database.exists_by_field(
                session, CustomerModel, "document", document
            )
        finally:
            session.close()

    def exists_by_email(self, email: str) -> bool:
        """Check if a customer exists with the given email"""
        session = self._get_session()
        try:
            return self.database.exists_by_field(session, CustomerModel, "email", email)
        finally:
            session.close()

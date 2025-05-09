from sqlalchemy import Column, Integer, Float, DateTime, String
from app.adapter.outbound.repositories.sql.orm import database

class Customer(database.Base):

    __tablename__ = "customer"

    id = Column(Integer, primary_keys=True, index=True)
    email = Column(String)
    name = Column(String)
    document = Column(String)
    
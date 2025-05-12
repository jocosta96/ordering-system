import typing

from app.domain.ports import customer_port
from app.domain.entities import customer_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import customer_sql
from app.adapter.outbound.repositories.sql.mapper import customer_sql_mapper


class CustomerRepoImpl(customer_port.CreateUserRepository):

    def __init__():
        pass
    
    def create_user():
        pass

    def read_user(self):
        pass
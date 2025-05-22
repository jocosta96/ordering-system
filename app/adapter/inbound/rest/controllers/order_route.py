from fastapi import APIRouter

from app.adapter.outbound.repositories.sql.implementation import order_impl
from app.domain.use_cases import order_uc
from app.adapter.inbound.rest.entity import order_rest
from app.adapter.inbound.rest.mapper import order_rest_mapper


repo_order = order_impl.OrderRepoImpl()
uc_order_create = order_uc.OrderCreate(repo_order)
uc_order_delete = order_uc.OrderDelete(repo_order)
uc_order_read = order_uc.OrderRead(repo_order)
uc_order_update = order_uc.OrderUpdate(repo_order)

order = APIRouter(tags=["order"], prefix="/order")

@order.get('')
def order_read(search_key, search_value):

    order = uc_order_read.read_order(search_key, search_value)

    order = order_rest_mapper.to_rest_entity(order)

    return order

@order.post('')
def order_create(order_data:order_rest.CreateOrder):

    order = order_rest_mapper.to_domain_entity(order_data)
    order.set_start_date()
    order.next_status()

    return uc_order_create.create_order(order)

@order.put('')
def order_update(search_key, search_value, order_data:order_rest.CreateOrder):
    
    order = order_rest_mapper.to_domain_entity(order_data)

    return uc_order_update.update_order(search_key, search_value, order)

@order.delete('')
def order_delete():
    pass

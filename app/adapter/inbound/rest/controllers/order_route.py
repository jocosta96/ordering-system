from fastapi import APIRouter
from typing import List

from app.adapter.outbound.repositories.sql.implementation import order_impl
from app.domain.use_cases import order_uc
from app.adapter.inbound.rest.entity import order_rest
from app.adapter.inbound.rest.mapper import order_rest_mapper
from app.domain.value_objects import status as obj_status
from app.domain.errors.custom_errors import NotFoundError

repo_order = order_impl.OrderRepoImpl()
uc_order_create = order_uc.OrderCreate(repo_order)
uc_order_delete = order_uc.OrderDelete(repo_order)
uc_order_read = order_uc.OrderRead(repo_order)
uc_order_update = order_uc.OrderUpdate(repo_order)
uc_order_list = order_uc.OrderList(repo_order)

order = APIRouter(tags=["order"], prefix="/order")


@order.get("/list")
async def order_list(search_key, search_value) -> List[order_rest.Order]:
    try:
        orders = uc_order_list.list_order(
            search_key=search_key,
            search_value=search_value
        )
        return [order_rest_mapper.to_rest_entity(o) for o in orders]
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@order.get('/{order_id}')
async def order_read(order_id: str):
    order = uc_order_read.read_order(order_id)

    print('****' * 20, order.__dict__)

    order = order_rest_mapper.to_rest_entity(order)

    return order


@order.post('')
async def order_create(order_data: order_rest.Order):
    order = order_rest_mapper.to_domain_entity(order_data)
    order.set_start_date()
    order.next_status()

    return uc_order_create.create_order(order)


@order.put('')
async def order_update(order_id: str, status: str):
    status = obj_status.OrderStatus(status=status)
    return uc_order_update.update_order(order_id, status)


@order.delete('')
async def order_delete():
    pass

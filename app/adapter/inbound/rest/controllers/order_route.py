from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from app.adapter.outbound.repositories.sql.implementation import order_impl
from app.domain.use_cases import order_uc
from app.adapter.inbound.rest.entity import order_rest
from app.adapter.inbound.rest.entity import payment_rest
from app.adapter.inbound.rest.mapper import order_rest_mapper
from app.domain.value_objects import status as obj_status
from app.domain.errors.custom_errors import NotFoundError


repo_order = order_impl.OrderRepoImpl()
uc_order_create = order_uc.OrderCreate(repo_order)
uc_order_read = order_uc.OrderRead(repo_order)
uc_order_update = order_uc.OrderUpdate(repo_order)
uc_order_payment = order_uc.OrderPay(repo_order)
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


@order.get("/queue/{status}")
async def order_list_by_status(status) -> List[order_rest.SimpleOrderReader]:
    try:
        orders = uc_order_list.list_order(
            search_key='status',
            search_value=status
        )
        return [order_rest_mapper.to_simple_reader(o) for o in orders]
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@order.get('/read/{order_id}')
async def order_read(order_id: str):
    order = uc_order_read.read_order(order_id)

    print('****' * 20, order.__dict__)

    order = order_rest_mapper.to_rest_entity(order)

    return order


@order.post('')
async def order_create(order_data: order_rest.Order):
    order = order_rest_mapper.to_domain_entity(order_data)
    order.set_start_date()

    return uc_order_create.create_order(order)


@order.patch('/update/{order_id}')
async def order_update_status(order_id: str, status: str):
    status = obj_status.OrderStatus(status=status)
    return uc_order_update.update_order(order_id, status)


@order.patch('/pay/{order_id}')
async def order_payment(payment: payment_rest.Payment, order_id):

    order = uc_order_read.read_order(order_id)
    order.validate_duplicated_payment()

    return uc_order_payment.pay_order(
        payment.order_id,
        payment.payment_date,
        payment.payment_transaction_id,
    )

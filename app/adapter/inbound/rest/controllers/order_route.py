from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from typing_extensions import Annotated
from fastapi.responses import JSONResponse

from app.adapter.outbound.repositories.sql.implementation import order_impl
from app.adapter.outbound.repositories.rest.payment import qr_code
from app.domain.use_cases import order_uc, payment_uc
from app.adapter.inbound.rest.entity import order_rest
from app.adapter.inbound.rest.entity import payment_rest
from app.adapter.inbound.rest.mapper import order_rest_mapper
from app.domain.value_objects import status as obj_status
from app.domain.errors.custom_errors import NotFoundError
from app.adapter.inbound.rest.controllers.security import check_credentials, raise_not_authorized

repo_rest_payment = qr_code.QRPayment()
repo_sql_order = order_impl.OrderRepoImpl()
uc_order_create = order_uc.OrderCreate(repo_sql_order)
uc_order_read = order_uc.OrderRead(repo_sql_order)
uc_order_update = order_uc.OrderUpdate(repo_sql_order)
uc_order_payment = order_uc.OrderPay(repo_sql_order)
uc_order_list = order_uc.OrderList(repo_sql_order)
uc_payment = payment_uc.RequestPayment(repo_rest_payment)

order = APIRouter(tags=["order"], prefix="/order")


@order.get("/list")
async def order_list(search_key=None, search_value=None) -> List[order_rest.Order]:
    try:
        orders = uc_order_list.list_order(
            search_key=search_key, search_value=search_value
        )
        return [order_rest_mapper.to_rest_entity(o) for o in orders]
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@order.get("/queue/{status}")
async def order_list_by_status(status) -> List[order_rest.SimpleOrderReader]:
    try:
        orders = uc_order_list.list_order(search_key="status", search_value=status)
        return [order_rest_mapper.to_simple_reader(o) for o in orders]
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@order.get("/read/{order_id}")
async def order_read(order_id: str) -> order_rest.Order:
    order = uc_order_read.read_order(order_id)
    if order is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found")
    order = order_rest_mapper.to_rest_entity(order)
    return order


@order.post("")
async def order_create(
    order_data: order_rest.Order,
    login: Annotated['str', Depends(check_credentials)]
) -> order_rest.SimpleOrderReader:
    
    if not login:
        raise_not_authorized()    

    order = order_rest_mapper.to_domain_entity(order_data)
    order.set_start_date()
    order_entity = uc_order_create.create_order(order)
    
    return order_rest_mapper.to_simple_reader(order_entity)


@order.patch("/update/{order_id}")
async def order_update_status(
    order_id: str,
    status: str,
    login: Annotated['str', Depends(check_credentials)]
):
    
    if not login:
        raise_not_authorized()       

    status = obj_status.OrderStatus(status=status)
    return uc_order_update.update_order(order_id, status)


@order.post("/payment_request/{order_id}")
async def request_order_payment(
    order_id,
    login: Annotated['str', Depends(check_credentials)]
):
    
    if not login:
        raise_not_authorized()
        
    order = uc_order_read.read_order(order_id)

    return uc_payment.request_payment(order.id, order.value)


@order.patch("/pay/{order_id}")
async def order_payment(
    payment: payment_rest.Payment,
    order_id,
    login: Annotated['str', Depends(check_credentials)]
):
    
    if not login:
        raise_not_authorized()
        
    order = uc_order_read.read_order(order_id)

    order.process_payment(
        dict(payment)
    )

    uc_order_payment.pay_order(
        order
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": payment.message}
    )
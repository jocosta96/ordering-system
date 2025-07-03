import requests
from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse

from app.adapter.inbound.rest.entity import payment_rest

webhook = FastAPI()

@webhook.get("/health")
def check() -> bool:
    return True


@webhook.webhooks.post('payment')
def new_payment(body: payment_rest.Payment):

    url = f'http://localhost:8080/order/pay/{body["order_id"]}'

    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Payment processed and forwarded."})
    except requests.RequestException as e:
        return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content={"error": str(e)})

import os
import httpx
import base64
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

webhook = FastAPI()


class MercadoPagoNotification(BaseModel):
    payment_date: Optional[str] = None
    payment_transaction_id: Optional[str] = None
    order_id: str


@webhook.get("/health")
def check() -> dict:
    return {"status": "ok"}

@webhook.post("/webhook/mercadopago", status_code=status.HTTP_200_OK)
async def mercadopago_webhook(notification: MercadoPagoNotification):
    url = f"http://localhost:8080/order/pay/{notification.order_id}"
    username = os.environ["API_USER"]
    password = os.environ["API_PWD"]
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=dict(notification), headers=headers)
            response.raise_for_status()
        return {"message": "Notification received and processed."}
    except httpx.RequestError as e:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY, content={"error": str(e)}
        )

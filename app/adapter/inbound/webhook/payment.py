import httpx
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    # Example: Forward notification to order service or process as needed
    url = f'http://localhost:8080/order/pay/{notification.order_id}'
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=dict(notification))
            response.raise_for_status()
        return {"message": "Notification received and processed."}
    except httpx.RequestError as e:
        return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content={"error": str(e)})

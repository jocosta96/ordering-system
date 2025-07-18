import os
import httpx
import base64
from datetime import datetime
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

webhook = FastAPI()


class MercadoPagoNotification(BaseModel):
    date: Optional[str] = None                                  
    transaction_id: Optional[str] = None
    approval_status: Optional[bool] = None
    message: Optional[str] = None
    order_id: str


@webhook.get("/health")
def check() -> dict:
    return {"status": "ok"}

@webhook.post("/webhook/mercadopago", status_code=status.HTTP_200_OK)
async def mercadopago_webhook(notification: MercadoPagoNotification):
    # Respond immediately to avoid timeout
    import asyncio
    
    # Start processing payment in background
    asyncio.create_task(process_payment_async(notification))
    
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": "Notification received, processing payment..."}
    )

async def process_payment_async(notification: MercadoPagoNotification):
    """Process payment asynchronously"""
    
    url = f"http://127.0.0.1:8080/order/pay/{notification.order_id}"
    username = os.environ["API_USER"]
    password = os.environ["API_PWD"]
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    
    try:
        # Convert date string to datetime if provided
        payment_date = None
        if notification.date:
            try:
                payment_date = datetime.fromisoformat(notification.date.replace('Z', '+00:00'))
            except ValueError:
                # If date parsing fails, use current datetime
                payment_date = datetime.now()
        
        payment_data = {
            "date": payment_date.isoformat() if payment_date else None,
            "transaction_id": notification.transaction_id,
            "approval_status": notification.approval_status,
            "message": notification.message,
            "order_id": notification.order_id
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.patch(url, json=payment_data, headers=headers)
            print(f"Payment processing completed. Status: {response.status_code}")
            response.raise_for_status()
            
    except Exception as e:
        print(f"Error processing payment asynchronously: {e}")

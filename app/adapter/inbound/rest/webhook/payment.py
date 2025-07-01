import requests
from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse

from app.adapter.inbound.rest.entity import payment_rest

app = FastAPI()

@app.webhooks.post('payment')
def new_payment(body: payment_rest.Payment):

    url = 'http://localhost:8080/fastfood/api/some-endpoint'

    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Payment processed and forwarded."})
    except requests.RequestException as e:
        return JSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content={"error": str(e)})

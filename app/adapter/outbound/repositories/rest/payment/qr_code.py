import random
import uuid
from datetime import datetime
import requests

from fastapi.responses import JSONResponse
from fastapi import status

from app.adapter.outbound.repositories.rest.payment import factory


class PaymentMock():

    def __init__(
            self, order_id: str, amount:float
        ):

        self.date = datetime.now()
        self.transaction_id = uuid.uuid4()
        self.approval_status = None
        self.message = None
        self.amount = amount
        self.order_id = order_id

        self.is_payment_successful()


    @property
    def as_dict(self):
        return {
              'date' : self.date.isoformat()
            , 'transaction_id' : str(self.transaction_id)
            , 'approval_status' : self.approval_status
            , 'message' : self.message
            , 'amount' : str(self.amount)
            , 'order_id' : str(self.order_id)
        }

    def is_payment_successful(self):

        is_approved = random.choice([True, False])

        if is_approved:
            self.approval_status = True
            self.message = 'success'
        else: 
            self.approval_status = False
            self.message = 'refused'


class QRPayment(factory.PaymentFactory):
    
    def request_payment(self, order_id, amount):
        """
        Simulate a payment by calling the payment webhook endpoint with a valid payload.
        """

        url = "http://localhost:8000/webhook/mercadopago"
        body = PaymentMock(order_id, amount).as_dict

        try:
            resp = requests.post(url, json=body, timeout=30)
            return JSONResponse(
                status_code=status.HTTP_200_OK, content={"message": resp.text}
            )

        except requests.RequestException as e:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY, content={"error": str(e)}
            )

import requests

BASE_URL = "http://192.168.49.2:30080/"


def _add_customer():
    url = BASE_URL + "customer"

    body = {
        "id": 0,
        "document": {"document": "83904593021"},
        "email": {"email": "email@domain.com"},
        "first_name": {"name": "Cliente"},
        "last_name": {"name": "Um"},
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


def _add_ingredients():
    url = BASE_URL + "ingredient"

    ingredient_list = [
        {
            "id": 1,
            "name": {"name": "ALFACE"},
            "price": {"amount": "5.00"},
            "product_category": {"category": "LANCHE"},
            "is_active": True,
        },
        {
            "id": 2,
            "name": {"name": "PAO"},
            "price": {"amount": "5.00"},
            "product_category": {"category": "LANCHE"},
            "is_active": True,
        },
        {
            "id": 3,
            "name": {"name": "QUEIJO"},
            "price": {"amount": "5.00"},
            "product_category": {"category": "LANCHE"},
            "is_active": True,
        },
    ]

    for body in ingredient_list:
        response = requests.post(url, json=body)
        response.raise_for_status()


def _add_product():
    url = BASE_URL + "product"
    body = {
        "name": {"name": "X-Burguer"},
        "category": {"category": "LANCHE"},
        "default_ingredient": [
            {
                "ingredient": {
                    "id": 1,
                    "name": {"name": "ALFACE"},
                    "price": {"amount": "5.00"},
                    "product_category": {"category": "LANCHE"},
                    "is_active": True,
                },
                "quantity": 1,
            },
            {
                "ingredient": {
                    "id": 2,
                    "name": {"name": "PAO"},
                    "price": {"amount": "5.00"},
                    "product_category": {"category": "LANCHE"},
                    "is_active": True,
                },
                "quantity": 2,
            },
            {
                "ingredient": {
                    "id": 3,
                    "name": {"name": "QUEIJO"},
                    "price": {"amount": "5.00"},
                    "product_category": {"category": "LANCHE"},
                    "is_active": True,
                },
                "quantity": 3,
            },
        ],
        "price": {"amount": 32.00},
        "sku": {"sku": "PROD-1234-XYZ"},
    }

    response = requests.post(url, json=body)
    response.raise_for_status()


def _add_order(product_id):
    url = BASE_URL + "order"
    body = {
        "customer_id": 1,
        "order_items": [
            {
                "additional_ingredient": [
                    {
                        "id": 3,
                        "name": {"name": "QUEIJO"},
                        "price": {"amount": "5.00"},
                        "product_category": {"category": "LANCHE"},
                        "is_active": True,
                    }
                ],
                "product": {
                    "name": {"name": "X-Burguer"},
                    "category": {"category": "LANCHE"},
                    "default_ingredient": [
                        {
                            "ingredient": {
                                "id": 1,
                                "name": {"name": "ALFACE"},
                                "price": {"amount": "5.00"},
                                "product_category": {"category": "LANCHE"},
                                "is_active": True,
                            },
                            "quantity": 1,
                        },
                        {
                            "ingredient": {
                                "id": 2,
                                "name": {"name": "PAO"},
                                "price": {"amount": "5.00"},
                                "product_category": {"category": "LANCHE"},
                                "is_active": True,
                            },
                            "quantity": 2,
                        },
                        {
                            "ingredient": {
                                "id": 3,
                                "name": {"name": "QUEIJO"},
                                "price": {"amount": "5.00"},
                                "product_category": {"category": "LANCHE"},
                                "is_active": True,
                            },
                            "quantity": 3,
                        },
                    ],
                    "price": {"amount": "32.00"},
                    "sku": {"sku": "PROD-1234-XYZ"},
                    "id": product_id,
                },
                "remove_ingredient": [],
            }
        ],
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
    # Return the order id from the response if available
    try:
        return response.json().get("id", 1)  # fallback to 1 if not present
    except Exception:
        return 1


def _payment_webhook(order_id):
    """
    Simulate a payment by calling the payment webhook endpoint with a valid payload.
    """
    url = "http://192.168.49.2:30000/webhook/mercadopago"  # Adjust port if needed
    body = {
        "payment_date": "2019-08-24T14:15:22Z",
        "payment_transaction_id": order_id,
        "order_id": order_id,
    }

    response = requests.post(url, json=body)
    response.raise_for_status()
    return response


def test_end_to_end():
    _add_customer()
    _add_ingredients()
    _add_product()

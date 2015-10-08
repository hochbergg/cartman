import paypalrestsdk
from config.development import PAYPAL_CLIENT_ID, PAYPAL_SECRET

FAKE_PAYMENT = {
    "intent": "authorize",
    "payer": {
        "payment_method": "credit_card",
        "funding_instruments": [{
            "credit_card": {
                "type": "visa",
                "number": "4417119669820331",
                "expire_month": "11",
                "expire_year": "2018",
                "cvv2": "874",
                "first_name": "Joe",
                "last_name": "Shopper"}}]},
    "transactions": [{
        "item_list": {
            "items": [{
                "name": "item",
                "sku": "item",
                "price": "1.00",
                "currency": "USD",
                "quantity": 1}]},
        "amount": {
            "total": "1.00",
            "currency": "USD"},
        "description": "This is the payment transaction description."
    }]
}


def configure_paypal():
    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_SECRET
    })

    return paypalrestsdk


def authorize_user():
    paypalrestsdk = configure_paypal()

    authorization = paypalrestsdk.Authorization

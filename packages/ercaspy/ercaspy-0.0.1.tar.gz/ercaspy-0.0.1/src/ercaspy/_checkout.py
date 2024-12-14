from typing import Literal
from . import config
from ._api_call import Request


class Checkout:
    @staticmethod
    def initiate(
        payment_ref: str,
        amount: int,
        customer: dict[Literal["name", "email", "phone"], str],
        currency: str = "NGN",
        description: str | None = None,
        payment_methods: str | None = None,
        fee_bearer: Literal["merchant", "customer"] | None = None,
        redirect_url: str | None = None,
        metadata: dict[str, str] | None = None,
    ):
        url = f"{config.API_URL}/payment/initiate"
        data = {
            "paymentReference": payment_ref,
            "amount": amount,
            "currency": currency,
            "customerName": customer.get("name"),
            "customerEmail": customer.get("email"),
            "customerPhoneNumber": customer.get("phone"),
            "description": description,
            "paymentMethods": payment_methods,
            "feeBearer": fee_bearer,
            "redirectUrl": redirect_url,
            "metadata": metadata,
        }

        response = Request.call(Request.Method.POST, url, data)
        return response

    @staticmethod
    def verify(transaction_ref: str):
        url = f"{config.API_URL}/payment/transaction/verify/{transaction_ref}"
        response = Request.call(Request.Method.GET, url)
        return response

    @staticmethod
    def cancel(transaction_ref: str):
        url = f"{config.API_URL}//payment/cancel/{transaction_ref}"
        response = Request.call(Request.Method.GET, url)
        return response

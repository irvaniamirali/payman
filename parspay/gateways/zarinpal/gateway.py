from typing import Optional
from parspay.http import API
from .models import Payment

ZARINPAL_API_BASE_URL = 'https://payment.zarinpal.com/pg/v{}/payment/request.json'


class ZarinPal:
    def __init__(
            self,
            merchant_id: str,
            version: Optional[int] = 4
    ):
        self.merchant_id = merchant_id
        self.version = version
        self.base_url = ZARINPAL_API_BASE_URL.format(version)
        self.client = API(base_url=self.base_url)

    async def payment(self, pay: Payment):
        ...

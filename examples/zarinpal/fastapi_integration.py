import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from payman import ZarinPal
from payman.errors.base import PaymentGatewayError
from payman.gateways.zarinpal.models import (
    PaymentRequest,
    PaymentResponse,
    PaymentVerifyRequest,
    PaymentVerifyResponse
)

# Initialize ZarinPal client
pay = ZarinPal(merchant_id="12345678-1234-1234-1234-123456789012", sandbox=True)

app = FastAPI()

@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if isinstance(e, PaymentGatewayError):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/pay", response_model=PaymentResponse)
async def initiate_payment(request: PaymentRequest):
    return await pay.payment(request)

@app.get("/redirect-to-payment-page/{authority}")
async def redirect_to_payment_page(authority: str):
    redirect_url = pay.payment_url_generator(authority)
    return RedirectResponse(redirect_url)

@app.post("/verify-payment", response_model=PaymentVerifyResponse)
async def verify_payment(request: PaymentVerifyRequest):
    return await pay.verify(request)

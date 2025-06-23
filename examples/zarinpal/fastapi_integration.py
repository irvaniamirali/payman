from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from payman.gateways.zarinpal import ZarinPal
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

@app.post("/payment", response_model=PaymentResponse)
async def initiate_payment(request: PaymentRequest):
    return await pay.payment(request)

@app.get("/payment/redirect/{authority}", response_class=RedirectResponse)
async def redirect_to_payment(authority: str):
    payment_redirect_url = pay.payment_url_generator(authority)
    return RedirectResponse(payment_redirect_url)

@app.post("/verify", response_model=PaymentVerifyResponse)
async def verify(request: PaymentVerifyRequest):
    return await pay.verify(request)

@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if isinstance(e, PaymentGatewayError):
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

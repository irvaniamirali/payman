from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from payman import Payman
from payman.gateways.zarinpal.models import (
    PaymentRequest,
    VerifyRequest,
    VerifyResponse,
    CallbackParams,
)
from payman.errors import GatewayError
from uuid import uuid4

app = FastAPI()

AMOUNT = 10_000
CALLBACK_URL = "http://127.0.0.1:8000/callback"

def get_gateway() -> Payman:
    """Returns a Payman instance for the ZarinPal gateway."""
    return Payman("zarinpal", merchant_id=str(uuid4()), sandbox=True)  # sandbox mode

@app.post("/pay", summary="Start a new payment", response_class=RedirectResponse)
async def start_payment(pay: Payman = Depends(get_gateway)):
    """
    Initiate a new payment request and redirect the user to the payment gateway.
    """
    try:
        request = PaymentRequest(
            amount=AMOUNT,
            callback_url=CALLBACK_URL,
            description="Test Order",
        )
        response = await pay.payment(request)
        return RedirectResponse(url=pay.get_payment_redirect_url(response.authority))

    except GatewayError as e:
        raise HTTPException(status_code=502, detail="Gateway error occurred")


@app.get("/callback", response_model=VerifyResponse, summary="Handle payment callback")
async def handle_callback(pay: Payman = Depends(get_gateway), callback: CallbackParams = Depends()):
    """
    Handle the callback from the payment gateway and verify the transaction.
    """
    if not callback.is_success:
        return JSONResponse(
            status_code=400,
            content={"message": "Payment was cancelled or failed."},
        )

    try:
        verify = await pay.verify(
            VerifyRequest(authority=callback.authority, amount=AMOUNT)
        )

        if verify.success:
            return JSONResponse(
                content={
                    "message": "Payment verified successfully!",
                    "verify_data": verify.model_dump(),
                }
            )
        return JSONResponse(
            status_code=400,
            content={"message": f"Verification failed: {verify.message}"},
        )

    except GatewayError as e:
        raise HTTPException(status_code=502, detail="Gateway error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from payman import Payman, GatewayError
from zibal import Zibal  # for type hint
from zibal.models import CallbackParams, PaymentRequest, VerifyRequest, VerifyResponse

app = FastAPI()

AMOUNT = 10_000
CALLBACK_URL = "http://127.0.0.1:8000/callback"


def get_zibal_gateway() -> Zibal:
    """Return a configured Payman instance for Zibal."""
    return Payman("zibal", merchant_id="zibal")  # sandbox mode

@app.post("/pay", response_class=RedirectResponse, status_code=302)
async def start_payment(pay: Zibal = Depends(get_zibal_gateway)):
    """
    Initiate a payment and redirect the user to Zibal gateway.
    """
    payment_request = PaymentRequest(
        amount=AMOUNT,
        callback_url=CALLBACK_URL,
        description="Test Order",
        order_id="order-123",
        mobile="09120000000",
    )

    try:
        response = await pay.initiate_payment(payment_request)
        payment_url = pay.get_payment_redirect_url(response.track_id)
        return RedirectResponse(url=payment_url)

    except GatewayError as e:
        raise HTTPException(status_code=502, detail=f"Payment initiation failed: {e}")


@app.get("/callback", response_model=dict)
async def handle_callback(
    callback: CallbackParams = Depends(), pay: Zibal = Depends(get_zibal_gateway)
):
    """
    Handle Zibal payment callback and verify payment status.
    """
    if not callback.is_success:
        return JSONResponse(
            status_code=400,
            content={"message": "Payment was not successful or cancelled."},
        )

    try:
        verify_request = VerifyRequest(track_id=callback.track_id)
        verify_response: VerifyResponse = await pay.verify_payment(verify_request)

        if verify_response.success:
            return {
                "message": "Payment verified successfully!",
                "verify_data": verify_response.model_dump(),
            }

        return JSONResponse(
            status_code=400,
            content={"message": f"Verification failed: {verify_response.message}"},
        )

    except GatewayError as e:
        raise HTTPException(status_code=502, detail=f"Verification error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

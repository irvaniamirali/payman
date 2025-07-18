from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from payman import Payman
from payman.gateways.zibal.models import (
    PaymentRequest,
    VerifyRequest,
    CallbackParams,
    VerifyResponse
)
from payman.errors import GatewayError

app = FastAPI()

AMOUNT = 10_000
CALLBACK_URL = "http://127.0.0.1:8000/callback"

def get_gateway() -> Payman:
    """Returns a Payman instance for the Zibal gateway."""
    return Payman("zibal", merchant_id="zibal")  # sandbox mode

@app.post("/pay", response_class=RedirectResponse, status_code=302)
async def start_payment(pay: Payman = Depends(get_gateway)):
    """
    Create a payment request and redirect the user to the payment gateway.
    """
    payment = PaymentRequest(
        amount=AMOUNT,
        callback_url=CALLBACK_URL,
        description="Test Order",
        order_id="order-123",
        mobile="09120000000"
    )

    try:
        response = await pay.payment(payment)
        payment_url = pay.get_payment_redirect_url(response.track_id)
        return RedirectResponse(url=payment_url)

    except GatewayError as e:
        raise HTTPException(status_code=502, detail="Payment initiation failed.")


@app.get("/callback", response_model=dict)
async def handle_callback(
    callback: CallbackParams = Depends(),
    pay: Payman = Depends(get_gateway)
):
    """
    Handle the payment gateway callback from Zibal.
    Expects query parameters: trackId, status, success, orderId.
    """
    try:
        if not callback.is_success:
            return JSONResponse(
                status_code=400,
                content={"message": "Payment was not successful or cancelled."}
            )

        verify_request = VerifyRequest(track_id=callback.track_id)
        verify_response: VerifyResponse = await pay.verify(verify_request)

        if verify_response.success:
            return {
                "message": "Payment verified successfully!",
                "verify_data": verify_response.model_dump()
            }

        return JSONResponse(
            status_code=400,
            content={"message": f"Verification failed: {verify_response.message}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

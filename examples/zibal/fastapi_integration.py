from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from payman import Zibal
from payman.gateways.zibal.models import PaymentRequest, VerifyRequest, CallbackParams
from payman.gateways.zibal.enums import Status
from payman.errors import PaymentGatewayError
from payman.gateways.zibal.errors import PaymentNotSuccessfulError
import logging

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize the Zibal gateway
pay = Zibal(merchant_id="zibal")  # sandbox mode


@app.post("/pay")
async def start_payment():
    """
    Create a payment request and redirect the user to the payment gateway.
    """
    try:
        payment = PaymentRequest(
            amount=10000,
            callback_url="http://localhost:8000/callback",
            description="Test Order",
            order_id="order-123",
            mobile="09120000000"
        )
        response = await pay.payment(payment)
        payment_url = pay.get_payment_redirect_url(response.track_id)
        return RedirectResponse(url=payment_url)
    except PaymentGatewayError as e:
        logger.exception("Failed to initiate payment")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/callback")
async def handle_callback(request: Request):
    """
    Handle the payment gateway callback.
    Zibal sends `trackId` and `status`, `success`, `orderId` as query params.
    """
    try:
        params = dict(request.query_params)
        callback_data = CallbackParams(**params)

        if not callback_data.is_successful():
            return JSONResponse(
                status_code=400,
                content={"message": "Payment was not successful or was cancelled by the user."}
            )

        verify_response = await pay.verify(
            VerifyRequest(track_id=callback_data.track_id)
        )

        if verify_response.result == 100:
            return JSONResponse(content={
                "message": "Payment verified successfully!",
                "verify_data": verify_response,
            })
        else:
            return JSONResponse(
                status_code=400,
                content={"message": f"Verification failed: {verify_response.message}"}
            )

    except PaymentNotSuccessfulError as e:
        return JSONResponse(status_code=400, content={"message": f"Payment failed: {e.message}"})
    except Exception as e:
        logger.exception(f"Unhandled exception during payment callback: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

import asyncio
import logging
from payman import Zibal
from payman.gateways.zibal.models import PaymentRequest, VerifyRequest, CallbackParams
from payman.gateways.zibal.enums import Status
from payman.errors import PaymentGatewayError
from payman.gateways.zibal.errors import PaymentNotSuccessfulError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Zibal gateway (sandbox mode)
pay = Zibal(merchant_id="zibal")  # `zibal` for sandbox mode


async def create_payment() -> int:
    """
    Sends a payment request to Zibal and returns the track ID.
    """
    request = PaymentRequest(
        amount=10000,
        callback_url="https://yourapp.com/callback",
        description="Test payment",
        order_id="order-xyz-001",
        mobile="09121234567",
    )

    try:
        response = await pay.payment(request)
        logger.info(f"Payment request successful. Track ID: {response.track_id}")
        payment_url = pay.get_payment_redirect_url(response.track_id)
        logger.info(f"Redirect the user to: {payment_url}")
        return response.track_id
    except PaymentGatewayError as e:
        logger.error(f"Failed to initiate payment: {e}")
        raise


async def simulate_callback(track_id: int) -> CallbackParams:
    """
    Simulates Zibal's callback after user payment (for testing).
    In a real app, this would come from the HTTP request parameters.
    """
    # Simulating a successful payment
    return CallbackParams(
        track_id=track_id,
        success=1,
        status=100,
        order_id="order-xyz-001"
    )


async def verify_payment(track_id: int):
    """
    Verifies the payment after receiving the callback.
    """
    try:
        response = await pay.verify(VerifyRequest(track_id=track_id))
        logger.info("Payment verified successfully!")
        logger.info(f"Track ID: {response.track_id}")
        logger.info(f"Paid at: {response.paid_at}")
    except PaymentNotSuccessfulError as e:
        logger.warning(f"Payment was not successful: {e.message}")
    except PaymentGatewayError as e:
        logger.error(f"Payment verification failed: {e}")


async def main():
    track_id = await create_payment()

    # Simulate user completing the payment
    logger.info("Waiting for user to complete payment...")
    await asyncio.sleep(10)

    callback = await simulate_callback(track_id)

    if callback.status == Status.SUCCESS:
        await verify_payment(callback.track_id)
    else:
        logger.warning("User cancelled the payment or transaction failed.")


if __name__ == "__main__":
    asyncio.run(main())

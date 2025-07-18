import asyncio
import logging
from payman import Payman
from payman.gateways.zibal.models import CallbackParams
from payman.errors import GatewayError
from payman.gateways.zibal.errors import PaymentNotSuccessfulError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AMOUNT = 10_000
CALLBACK_URL = "https://yourapp.com/callback"

# Initialize Zibal gateway (sandbox mode)
pay = Payman("zibal", merchant_id="zibal")  # `zibal` for sandbox mode


async def create_payment() -> int:
    """
    Sends a payment request to Zibal and returns the track ID.
    """
    try:
        response = await pay.payment(
            amount=AMOUNT,
            callback_url=CALLBACK_URL,
            description="Test payment",
            order_id="order-xyz-001",
            mobile="09121234567"
        )
        logger.info(f"Payment request successful. Track ID: {response.track_id}")
        payment_url = pay.get_payment_redirect_url(response.track_id)
        logger.info(f"Redirect the user to: {payment_url}")
        return response.track_id
    except GatewayError as e:
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
        response = await pay.verify(track_id=track_id)
        logger.info("Payment verified successfully!")
        logger.info(f"Track ID: {response.track_id}")
        logger.info(f"Paid at: {response.paid_at}")
    except PaymentNotSuccessfulError as e:
        logger.warning(f"Payment was not successful: {e.message}")
    except GatewayError as e:
        logger.error(f"Payment verification failed: {e}")


async def main():
    track_id = await create_payment()

    # Simulate user completing the payment
    logger.info("Waiting for user to complete payment...")
    await asyncio.sleep(10)

    callback = await simulate_callback(track_id)

    if callback.is_successful:
        await verify_payment(callback.track_id)
    else:
        logger.warning("User cancelled the payment or transaction failed.")


if __name__ == "__main__":
    asyncio.run(main())

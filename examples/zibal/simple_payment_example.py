import asyncio
import logging

from payman import Payman, GatewayError
from zibal.exceptions import PaymentNotSuccessfulError
from zibal.models import CallbackParams

# -----------------------------
# Logging configuration
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Configuration
# -----------------------------
AMOUNT = 10_000
CALLBACK_URL = "https://yourapp.com/callback"
ORDER_ID = "order-xyz-001"
MOBILE = "09121234567"

# -----------------------------
# Initialize Zibal gateway
# -----------------------------
pay = Payman("zibal", merchant_id="zibal")  # Sandbox mode


# -----------------------------
# Payment operations
# -----------------------------
async def create_payment() -> int:
    """Send payment request to Zibal and return track ID."""
    try:
        response = await pay.initiate_payment(
            amount=AMOUNT,
            callback_url=CALLBACK_URL,
            description="Test payment",
            order_id=ORDER_ID,
            mobile=MOBILE,
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
    Simulate Zibal callback for testing.
    In real apps, these params come from HTTP request.
    """
    logger.info("Simulating payment callback...")
    # Simulate a successful payment
    return CallbackParams(track_id=track_id, success=1, status=1, order_id=ORDER_ID)


async def verify_payment(track_id: int):
    """Verify payment status via Zibal."""
    try:
        response = await pay.verify_payment(track_id=track_id)
        logger.info("Payment verified successfully!")
        logger.info(f"Track ID: {response.track_id}, Paid at: {response.paid_at}")

    except PaymentNotSuccessfulError as e:
        logger.warning(f"Payment not successful: {e.message}")

    except GatewayError as e:
        logger.error(f"Payment verification failed: {e}")


# -----------------------------
# Main workflow
# -----------------------------
async def main():
    track_id = await create_payment()

    logger.info("Waiting for user to complete payment...")
    await asyncio.sleep(10)  # Simulate user action

    callback = await simulate_callback(track_id)

    if callback.is_success:
        await verify_payment(callback.track_id)
    else:
        logger.warning("Payment was cancelled or failed.")


if __name__ == "__main__":
    asyncio.run(main())

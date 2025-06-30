import asyncio
import logging
import uuid
from payman import ZarinPal
from payman.gateways.zarinpal.models import PaymentRequest, VerifyRequest, CallbackParams
from payman.errors import PaymentGatewayError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize ZarinPal gateway (sandbox mode)
pay = ZarinPal(merchant_id=str(uuid.uuid4()).replace("-", ''))


async def create_payment() -> str:
    """
    Sends a payment request to ZarinPal and returns the authority.
    """
    request = PaymentRequest(
        amount=10000,
        callback_url="https://yourapp.com/callback",
        description="Test payment"
    )

    try:
        response = await pay.payment(request)
        logger.info(f"Payment request successful. Authority: {response.authority}")
        payment_url = pay.get_payment_redirect_url(response.authority)
        logger.info(f"Redirect the user to: {payment_url}")
        return response.authority
    except PaymentGatewayError as e:
        logger.error(f"Failed to initiate payment: {e}")
        raise


async def simulate_callback(authority: str) -> CallbackParams:
    """
    Simulates ZarinPal's callback after user payment (for testing).
    In a real app, this would come from the HTTP request parameters.
    """
    # Simulating a successful payment
    return CallbackParams(
        authority=authority,  # authority is usually a hash string in reality
        status="OK"
    )


async def verify_payment(authority: str):
    """
    Verifies the payment after receiving the callback.
    """
    try:
        response = await pay.verify(VerifyRequest(authority=authority))
        logger.info("Payment verified successfully!")
        logger.info(f"Authority: {response.authority}")
        logger.info(f"Ref ID: {response.ref_id}")
    except PaymentGatewayError as e:
        logger.error(f"Payment verification failed: {e}")


async def main():
    authority = await create_payment()

    # Simulate user completing the payment
    logger.info("Waiting for user to complete payment...")
    await asyncio.sleep(10)

    callback = await simulate_callback(authority)

    if callback.is_successful():
        await verify_payment(callback.authority)
    else:
        logger.warning("User cancelled the payment or transaction failed.")


if __name__ == "__main__":
    asyncio.run(main())

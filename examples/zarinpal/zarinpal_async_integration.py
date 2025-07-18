import asyncio
import logging
import uuid
from payman import Payman
from payman.gateways.zarinpal.models import CallbackParams
from payman.errors import GatewayError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AMOUNT = 10_000
CALLBACK_URL = "https://yourapp.com/callback"

pay = Payman("zarinpal", merchant_id=str(uuid.uuid4()), sandbox=True)

async def create_payment(pay: Payman) -> str:
    response = await pay.payment(
        amount=AMOUNT,
        callback_url=CALLBACK_URL,
        description="Test payment"
    )
    authority = response.authority
    logger.info(f"Payment request successful. Authority: {authority}")
    logger.info(f"Redirect user to: {pay.get_payment_redirect_url(authority)}")
    return authority


async def simulate_callback(authority: str) -> CallbackParams:
    # In a real-world scenario, this would be extracted from the HTTP GET parameters.
    return CallbackParams(authority=authority, status="OK")


async def verify_payment(pay: Payman, authority: str, amount: int) -> None:
    response = await pay.verify(authority=authority, amount=amount)
    logger.info(f"Payment verified! Ref ID: {response.ref_id}")


async def run_payment_flow():
    try:
        authority = await create_payment(pay)
        print("Simulating user payment flow...")
        await asyncio.sleep(10)  # Simulated delay

        callback = await simulate_callback(authority)

        if callback.is_success:
            await verify_payment(pay, callback.authority, AMOUNT)
        else:
            logger.error("Payment failed or cancelled by user.")
    except GatewayError as e:
        logger.error(f"Gateway error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(run_payment_flow())

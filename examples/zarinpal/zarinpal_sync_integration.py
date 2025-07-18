import time
import uuid
import logging
from payman import Payman
from payman.gateways.zarinpal.models import CallbackParams
from payman.errors import GatewayError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AMOUNT = 10_000
CALLBACK_URL = "https://yourapp.com/callback"

pay = Payman("zarinpal", merchant_id=str(uuid.uuid4()), sandbox=True)

def create_payment(pay: Payman) -> str:
    response = pay.payment(
        amount=AMOUNT,
        callback_url=CALLBACK_URL,
        description="Test payment"
    )
    authority = response.authority
    logger.info(f"Payment request successful. Authority: {authority}")
    logger.info(f"Redirect user to: {pay.get_payment_redirect_url(authority)}")
    return authority


def simulate_callback(authority: str) -> CallbackParams:
    # In a real-world scenario, this would be extracted from the HTTP GET parameters.
    return CallbackParams(authority=authority, status="OK")


def verify_payment(pay: Payman, authority: str, amount: int) -> None:
    response = pay.verify(authority=authority, amount=amount)
    logger.info(f"Payment verified! Ref ID: {response.ref_id}")


def run_payment_flow(amount: int = 10000):
    try:
        authority = create_payment(pay)
        logger.info("Simulating user payment flow...")
        time.sleep(10)  # Simulated delay

        callback = simulate_callback(authority)

        if callback.is_success:
            verify_payment(pay, callback.authority, amount)
        else:
            logger.error("Payment failed or cancelled by user.")
    except GatewayError as e:
        logger.error(f"Gateway error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    run_payment_flow()

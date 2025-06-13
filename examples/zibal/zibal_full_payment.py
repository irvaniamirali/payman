import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from payman.gateways import Zibal
from payman.gateways.zibal.models import (
    PaymentRequest,
    PaymentVerifyRequest,
    CallbackParams,
)
import asyncio

# Initialize Zibal client with your merchant ID
zibal = Zibal(merchant="zibal")  # sandbox mode

async def simulate_payment():
    request_data = PaymentRequest(
        amount=10000,
        callback_url="https://example.com/callback",
        description="Test transaction",
        mobile="09120000000",
        order_id="test-order-123"
    )

    try:
        payment_resp = await zibal.request_payment(request_data)
        print(f"Payment request sent. Track ID: {payment_resp.track_id}")
    except Exception as e:
        print(f"Payment request failed: {e}")
        return

    payment_url = zibal.payment_url_generator(payment_resp.track_id)
    print(f"Redirect user to: {payment_url}")

    await asyncio.sleep(10)  # simulate user payment delay

    # Simulate callback params (can toggle success to 0 for failure test)
    callback_data = CallbackParams(track_id=payment_resp.track_id, success=1)

    if callback_data.success == 1:
        verify_request = PaymentVerifyRequest(track_id=callback_data.track_id)

        try:
            verify_resp = await zibal.verify(verify_request)
        except Exception as e:
            print(f"Payment verification failed with error: {e}")
            return

        if verify_resp.result == 100:
            print("Payment verified successfully!")
            print(f"Full Response: {verify_resp}")
        else:
            print(f"Verification failed: {verify_resp.message}")
    else:
        print("Payment was not successful or was cancelled by the user.")


if __name__ == "__main__":
    asyncio.run(simulate_payment())

import sys
import os

# Add project root to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import asyncio
import uuid
from payman import Payman
from payman.gateways.zarinpal import ZarinPal
from payman.gateways.zarinpal.models import (
    CallbackParams,
    PaymentRequest,
    PaymentMetadata,
    PaymentVerifyRequest
)

# Initialize ZarinPal client in sandbox mode
zarinpal = ZarinPal(
    merchant_id=str(uuid.uuid4()),
    sandbox=True
)

pay = Payman(gateway=zarinpal)

async def main():
    # Prepare payment request
    payment_data = PaymentRequest(
        amount=10000,
        description="Monthly subscription",
        callback_url="https://example.com/zarinpal/callback",
        metadata=PaymentMetadata(
            mobile="09123456789",
            order_id="INV-2025-001"
        )
    )

    # Send payment creation request
    try:
        response = await zarinpal.create_payment(payment_data)
    except Exception as e:
        print("Error creating payment:", e)
        return

    print("Authority code:", response.authority)
    print("Payment URL:", zarinpal.generate_payment_url(response.authority))

    await asyncio.sleep(15)  # Simulate waiting for user to complete payment

    # Simulate callback from ZarinPal after payment
    callback = CallbackParams(status="OK", authority=response.authority)

    try:
        await zarinpal.process_payment_callback(callback)
    except Exception as e:
        print("Payment was cancelled or failed:", e)
        return

    # Verify payment
    verify_data = PaymentVerifyRequest(
        authority=response.authority,
        amount=payment_data.amount
    )

    try:
        verify_response = await zarinpal.verify_payment(verify_data)
        print("Payment verified successfully!")
        print("Reference ID:", verify_response.ref_id)
        print("Card PAN:", verify_response.card_pan)
        print("Fee:", verify_response.fee, "IRR")
    except Exception as e:
        print("Unknown error:\n", e)

asyncio.run(main())

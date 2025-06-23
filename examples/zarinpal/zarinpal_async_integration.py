import asyncio
from payman import ZarinPal
from payman.gateways.zarinpal.models import PaymentRequest, PaymentMetadata, PaymentVerifyRequest

# Initialize ZarinPal client in sandbox mode
pay = ZarinPal(
    merchant_id="12345678-1234-1234-1234-123456789012",
    sandbox=True
)

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
    response = await pay.payment(payment_data)

    print("Authority code:", response.authority)
    print("Payment URL:", pay.payment_url_generator(response.authority))

    await asyncio.sleep(10)  # Simulate waiting for user to complete payment

    # Verify payment
    verify_data = PaymentVerifyRequest(
        authority=response.authority,
        amount=payment_data.amount
    )
    verify_response = await pay.verify(verify_data)
    print("Payment verified successfully!")
    print("Reference ID:", verify_response.ref_id)
    print("Card PAN:", verify_response.card_pan)
    print("Fee:", verify_response.fee, "IRR")

asyncio.run(main())

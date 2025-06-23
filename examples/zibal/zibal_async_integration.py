import asyncio
from payman import Zibal
from payman.gateways.zibal.models import PaymentRequest, PaymentVerifyRequest, CallbackParams

# Initialize Zibal client with your merchant ID
pay = Zibal(merchant="zibal")  # sandbox mode

async def main():
    payment_data = PaymentRequest(
        amount=1000,
        callback_url="https://example.com/callback",
        description="Test transaction",
        mobile="09120000000",
        order_id="test-order-123"
    )
    payment_response = await pay.payment(payment_data)
    print(f"Payment request sent. Track ID: {payment_response.track_id}")

    payment_url = pay.payment_url_generator(payment_response.track_id)
    print(f"Redirect user to: {payment_url}")

    await asyncio.sleep(10)  # simulate user payment delay

    # Simulate callback params (can toggle success to 0 for failure test)
    callback_data = CallbackParams(track_id=payment_response.track_id, success=1)

    if callback_data.success == 1:
        verify_response = await pay.verify(PaymentVerifyRequest(track_id=callback_data.track_id))

        if verify_response.result == 100:
            print("Payment verified successfully!")
            print(f"Full Response: {verify_response}")
        else:
            print(f"Verification failed: {verify_response.message}")
    else:
        print("Payment was not successful or was cancelled by the user.")

if __name__ == "__main__":
    asyncio.run(main())

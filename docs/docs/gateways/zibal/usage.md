# Using Zibal Gateway with Payman

This section guides you on how to integrate the [Zibal](https://zibal.ir/) payment gateway using the Payman Python package.
You will find examples for both asynchronous and synchronous usage to suit various application types.


## Quick Start Guide for Zibal Integration

Follow these simple steps to integrate Zibal payment gateway with Payman:

### 1. Initialize the Gateway
Import `Zibal` and create an instance with your merchant ID:

```python
from payman import Zibal

pay = Zibal(merchant_id="YOUR-MERCHANT-ID")
```

#### Note: Test Mode for Development
Zibal provides a test mode that allows you to safely test payment flows without real transactions.
To use Zibal in test mode:

- Set your `merchant_id` to the string "zibal", which activates test behavior automatically.

Example:

```python
from payman import Zibal

pay = Zibal(merchant_id="zibal")
```
This will trigger mock responses from Zibal, allowing you to fully test your integration in a safe, non-production environment.

---

### 2. Create a Payment Request
Prepare and send a payment request to Zibal with the desired amount and callback URL.

```python
from payman.gateways.zibal.models import PaymentRequest

amount = 10000  # IRR

payment_response = pay.payment(
    PaymentRequest(
        amount=amount,
        callback_url="https://example.com/callback",
        description="Test Payment",
    )
)
track_id = payment_response.track_id
print(f"Track ID: {track_id}")
```

---

### 3. Redirect User to Payment URL
Use the `track_id` returned from the payment request to generate the redirect URL for the user.
```python
payment_redirect_url = pay.get_payment_redirect_url(track_id=track_id)
print(payment_redirect_url)
```
This URL should be used to redirect the user to Zibal's payment page.

---

### 4. Receive Callback
After the payment process, Zibal will redirect the user back to your `callback_url` with payment result parameters via a `GET` request.

The key query parameters are:

- `trackId`: A unique identifier for the transaction.
- `success`: 1 if the transaction was successful, 0 otherwise.

You can validate these using CallbackParams:
```python
from payman.gateways.zibal.models import CallbackParams

# This is an example. In production, extract from your framework's request:
callback = CallbackParams(track_id=track_id, success=1, status=100, order_id="my-order-id")
if callback.is_successful():
    print("Transaction succeeded!")
```
In FastAPI, Flask, or Django, you'll extract these values from the incoming request query params.

Example callback URL:
```python
https://example.com/callback?trackId=123456&success=1&status=100&orderId=my-order-id
```

---

### 5. Verify Payment
Once the user is redirected back, use the `track_id` to verify the payment with Zibal.

```python
from payman.gateways.zibal.models import VerifyRequest

verify_response = pay.verify(
    VerifyRequest(track_id=track_id)
)
ref_number = verify_response.ref_number
print(f"Bank Ref Number: {ref_number}")
```

---

> NOTE: **Payman supports both sync and async code.**
> All gateway methods like `payment()` and `verify()` can be called with or without `await`, depending on your application's architecture.

---

## Summary
| Step        | Description                                 |
| ----------- | ------------------------------------------- |
| 1. Init     | Create `Zibal` with your merchant ID        |
| 2. Payment  | Send payment request and receive `track_id` |
| 3. Redirect | Redirect user to Zibal payment page         |
| 4. Callback | Receive result on your callback URL         |
| 5. Verify   | Confirm transaction status with `track_id`  |

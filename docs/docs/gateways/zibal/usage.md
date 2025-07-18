# Using Zibal Gateway with Payman

This section guides you on how to integrate the [Zibal](https://zibal.ir/) payment gateway using the Payman Python package.
You will find examples for both asynchronous and synchronous usage to suit various application types.


## Quick Start Guide for Zibal Integration

Follow these simple steps to integrate Zibal payment gateway with Payman:

### 1. Initialize the Gateway
Import `Payman` and create an instance with your merchant ID:

```python
from payman import Payman

pay = Payman("zibal", merchant_id="YOUR-MERCHANT-ID")
```

#### Note: Test Mode for Development
Zibal provides a test mode that allows you to safely test payment flows without real transactions.
To use Zibal in test mode:

- Set your `merchant_id` to the string "zibal", which activates test behavior automatically.

Example:

```python
from payman import Payman

pay = Payman("zibal", merchant_id="zibal")
```
This will trigger mock responses from Zibal, allowing you to fully test your integration in a safe, non-production environment.

---

### 2. Create a Payment Request
Prepare and send a payment request to Zibal with the desired amount and callback URL.

```python
amount = 10_000  # IRR

payment_response = pay.payment(
    amount=amount,
    callback_url="https://example.com/callback",
    description="Test Payment",
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
verify_response = pay.verify(track_id=track_id)

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



## Flexible Input Support

All `Payman` methods such as `payment(...)` and `verify(...)` accept input in **three flexible formats**:

- ✅ Pydantic model  
- ✅ Plain dictionary  
- ✅ Keyword arguments (`kwargs`)

This allows you to choose the most convenient style for your use case.

### Example: `payment(...)` in all supported formats

```python
from payman import Payman
from payman.gateways.zibal.models import PaymentRequest

pay = Payman("zibal", merchant_id="...")

# 1. Using a Pydantic model
resp1 = pay.payment(PaymentRequest(
    amount=10_000,
    callback_url="https://site.com/callback",
    description="Test A"
))

# ✅ 2. Using a dictionary
resp2 = pay.payment({
    "amount": 10_000,
    "callback_url": "https://site.com/callback",
    "description": "Test B"
})

# ✅ 3. Using keyword arguments
resp3 = pay.payment(
    amount=10_000,
    callback_url="https://site.com/callback",
    description="Test C"
)
```
All three are fully supported and behave exactly the same.

### Input Validation with Pydantic

Regardless of how you provide input—whether as a **Pydantic model**, a **plain dictionary**, or **keyword arguments** (`kwargs`)—all data is strictly validated using **Pydantic**.

This means:

- Field types are enforced (e.g., amount must be an int)

- Required fields are checked

- Invalid or malformed values raise immediate validation errors

- You get clear and informative pydantic.ValidationError exceptions when something is wrong

This design gives you full flexibility while ensuring that all inputs are consistently validated behind the scenes.


#### Example: Flexible Input, Strict Validation
```python
# Even when using kwargs or a dict, Pydantic validation applies
pay.payment(
    amount="invalid",  # ❌ raises ValidationError
    callback_url="https://your-site.com",
    description="Example"
)
```
You can also catch and handle validation errors gracefully:
```python
from pydantic import ValidationError

try:
    pay.payment(amount="bad", callback_url=..., description=...)
except ValidationError as e:
    print("Invalid input:", e)
```

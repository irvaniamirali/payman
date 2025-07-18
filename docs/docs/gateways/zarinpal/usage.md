# Using ZarinPal Gateway with Payman
This section guides you on how to integrate the [ZarinPal](https://www.zarinpal.com/) payment gateway using the Payman Python package.
You will find examples for both asynchronous and synchronous usage to fit different application needs.

## Quick Start Guide for ZarinPal Integration
Follow these simple steps to integrate ZarinPal payment gateway with Payman:

### 1. Initialize the Gateway
Import `Payman` and create an instance with your merchant ID:

```python
from payman import Payman

pay = Payman("zarinpal", merchant_id="YOUR-MERCHANT-ID")
```

#### Note: Sandbox Mode for Development
When developing or testing your integration with ZarinPal, you should use sandbox mode to avoid real transactions.
To enable sandbox mode:

- Use a randomly generated UUID (version 4) as your `merchant_id`.
- Set the `sandbox=True` flag when creating the `Payman` instance:

```python
from payman import Payman

pay = Payman("zarinpal", merchant_id="YOUR-MERCHANT-ID", sandbox=True)
```
This will route all requests to ZarinPal’s sandbox environment, allowing safe and isolated testing.

---

### 2. Create a Payment Request
Prepare and send a payment request to ZarinPal with the desired amount and callback URL.

```python
amount = 10000  # IRR

payment_response = pay.payment(
    amount=amount,
    callback_url="https://example.com/callback",
    description="Test Payment"
)
authority = payment_response.authority
print(f"Payment Authority: {authority}")
```

---

### 3. Redirect User to Payment URL
Use the authority code returned by the payment request to generate a URL and redirect your user there to complete the payment.

```python
payment_redirect_url = pay.get_payment_redirect_url(authority=authority)
print(payment_redirect_url)
```

---

### 4. Receive Callback

[//]: # (After payment, ZarinPal will redirect the user back to your `callback_url` with payment status parameters.)

After payment, ZarinPal will redirect the user back to your `callback_url` with payment result parameters via a `GET` request.

The two key query parameters are:

- `Authority`: A unique identifier for the payment session.
- `Status`: Indicates whether the user successfully completed the payment ("OK") or canceled/failed it ("NOK").


```python
from payman.gateways.zarinpal.models import CallbackParams

# This is a simulated example. In real use, extract these from the HTTP request:
callback = CallbackParams(authority="...", status="OK")  # CallbackParams uses alias for `Authority` and `Status`
```
Note: If you're using FastAPI, Flask, Django, or any other framework, the logic is the same — just read the Authority and Status from the query string of the incoming `GET` request.

For a better understanding, see the [FastAPI example code](https://github.com/irvaniamirali/payman/blob/main/examples/zarinpal/fastapi_integration.py)

Example callback URL:
`https://example.com/callback?Authority=A00000000000000000000000000123456789&Status=OK`

---

### 5. Verify Payment
Once the user is redirected back to your app, use the received `authority` code to verify the payment with ZarinPal.

```python
verify_response = pay.verify(authority=authority, amount=amount)

ref_id = verify_response.ref_id
print(f"Ref ID: {ref_id}")
```

---

> NOTE: **Payman supports both sync and async code.**
> All gateway methods like `payment()` and `verify()` can be called with or without `await`, depending on your application's architecture.


## Flexible Input Support

All `Payman` methods such as `payment(...)` and `verify(...)` accept input in **three flexible formats**:

- ✅ Pydantic model  
- ✅ Plain dictionary  
- ✅ Keyword arguments (`kwargs`)

This allows you to choose the most convenient style for your use case.

### Example: `payment(...)` in all supported formats

```python
from payman import Payman
from payman.gateways.zarinpal.models import PaymentRequest

pay = Payman("zarinpal", merchant_id="...")

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

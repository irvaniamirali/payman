# Using ZarinPal Gateway with Payman
This section guides you on how to integrate the [ZarinPal](https://www.zarinpal.com/) payment gateway using the Payman Python package.
You will find examples for both asynchronous and synchronous usage to fit different application needs.

## Quick Start Guide for ZarinPal Integration
Follow these simple steps to integrate ZarinPal payment gateway with Payman:

### 1. Initialize the Gateway
Import `ZarinPal` and create an instance with your merchant ID:

```python
from payman import ZarinPal

pay = ZarinPal(merchant_id="YOUR-MERCHANT-ID")
```

#### Note: Sandbox Mode for Development
When developing or testing your integration with ZarinPal, you should use sandbox mode to avoid real transactions.
To enable sandbox mode:

- Use a randomly generated UUID (version 4) as your `merchant_id`.
- Set the `sandbox=True` flag when creating the `ZarinPal` instance:

```python
from uuid import uuid4
from payman import ZarinPal

pay = ZarinPal(merchant_id=str(uuid4()), sandbox=True)
```
This will route all requests to ZarinPal’s sandbox environment, allowing safe and isolated testing.

---

### 2. Create a Payment Request
Prepare and send a payment request to ZarinPal with the desired amount and callback URL.

```python
from payman.gateways.zarinpal.models import PaymentRequest

amount = 10000  # IRR

payment_response = pay.payment(
    PaymentRequest(
        amount=amount,
        callback_url="https://example.com/callback",
        description="Test Payment"
    )
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

- `authority`: A unique identifier for the payment session.
- `status`: Indicates whether the user successfully completed the payment ("OK") or canceled/failed it ("NOK").


```python
from payman.gateways.zarinpal.models import CallbackParams

# This is a simulated example. In real use, extract these from the HTTP request:
callback = CallbackParams(authority="...", status="OK")
```
Note: If you're using FastAPI, Flask, Django, or any other framework, the logic is the same — just read the Authority and Status from the query string of the incoming `GET` request.

For a better understanding, see the [FastAPI example code](https://github.com/irvaniamirali/payman/blob/main/examples/zarinpal/fastapi_integration.py)

Example callback URL:
`https://example.com/callback?Authority=A00000000000000000000000000123456789&Status=OK`

---

### 5. Verify Payment
Once the user is redirected back to your app, use the received `authority` code to verify the payment with ZarinPal.

```python
from payman.gateways.zarinpal.models import VerifyRequest

verify_response = pay.verify(
    VerifyRequest(authority=authority, amount=amount)
)
ref_id = verify_response.ref_id
print(f"Ref ID: {ref_id}")
```

---

> NOTE: **Payman supports both sync and async code.**
> All gateway methods like `payment()` and `verify()` can be called with or without `await`, depending on your application's architecture.

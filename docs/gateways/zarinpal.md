# ZarinPal Payment Gateway Documentation

### Overview

ZarinPal provides a secure web payment gateway service for online stores. This document outlines the payment process, key parameters, API methods, and security requirements.

### [Official ZarinPal documents](https://www.zarinpal.com/docs/)

### Key Terms

- Merchant: The entity selling products/services online.
- Buyer: Cardholder purchasing from the merchant.
- Transaction: A financial operation representing an online purchase.

### 1. Creating a Payment Request
Creates a payment request by calling ZarinPal's API via the payman package. If successful, it returns the authority code needed to redirect the user to the payment gateway. Optional metadata like mobile, email, and order ID can be attached to the payment.

```python
from payman import Payman
from payman.gateways.zarinpal import ZarinPal
from payman.gateways.zarinpal.models import Payment, PaymentResponse

# Your merchant ID provided by ZarinPal
MERCHANT_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Initialize the Payman client
zarinpal = ZarinPal(merchant_id=MERCHANT_ID, sandbox=False)  # Use sandbox=True for testing

pay = Payman(gateway=zarinpal)

amount = 1000

# Send a payment request to ZarinPal
response: PaymentResponse = pay.create_payment(
    Payment(
        amount=amount,
        callback_url="https://your-site.com/verify",
        description="Test transaction",
        mobile="09121234567",
        email="test@example.com",
        order_id="12345"
    )
)

# Check the response code
if response.code == 100:
    authority = response.authority
    print(f"Payment request successful, authority: {authority}")
else:
    print(f"Payment request failed: {response.message} (code {response.code})")
```

### 2. Redirecting the User to ZarinPal Payment Page
Using the authority code from the payment request, generate the URL that the buyer must be redirected to in order to complete the payment on ZarinPal's platform.
```python
payment_url = pay.generate_payment_url(authority)
print(f"Redirect the buyer to: {payment_url}")
# In a web framework (e.g. Flask, FastAPI), use a redirect response:
# return redirect(payment_url)
```

### 3. Verifying the Payment
After the user completes or cancels the payment, you verify the payment status with ZarinPal by sending back the authority and amount. Different response codes indicate success, already-verified status, or failure.
```python
from payman.gateways.zarinpal.models import PaymentVerify, VerifyPaymentResponse

# Verify the payment by sending authority and amount back to ZarinPal
response: VerifyPaymentResponse = pay.verify_payment(
    PaymentVerify(
        authority=authority, 
        amount=amount
    )
)

code = response.code

if code == 100:
    print(f"Payment successful. Ref ID: {response.ref_id}")
    # Save transaction info to your database, update order status etc.
elif code == 101:
    print("Payment already verified.")
else:
    print(f"Payment verification failed with code {code}.")
```

### Important Notes

- Use sandbox=True in development/testing environments to avoid real transactions.
- The amount during verification must exactly match the requested amount.


### Technical Info & Parameters

| Parameter      | Type         | Description                                               |
| -------------- | ------------ | --------------------------------------------------------- |
| `merchant_id`  | `String(36)` | Unique merchant identifier from ZarinPal.                 |
| `IP`           | `String`     | Merchant server's main IP, registered with ZarinPal.      |
| `authority`    | `String(36)` | Unique purchase request ID (UUID starting with `"A"`).    |
| `code`         | `Integer`    | Transaction status code returned by ZarinPal.             |
| `ref_id`       | `Integer`    | Unique transaction ID generated after successful payment. |
| `description`  | `String`     | Short description of the product or service.              |
| `mobile`       | `String`     | Buyer’s phone number *(optional)*.                        |
| `email`        | `String`     | Buyer’s email address *(optional)*.                       |
| `callback_url` | `String`     | URL the buyer is redirected to after payment process.     |


## Common Error Codes

| Code    | English Message                 | Meaning                                    |
|---------|---------------------------------|--------------------------------------------|
| -9      | Validation error                | Missing or invalid required fields         |
| -2      | Callback URL missing            | `callback_url` not provided                |
| -3      | Description missing or too long | `description` missing or exceeds 500 chars |
| -4      | Amount out of valid range       | Invalid transaction amount                 |
| -10     | Invalid merchant_id or IP       | Incorrect merchant ID or IP address        |
| -11     | Merchant inactive               | Merchant account not active                |
| -12     | Too many attempts               | Too many requests in a short time          |
| -15     | Merchant suspended              | Merchant account suspended                 |
| -16/-17 | Merchant level insufficient     | Merchant account level too low             |
| -18     | Referrer domain mismatch        | Merchant domain mismatch                   |
| -19     | Transactions banned             | Merchant cannot create transactions        |
| 100     | Success                         | Operation succeeded                        |
| -50     | Amount mismatch in verify       | Payment amount mismatch                    |
| -51     | Payment unsuccessful            | Payment failed                             |
| -54     | Invalid authority               | Authority code invalid                     |
| 101     | Verified                        | Transaction already verified               |
For a full list, consult ZarinPal official docs.

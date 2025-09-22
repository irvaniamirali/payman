# Using Zibal Gateway with Payman

This comprehensive guide shows you how to integrate the [Zibal](https://zibal.ir/) payment gateway using the Payman Python package. You'll find examples for asynchronous usage to suit various application types.

---

## Quick Start Guide

Follow these simple steps to integrate Zibal payment gateway with Payman:

### 1. Initialize the Gateway

Import `Payman` and create an instance with your merchant ID:

```python
from payman import Payman

# Production mode
pay = Payman("zibal", merchant_id="YOUR-MERCHANT-ID")

# Test/sandbox mode
pay = Payman("zibal", merchant_id="zibal")
```

#### Test Mode for Development

Zibal provides a test mode that allows you to safely test payment flows without real transactions. To use Zibal in test mode, set your `merchant_id` to the string "zibal":

```python
from payman import Payman

pay = Payman("zibal", merchant_id="zibal")
```

This will trigger mock responses from Zibal, allowing you to fully test your integration in a safe, non-production environment.

### 2. Create a Payment Request

Prepare and send a payment request to Zibal with the desired amount and callback URL:

```python
response = await pay.initiate_payment(
    amount=10_000,  # Amount in IRR
    callback_url="https://example.com/callback",
    description="Test Payment",
    order_id="order-123"
)

if response.success:
    track_id = response.track_id
    print(f"Track ID: {track_id}")
else:
    print(f"Payment creation failed: {response.message}")
```

### 3. Redirect User to Payment URL

Use the `track_id` returned from the payment request to generate the redirect URL:

```python
if response.success:
    payment_redirect_url = pay.get_payment_redirect_url(response.track_id)
    print(f"Redirect user to: {payment_redirect_url}")
    # In a web application, redirect the user to this URL
```

### 4. Handle the Callback

After the payment process, Zibal will redirect the user back to your `callback_url` with payment result parameters via a `GET` request.

The key query parameters are:
- `trackId`: A unique identifier for the transaction
- `success`: 1 if the transaction was successful, 0 otherwise
- `status`: Payment status code
- `orderId`: Your order identifier

#### FastAPI Callback Handler

```python
from fastapi import FastAPI, Query
from payman import Payman

app = FastAPI()
pay = Payman("zibal", merchant_id="your-merchant-id")

@app.get("/callback")
async def handle_callback(
    trackId: int = Query(..., alias="trackId"),
    success: int = Query(..., alias="success"),
    status: int = Query(..., alias="status"),
    orderId: str = Query(..., alias="orderId")
):
    if success == 1:
        # Payment was successful, verify it
        verify_response = await pay.verify_payment(track_id=trackId)
        if verify_response.success:
            return {"message": "Payment successful", "ref": verify_response.ref_number}
    
    return {"message": "Payment failed or cancelled"}
```

### 5. Verify Payment

Once the user is redirected back, use the `track_id` to verify the payment with Zibal:

```python
# Async verification
verify_response = await pay.verify_payment(track_id=track_id)

if verify_response.success:
    ref_number = verify_response.ref_number
    print(f"Bank Ref Number: {ref_number}")
    print(f"Paid Amount: {verify_response.amount}")
    print(f"Paid At: {verify_response.paid_at}")
else:
    print(f"Verification failed: {verify_response.message}")
```

---

## Complete Example

Here's a complete working example:

```python
import asyncio
from payman import Payman, GatewayError

async def complete_payment_flow():
    # Initialize gateway
    pay = Payman("zibal", merchant_id="zibal")  # Sandbox mode
    
    try:
        # Step 1: Create payment
        response = await pay.initiate_payment(
            amount=25_000,
            callback_url="https://your-site.com/callback",
            description="Order #123",
            order_id="order-123",
            mobile="09123456789"
        )
        
        if not response.success:
            print(f"Payment creation failed: {response.message}")
            return
        
        print(f"Payment created successfully. Track ID: {response.track_id}")
        
        # Step 2: Get redirect URL
        payment_url = pay.get_payment_redirect_url(response.track_id)
        print(f"Redirect user to: {payment_url}")
        
        # Step 3: Simulate user payment (in real app, user goes to payment_url)
        print("User completes payment...")
        
        # Step 4: Verify payment
        verify_response = await pay.verify_payment(track_id=response.track_id)
        
        if verify_response.success:
            print(f"Payment verified! Ref: {verify_response.ref_number}")
            print(f"Amount: {verify_response.amount} IRR")
            print(f"Paid at: {verify_response.paid_at}")
        else:
            print(f"Verification failed: {verify_response.message}")
            
    except GatewayError as e:
        print(f"Gateway error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run the example
asyncio.run(complete_payment_flow())
```

---

## Payment Flow Summary

| Step | Description | Method | Response |
|------|-------------|--------|----------|
| 1. Init | Create Payman instance | `Payman("zibal", merchant_id="...")` | Gateway instance |
| 2. Payment | Send payment request | `initiate_payment(...)` | `PaymentResponse` with `track_id` |
| 3. Redirect | Get payment URL | `get_payment_redirect_url(track_id)` | Payment page URL |
| 4. Callback | Handle user return | Extract params from request | Callback parameters |
| 5. Verify | Confirm payment | `verify_payment(track_id)` | `VerifyResponse` with details |

---

## Flexible Input Support

All Payman methods accept input in **three flexible formats**:

### 1. Pydantic Models

```python
from zibal.models import PaymentRequest, VerifyRequest

# Payment request
request = PaymentRequest(
    amount=10_000,
    callback_url="https://site.com/callback",
    description="Test Payment",
    order_id="order-123"
)
response = await pay.initiate_payment(request)

# Verify request
verify_request = VerifyRequest(track_id=123456)
verify_response = await pay.verify_payment(verify_request)
```

### 2. Dictionary Input

```python
# Payment request
request_data = {
    "amount": 10_000,
    "callback_url": "https://site.com/callback",
    "description": "Test Payment"
}
response = await pay.initiate_payment(request_data)

# Verify request
verify_data = {"track_id": 123456}
verify_response = await pay.verify_payment(verify_data)
```

### 3. Keyword Arguments

```python
# Payment request
response = await pay.initiate_payment(
    amount=10_000,
    callback_url="https://site.com/callback",
    description="Test Payment"
)

# Verify request
verify_response = await pay.verify_payment(track_id=123456)
```

## Input Validation

All inputs are strictly validated using Pydantic, regardless of the input format:

- **Field types** are enforced (e.g., amount must be an int)
- **Required fields** are checked
- **Invalid values** raise immediate validation errors
- **Clear error messages** help with debugging

### Validation Example

```python
from pydantic import ValidationError

try:
    response = await pay.initiate_payment(
        amount="invalid",  # ❌ This will raise ValidationError
        callback_url="https://your-site.com",
        description="Example"
    )
except ValidationError as e:
    print("Validation error:", e)
```

## Error Handling

Payman provides comprehensive error handling for different scenarios:

```python
from payman import GatewayError
from zibal.exceptions import PaymentNotSuccessfulError, InvalidTrackIdError

try:
    response = await pay.initiate_payment(...)
except PaymentNotSuccessfulError as e:
    print(f"Payment failed: {e.message}")
except InvalidTrackIdError as e:
    print(f"Invalid track ID: {e.message}")
except GatewayError as e:
    print(f"Gateway error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Advanced Features

### Custom HTTP Configuration

```python
from payman import Payman

# Configure HTTP client with custom settings
pay = Payman(
    "zibal", 
    merchant_id="your-merchant-id",
    timeout=30.0,
    max_retries=3,
    retry_delay=1.0
)
```

### Logging Configuration

```python
import logging

# Configure logging for Payman
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("payman")

# Payman will automatically use the configured logger
```

## Testing

### Sandbox Mode

Always test your integration using sandbox mode:

```python
# Use sandbox mode for testing
pay = Payman("zibal", merchant_id="zibal")

# This will use mock responses
response = await pay.initiate_payment(
    amount=10_000,
    callback_url="https://your-site.com/callback"
)
```

## Best Practices

1. **Always use HTTPS** for callback URLs in production
2. **Validate amounts** before sending to the gateway
3. **Store track_id** securely for verification
4. **Handle all exceptions** gracefully
5. **Use environment variables** for sensitive data
6. **Test thoroughly** in sandbox mode before going live
7. **Implement proper logging** for debugging and monitoring
8. **Verify payments** on your server, not just the client
9. **Use unique order_id** for each transaction
10. **Implement idempotency** for payment operations

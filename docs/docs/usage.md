# Usage Guide

This comprehensive guide will help you understand how to use Payman in your project and integrate with specific payment gateways.

---

## Supported Gateways

Each gateway comes with its own detailed usage guide and example code:

- **[Zibal](./gateways/zibal/usage.md)** - Complete integration with all features
- **[Zarinpal](gateways/zarinpal/usage.md)** - Coming soon

---

## Common Payment Workflow

Regardless of the gateway, the typical payment flow follows these steps:

1. **Initialize Gateway** - Create a Payman instance with your credentials
2. **Create Payment Request** - Send payment details to the gateway
3. **Redirect User** - Send user to the payment page
4. **Handle Callback** - Process the return from the payment gateway
5. **Verify Payment** - Confirm the transaction was successful

Payman standardizes this flow across all gateways, making it easy to switch between providers.

## Basic Usage Patterns

### 1. Gateway Initialization

```python
from payman import Payman

# Initialize Zibal gateway
pay = Payman("zibal", merchant_id="your-merchant-id")

# For testing, use sandbox mode
pay = Payman("zibal", merchant_id="zibal")  # Sandbox mode
```

### 2. Payment Creation

```python
response = await pay.initiate_payment(
    amount=10_000,
    callback_url="https://your-site.com/callback",
    description="Order #123",
    order_id="order-123"
)
```

### 3. User Redirection

```python
if response.success:
    payment_url = pay.get_payment_redirect_url(response.track_id)
    # Redirect user to payment_url
    print(f"Redirect user to: {payment_url}")
```

### 4. Payment Verification

```python
# After user returns from payment gateway
verify_response = await pay.verify_payment(track_id=response.track_id)

if verify_response.success:
    print(f"Payment successful! Ref: {verify_response.ref_number}")
else:
    print(f"Payment failed: {verify_response.message}")
```

## Input Flexibility

Payman supports multiple input formats for maximum flexibility:

### Pydantic Models
```python
from zibal.models import PaymentRequest

request = PaymentRequest(
    amount=10_000,
    callback_url="https://site.com/callback",
    description="Test payment"
)
response = await pay.initiate_payment(request)
```

### Dictionary Input
```python
request_data = {
    "amount": 10_000,
    "callback_url": "https://site.com/callback",
    "description": "Test payment"
}
response = await pay.initiate_payment(request_data)
```

### Keyword Arguments
```python
response = await pay.initiate_payment(
    amount=10_000,
    callback_url="https://site.com/callback",
    description="Test payment"
)
```

## Error Handling

Payman provides comprehensive error handling:

```python
from payman import GatewayError
from zibal.exceptions import PaymentNotSuccessfulError

try:
    response = await pay.initiate_payment(...)
except GatewayError as e:
    print(f"Gateway error: {e}")
except PaymentNotSuccessfulError as e:
    print(f"Payment failed: {e.message}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Advanced Features

### Custom HTTP Client Configuration

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

For testing, use sandbox mode:

```python
# Zibal sandbox mode
pay = Payman("zibal", merchant_id="zibal")

# This will use mock responses for testing
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

## Next Steps

- Explore [Zibal Integration](./gateways/zibal/usage.md) for detailed Zibal-specific features
- Check the [API Reference](./api.md) for complete method documentation
- Review [examples](https://github.com/irvaniamirali/payman/tree/main/examples) for real-world implementation patterns

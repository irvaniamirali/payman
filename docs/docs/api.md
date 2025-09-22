# Payman API Reference

Welcome to the **Payman API** documentation. This section provides comprehensive documentation for the unified interface for interacting with multiple Iranian payment gateways.

---

## Gateway-Specific Documentation

Each gateway has its own detailed API documentation:

- **[Zibal API](./gateways/zibal/api.md)** - Complete Zibal integration reference
- **[Zarinpal API](./gateways/zarinpal/api.md)** - Coming soon

---

## Core API Overview

Payman provides a consistent and developer-friendly API for initiating, verifying, and managing payments across all supported gateways. All gateways follow the same public interface and support **asynchronous** usage.

## Main Classes and Functions

### `Payman` Factory Function

The main entry point for creating gateway instances.

```python
from payman import Payman

# Create a gateway instance
gateway = Payman("zibal", merchant_id="your-merchant-id")
```

**Parameters:**
- `name` (str): Gateway name ("zibal", "zarinpal", etc.)
- `merchant_id` (str): Your merchant ID for the gateway
- `**kwargs`: Additional gateway-specific parameters

**Returns:**
- Gateway instance implementing `GatewayInterface`

### `GatewayInterface`

Abstract base class that all payment gateways implement.

```python
from payman.interfaces.gateway_base import GatewayInterface
```

**Methods:**
- `initiate_payment(request, **kwargs)` - Create a new payment
- `verify_payment(request, **kwargs)` - Verify a payment
- `get_payment_redirect_url(token)` - Get payment page URL

## Core Exceptions

### `GatewayError`

Base exception for all gateway-related errors.

```python
from payman import GatewayError

try:
    response = await gateway.initiate_payment(...)
except GatewayError as e:
    print(f"Gateway error: {e}")
```

### HTTP Exceptions

```python
from payman.core.exceptions.http import (
    HttpClientError,
    HttpStatusError,
    TimeoutError,
    InvalidJsonError
)
```

## Utility Functions

### `to_model_instance`

Convert various input types to Pydantic model instances.

```python
from payman.utils import to_model_instance
from zibal.models import PaymentRequest

# Convert dict to model
data = {"amount": 1000, "callback_url": "https://example.com"}
request = to_model_instance(data, PaymentRequest)

# Convert with overrides
request = to_model_instance(None, PaymentRequest, amount=1000, callback_url="https://example.com")
```

## Gateway Registration

### `register_gateway`

Register a new payment gateway dynamically.

```python
from payman.core.gateways.register_gateway import register_gateway

# Register a custom gateway
register_gateway("mygateway", "mypackage.gateway.MyGateway")
```

### `get_gateway_instance`

Get a gateway instance by name.

```python
from payman.core.gateways.register_gateway import get_gateway_instance

gateway = get_gateway_instance("zibal", merchant_id="your-id")
```

## HTTP Client

### `AsyncHttpClient`

Asynchronous HTTP client with retry, logging, and session management.

```python
from payman.core.http.client import AsyncHttpClient

client = AsyncHttpClient(
    base_url="https://api.example.com",
    timeout=10.0,
    max_retries=3,
    retry_delay=1.0
)

async with client:
    response = await client.request("POST", "/payments", json_data={"amount": 1000})
```

**Parameters:**
- `base_url` (str, optional): Base URL for requests
- `timeout` (float): Request timeout in seconds (default: 10.0)
- `slow_request_threshold` (float): Threshold for slow request warnings (default: 3.0)
- `max_retries` (int): Maximum retry attempts (default: 0)
- `retry_delay` (float): Delay between retries in seconds (default: 1.0)
- `log_level` (int): Logging level (default: 20)
- `log_req_body` (bool): Log request bodies (default: True)
- `log_resp_body` (bool): Log response bodies (default: True)

## Type Hints and Models

Payman uses Pydantic models for type safety and validation. All request and response models are fully typed and validated.

### Example with Type Hints

```python
from typing import Optional
from payman import Payman
from zibal.models import PaymentRequest, PaymentResponse

async def process_payment(
    amount: int,
    callback_url: str,
    description: Optional[str] = None
) -> PaymentResponse:
    gateway = Payman("zibal", merchant_id="your-id")
    
    request = PaymentRequest(
        amount=amount,
        callback_url=callback_url,
        description=description
    )
    
    return await gateway.initiate_payment(request)
```

## Error Handling Patterns

### Basic Error Handling

```python
from payman import GatewayError
from zibal.exceptions import PaymentNotSuccessfulError

try:
    response = await gateway.initiate_payment(...)
except PaymentNotSuccessfulError as e:
    # Handle payment-specific errors
    print(f"Payment failed: {e.message}")
except GatewayError as e:
    # Handle general gateway errors
    print(f"Gateway error: {e}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
```

### Advanced Error Handling

```python
from payman.core.exceptions.http import HttpStatusError, TimeoutError

try:
    response = await gateway.initiate_payment(...)
except HttpStatusError as e:
    print(f"HTTP error {e.status_code}: {e.message}")
    if e.body:
        print(f"Response body: {e.body}")
except TimeoutError as e:
    print(f"Request timed out: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration and Environment

### Environment Variables

```python
import os
from payman import Payman

# Use environment variables for sensitive data
merchant_id = os.getenv("ZIBAL_MERCHANT_ID")
gateway = Payman("zibal", merchant_id=merchant_id)
```

## Testing Utilities

### Mock Gateway for Testing

```python
from unittest.mock import AsyncMock
from payman import Payman

def create_mock_gateway():
    gateway = Payman("zibal", merchant_id="test")
    gateway.initiate_payment = AsyncMock(return_value=MockResponse(success=True))
    gateway.verify_payment = AsyncMock(return_value=MockVerifyResponse(success=True))
    return gateway
```

### Test Configuration

```python
import pytest
from payman import Payman

@pytest.fixture
def test_gateway():
    return Payman("zibal", merchant_id="zibal")  # Sandbox mode

async def test_payment_flow(test_gateway):
    response = await test_gateway.initiate_payment(
        amount=1000,
        callback_url="https://example.com/callback"
    )
    assert response.success
```

## Performance Considerations

### Connection Pooling

The HTTP client automatically manages connection pooling for better performance:

```python
# Client reuses connections automatically
gateway = Payman("zibal", merchant_id="your-id")

# Multiple requests will reuse the same connection
for i in range(10):
    response = await gateway.initiate_payment(...)
```

### Async Context Management

Always use async context managers for proper resource cleanup:

```python
async with gateway:
    response = await gateway.initiate_payment(...)
# Client is automatically closed
```

## Migration Guide

### From v2 to v3

```python
# Old v2 syntax
from payman import Payman
from payman.gateways.zibal.models import RequestPayment
gateway = Payman("zibal", merchant_id="your-id")
response = await gateway.payment(RequestPayment(...))

# New v3 syntax
from payman import Payman
from zibal.models import PaymentRequest  # provided by `pip install payman[zibal]`
gateway = Payman("zibal", merchant_id="your-id")
response = await gateway.initiate_payment(RequestPayment(...))
```

## Contributing

To contribute new gateways or features:

1. Implement the `GatewayInterface`
2. Register your gateway using `register_gateway`
3. Add comprehensive tests
4. Update documentation

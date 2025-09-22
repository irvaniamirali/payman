# Zibal API Reference

This page documents the available methods and data models for the **Zibal** payment gateway integration using the **Payman** package. It includes detailed parameter tables, response models, and exception mappings.

---

## Gateway Instantiation

### Using Payman Factory (Recommended)

The recommended way to create a Zibal gateway instance:

```python
from payman import Payman

# Production mode
pay = Payman("zibal", merchant_id="your-merchant-id")

# Sandbox mode for testing
pay = Payman("zibal", merchant_id="zibal")
```

### Direct Instantiation

You can also instantiate the Zibal gateway directly (though not recommended for consistency):

```python
from zibal import Zibal

pay = Zibal(merchant_id="your-merchant-id")
```

---

## Core Methods

### `initiate_payment(request: PaymentRequest | dict | None = None, **kwargs) -> PaymentResponse`

Initiates a new payment request to Zibal.

#### Parameters

**`request`** (`PaymentRequest` | `dict` | `None`)

| Field                    | Type                                                                  | Required | Description                                         |
| ------------------------ | --------------------------------------------------------------------- | -------- | --------------------------------------------------- |
| `amount`                 | `int` (≥ 100)                                                         | ✅        | Payment amount in Rial (minimum: 100)               |
| `callback_url`           | `HttpUrl`                                                             | ✅        | URL to redirect the user after payment              |
| `description`            | `str \| None`                                                         | ❌        | Optional payment description                        |
| `order_id`               | `str \| None`                                                         | ❌        | Optional merchant order identifier                  |
| `mobile`                 | `constr(min_length=11, max_length=11, pattern="^09\d{9}$") \| None`   | ❌        | Optional buyer mobile number                        |
| `allowed_cards`          | `List[constr(min_length=16, max_length=16, pattern="^\d{16}$")]\| None` | ❌        | Optional list of allowed card PANs                  |
| `ledger_id`              | `str \| None`                                                         | ❌        | Optional ledger identifier                          |
| `national_code`          | `constr(min_length=10, max_length=10, pattern="^\d{10}$") \| None`    | ❌        | Optional national code of the buyer                 |
| `check_mobile_with_card` | `bool \| None`                                                        | ❌        | Optional mobile/card cross-check flag               |
| `percent_mode`           | `Literal[0,1]` (default: `0`)                                         | ❌        | Revenue-sharing mode: 0=fixed, 1=percent            |
| `fee_mode`               | `Literal[0,1,2]` (default: `0`)                                       | ❌        | Fee payer mode: 0=shopper, 1=merchant, 2=split      |
| `multiplexingInfos`      | `List[MultiplexingInfo]` (default: `[]`)                              | ❌        | Optional multiplexing (split payment) configuration |

#### Returns

**`PaymentResponse`**

| Field      | Type            | Description                                 |
| ---------- | --------------- | ------------------------------------------- |
| `success`  | `bool`          | Whether the payment request was successful  |
| `track_id` | `int`           | Unique transaction tracking ID              |
| `message`  | `str`           | Human-readable result message               |
| `status`   | `int`           | Response status code                        |

#### Example Usage

```python
# Using keyword arguments
response = await pay.initiate_payment(
    amount=10_000,
    callback_url="https://example.com/callback",
    description="Test Payment",
    order_id="order-123"
)

# Using Pydantic model
from zibal.models import PaymentRequest

request = PaymentRequest(
    amount=10_000,
    callback_url="https://example.com/callback",
    description="Test Payment"
)
response = await pay.initiate_payment(request)

# Using dictionary
request_data = {
    "amount": 10_000,
    "callback_url": "https://example.com/callback",
    "description": "Test Payment"
}
response = await pay.initiate_payment(request_data)
```

#### Raises

* `GatewayError` - Base gateway error
* `ZibalError` - Zibal-specific errors and subclasses

---

### `verify_payment(request: VerifyRequest | dict | None = None, **kwargs) -> VerifyResponse`

Verifies payment after user redirect or callback.

#### Parameters

**`request`** (`VerifyRequest` | `dict` | `None`)

| Field      | Type  | Required | Description                               |
| ---------- | ----- | -------- | ----------------------------------------- |
| `track_id` | `int` | ✅        | Transaction tracking ID returned by Zibal |

#### Returns

**`VerifyResponse`**

| Field               | Type                    | Description                                    |
| ------------------- | ----------------------- | ---------------------------------------------- |
| `success`           | `bool`                  | Whether verification was successful             |
| `result`            | `int`                   | Response status code (100 = success)           |
| `message`           | `str`                   | Result message                                 |
| `amount`            | `int \| None`           | Paid amount in Rial                            |
| `status`            | `int \| None`           | Bank transaction status (1=success,2=canceled) |
| `paid_at`           | `str \| None`           | ISO 8601 payment timestamp                     |
| `card_number`       | `str \| None`           | Masked payer card number                       |
| `ref_number`        | `str \| None`           | Bank reference number                          |
| `order_id`          | `str \| None`           | Merchant order ID                              |
| `description`       | `str \| None`           | Additional description                         |
| `track_id`          | `int \| None`           | Tracking ID                                    |
| `multiplexingInfos` | `List[MultiplexingInfo]` | Optional split payment details                 |

#### Example Usage

```python
# Using keyword arguments
verify_response = await pay.verify_payment(track_id=123456)

# Using Pydantic model
from zibal.models import VerifyRequest

verify_request = VerifyRequest(track_id=123456)
verify_response = await pay.verify_payment(verify_request)

# Check if verification was successful
if verify_response.success:
    print(f"Payment verified! Ref: {verify_response.ref_number}")
    print(f"Amount: {verify_response.amount} IRR")
else:
    print(f"Verification failed: {verify_response.message}")
```

#### Raises

* `GatewayError` - Base gateway error
* `PaymentNotSuccessfulError` - Payment was not successful
* `InvalidTrackIdError` - Invalid track ID provided

---

### `get_payment_redirect_url(track_id: int) -> str`

Builds the URL for redirecting the user to Zibal's payment page.

#### Parameters

* `track_id` (`int`): Tracking ID from `initiate_payment()`

#### Returns

* `str`: Complete redirect URL

#### Example

```python
track_id = 123456
payment_url = pay.get_payment_redirect_url(track_id)
print(payment_url)  # https://gateway.zibal.ir/start/123456
```

---

## Advanced Methods

### `inquiry(request: InquiryRequest | dict | None = None, **kwargs) -> InquiryResponse`

Fetches current transaction status without verification.

#### Parameters

**`request`** (`InquiryRequest` | `dict` | `None`)

| Field      | Type  | Required | Description             |
| ---------- | ----- | -------- | ----------------------- |
| `track_id` | `int` | ✅        | Transaction tracking ID |

#### Returns

**`InquiryResponse`**

| Field               | Type                    | Description                    |
| ------------------- | ----------------------- | ------------------------------ |
| `result`            | `int`                   | Response status code           |
| `message`           | `str`                   | Status message                 |
| `ref_number`        | `int \| None`           | Bank reference number          |
| `paid_at`           | `str \| None`           | Payment timestamp (ISO 8601)   |
| `verified_at`       | `str \| None`           | Verification timestamp         |
| `status`            | `int`                   | Payment status                 |
| `amount`            | `int`                   | Amount of transaction          |
| `order_id`          | `str`                   | Merchant order ID              |
| `description`       | `str`                   | Transaction description        |
| `card_number`       | `str \| None`           | Masked card number             |
| `wage`              | `int`                   | Associated wage                |
| `created_at`        | `str`                   | Transaction creation timestamp |
| `multiplexingInfos` | `List[MultiplexingInfo]` | Revenue sharing details        |

---

## Data Models

### `PaymentRequest`

Request model for initiating payments.

```python
from zibal.models import PaymentRequest

request = PaymentRequest(
    amount=10_000,
    callback_url="https://example.com/callback",
    description="Test Payment",
    order_id="order-123",
    mobile="09123456789"
)
```

### `PaymentResponse`

Response model for payment initiation.

```python
from zibal.models import PaymentResponse

# Response fields
response.success  # bool
response.track_id  # int
response.message  # str
response.status  # int
```

### `VerifyRequest`

Request model for payment verification.

```python
from zibal.models import VerifyRequest

request = VerifyRequest(track_id=123456)
```

### `VerifyResponse`

Response model for payment verification.

```python
from zibal.models import VerifyResponse

# Response fields
response.success  # bool
response.result  # int
response.message  # str
response.amount  # int | None
response.ref_number  # str | None
response.paid_at  # str | None
# ... and more
```

### `CallbackParams`

Model for handling callback parameters.

```python
from zibal.models import CallbackParams

# From query parameters
callback = CallbackParams(
    track_id=123456,
    success=1,
    status=100,
    order_id="order-123"
)

if callback.is_success:
    print("Payment was successful")
```

---

## Exception Handling

All Zibal-specific errors inherit from `ZibalError`. The gateway automatically raises the proper subclass based on the status code.

### Error Hierarchy

```
GatewayError (base)
└── ZibalError
    ├── MerchantNotFoundError
    ├── MerchantInactiveError
    ├── InvalidMerchantError
    ├── AmountTooLowError
    ├── InvalidCallbackUrlError
    ├── InvalidPercentModeError
    ├── InvalidMultiplexingBeneficiariesError
    ├── InactiveMultiplexingBeneficiaryError
    ├── MissingSelfBeneficiaryError
    ├── AmountMismatchInMultiplexingError
    ├── InsufficientWalletBalanceForFeesError
    ├── AmountExceedsLimitError
    ├── InvalidNationalCodeError
    ├── AlreadyConfirmedError
    ├── PaymentNotSuccessfulError
    └── InvalidTrackIdError
```

### Error Handling Example

```python
from payman import GatewayError
from zibal.exceptions import (
    PaymentNotSuccessfulError,
    InvalidTrackIdError,
    AmountTooLowError
)

try:
    response = await pay.initiate_payment(
        amount=50,  # Too low
        callback_url="https://example.com/callback"
    )
except AmountTooLowError as e:
    print(f"Amount too low: {e.message}")
except PaymentNotSuccessfulError as e:
    print(f"Payment failed: {e.message}")
except InvalidTrackIdError as e:
    print(f"Invalid track ID: {e.message}")
except GatewayError as e:
    print(f"Gateway error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Sandbox Testing

### Test Mode Configuration

To use Zibal in sandbox mode, set your `merchant_id` to the string `"zibal"`:

```python
from payman import Payman

# Sandbox mode
pay = Payman("zibal", merchant_id="zibal")

# This will use mock responses for testing
response = await pay.initiate_payment(
    amount=10_000,
    callback_url="https://example.com/callback"
)
```

---

## Configuration Options

### HTTP Client Configuration

```python
from payman import Payman

# Configure HTTP client with custom settings
pay = Payman(
    "zibal", 
    merchant_id="your-merchant-id",
    timeout=30.0,           # Request timeout in seconds
    max_retries=3,          # Maximum retry attempts
    retry_delay=1.0,        # Delay between retries
    log_level=20,           # Logging level
    log_req_body=True,      # Log request bodies
    log_resp_body=True      # Log response bodies
)
```

### Environment Variables

```python
import os
from payman import Payman

# Use environment variables for configuration
merchant_id = os.getenv("ZIBAL_MERCHANT_ID", "zibal")  # Default to sandbox
pay = Payman("zibal", merchant_id=merchant_id)
```

---

## Performance Considerations

### Connection Pooling

The HTTP client automatically manages connection pooling:

```python
# Client reuses connections automatically
pay = Payman("zibal", merchant_id="your-id")

# Multiple requests will reuse the same connection
for i in range(10):
    response = await pay.initiate_payment(...)
```

### Async Context Management

Always use async context managers for proper resource cleanup:

```python
async with pay:
    response = await pay.initiate_payment(...)
# Client is automatically closed
```

---

## Migration from v2

If you're migrating from Payman v2:

```python
# Old v2 syntax
from payman import Zibal
gateway = Zibal(merchant_id="your-id")
response = await gateway.payment(...)

# New v3 syntax
from payman import Payman
gateway = Payman("zibal", merchant_id="your-id")
response = await gateway.initiate_payment(...)
```

---

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'zibal'**
   - Make sure you have the zibal package installed
   - Check your Python environment

2. **ValidationError on payment creation**
   - Verify all required fields are provided
   - Check field types and formats

3. **GatewayError during verification**
   - Ensure track_id is valid and not expired
   - Check if payment was actually completed

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("payman")

# Your payment code here
```

---

## Support

For additional help:

- Check the [Usage Guide](../../usage.md) for integration examples
- Review [Error Handling Patterns](../../api.md#error-handling-patterns)
- See [Real-world Examples](../../../examples/zibal/) for complete implementations
- Open an issue on [GitHub](https://github.com/irvaniamirali/payman/issues)

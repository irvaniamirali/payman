from payman.gateways.zarinpal import PaymentRequest

# ZarinPal API Reference

This page documents the public API for the `ZarinPal` gateway class in the **Payman** package.

ZarinPal supports both **synchronous** and **asynchronous** usage. All methods behave the same regardless of the execution context.

Official API Reference: [ZarinPal Docs](https://docs.zarinpal.com/paymentGateway/)

---

## Class: `ZarinPal`

```python
from payman import ZarinPal
```

### Constructor

```python
ZarinPal(merchant_id: str, version: int = 4, sandbox: bool = False, **client_options)
```

#### Parameters:

* `merchant_id` (str): Your ZarinPal merchant ID (UUID).
* `version` (int): API version (default: 4).
* `sandbox` (bool): Use sandbox environment if `True`.
* `client_options`: Optional keyword arguments passed to the internal HTTP client.

## **Methods**

---

### `payment(request: PaymentRequest) -> PaymentResponse`

Initiates a new payment transaction request.

---

#### Parameters:
**`request`** (`PaymentRequest`) - Contains payment details.

| Field          | Type                           | Required | Description                                        |
| -------------- | ------------------------------ | ------- | -------------------------------------------------- |
| `amount`       | `int` (>= 1000)                | ✅       | Amount in IRR (minimum 1000)                       |
| `currency`     | `str` ("IRR" or "IRT")         | ❌       | Currency type (default: "IRR")                     |
| `description`  | `str`                          | ✅       | Payment description                                |
| `callback_url` | `HttpUrl | str`                 | ✅        | URL to redirect user after payment                 |
| `metadata`     | `PaymentMetadata | dict | None` | ❌        | Optional metadata (e.g., mobile, email, order_id) |
| `referrer_id`  | `str | None`                   | ❌        | Optional reseller tracking ID                      |
| `wages`        | `list[Wage]` (1 to 5 items)    | ❌       | Revenue sharing details between IBANs              |

`PaymentMetadata` — Optional metadata passed as the `metadata` field of `PaymentRequest`.
The `metadata` field in `PaymentRequest` can include optional information such as the user's mobile number, email, or internal order ID. It accepts a `PaymentMetadata` object or a compatible dictionary.

| Field      | Type                    | Description                             |
| ---------- | ----------------------- | --------------------------------------- |
| `mobile`   | `str` (regex: `^09\d{9}$`) | Mobile number of the user               |
| `email`    | `EmailStr | str | None`  | Email address of the user               |
| `order_id` | `str | None`            | Optional order ID for internal tracking |

---

#### Returns
**`PaymentResponse`** - Gateway response after processing the payment.

Returned after a successful payment request

| Field       | Type  | Description                            |
| ----------- | ----- | -------------------------------------- |
| `code`      | `int` | Result status code                     |
| `message`   | `str` | Description of the status              |
| `authority` | `str` | Unique payment session ID              |
| `fee_type`  | `str` | Entity responsible for transaction fee |
| `fee`       | `int` | Amount of fee in IRR                   |

---

#### Raises
- `PaymentGatewayError` — Base exception for gateway issues
- `ValidationError` — If request payload is invalid

---

#### Example

```python
response = gateway.payment(
    PaymentRequest(
        amount=10000,
        description="Purchase",
        callback_url="https://example.com/callback"
    )
)
```

---

#### `verify(request: VerifyRequest) -> VerifyResponse`

Verifies the result of a completed payment.

---

#### Parameters:
**`request`** (`VerifyRequest`) — Request to verify a payment session.

| Field       | Type           | Required | Description                             |
| ----------- | -------------- | -------- | --------------------------------------- |
| `amount`    | `int` (≥ 1000) | ✅        | Must match the original payment amount  |
| `authority` | `str`          | ✅        | The authority code returned by ZarinPal |

---

#### Returns
**`VerifyResponse`** — Contains transaction info and success details.

| Field       | Type                       | Description                                  |
| ----------- | -------------------------- | -------------------------------------------- |
| `code`      | `int`                      | Verification result code                     |
| `ref_id`    | `int | None`                | Unique transaction reference (if successful) |
| `card_pan`  | `str | None`               | Masked card number used for the payment      |
| `card_hash` | `str | None`               | SHA256 hash of the card number               |
| `fee_type`  | `str | None`               | Indicates who paid the transaction fee       |
| `fee`       | `int | None`               | Transaction fee in IRR                       |
| `message`   | `str | None`               | Gateway message or error detail              |
| `wages`     | `list[WageResponse] | None` | Returned if revenue sharing was used         |

---

#### Raises
- `PaymentGatewayError`
- `AlreadyVerifiedError`
- `PaymentNotCompletedError`

---

#### `get_payment_redirect_url(authority: str) -> str`

Returns the URL to redirect the user to ZarinPal's payment page.

---

#### Parameters
`authority` (`str`) — The unique authority code received from a successful payment request.

---

#### Returns
A `str` representing the full redirect URL (sandbox or production based on config).

---

#### Example
```python
url = gateway.get_payment_redirect_url(authority)
```

---

#### `reverse(request: ReverseRequest) -> ReverseResponse`

Reverse a pending or unsettled transaction.

---

#### Parameters
`request` (`ReverseRequest`) — Contains the authority code of the transaction to reverse.

| Field       | Type  | Required | Description                              |
| ----------- | ----- | -------- | ---------------------------------------- |
| `authority` | `str` | ✅        | The authority code of the target payment |

---

#### Returns
`ReverseResponse` — The result of the reverse request.

| Field     | Type  | Description                  |
| --------- | ----- | ---------------------------- |
| `code`    | `int` | Result status code           |
| `message` | `str` | Result message from ZarinPal |

---

#### Raises
- `PaymentGatewayError`
- `ReverseError`
- `ValidationError`
- `SessionError`

---

#### `get_unverified_payments() -> UnverifiedPayments`

Retrieves all successful payments that have not yet been verified (i.e. no `verify(...)` call has been made for them yet).

---

#### Parameters
None
This method does not take any parameters. It uses your configured merchant credentials to fetch unverified transactions from ZarinPal.

---

#### Returns
**`UnverifiedPayments`** — A container with metadata and a list of `UnverifiedTransaction` items.

| Field         | Type                          | Description                            |
| ------------- | ----------------------------- | -------------------------------------- |
| `code`        | `int`                         | Result status code                     |
| `message`     | `str`                         | Gateway response message               |
| `authorities` | `list[UnverifiedTransaction]` | List of unverified transaction records |


#### Related Models
- `UnverifiedTransaction`
Represents a single unverified payment session.

| Field          | Type         | Description                                   |
| -------------- | ------------ | --------------------------------------------- |
| `authority`    | `str`        | Unique authority code                         |
| `amount`       | `int`        | Payment amount in IRR                         |
| `callback_url` | `HttpUrl`    | The original callback URL for the transaction |
| `referer`      | `str | None` | Optional referer header (if available)        |
| `date`         | `datetime`   | Timestamp of the transaction                  |

---

#### Example
```python
unverified = gateway.get_unverified_payments()
for tx in unverified.authorities:
    print(tx.authority, tx.amount)
```

---

## Error Handling

All exceptions inherit from `ZarinPalError`, which is a subclass of `PaymentGatewayError`.

### Common Exceptions

```python
from payman.gateways.zarinpal.errors import *
```

* `ValidationError`
* `MerchantIDError`
* `TerminalError`
* `PaymentError`
* `SessionError`
* `AuthorityError`
* `ReverseError`
* `AlreadyVerifiedError`
* `PaymentNotCompletedError`

### Example Usage

```python
from payman.errors import PaymentGatewayError

try:
    response = pay.payment(PaymentRequest(...))
except PaymentGatewayError as e:
    print("Payment failed:", e)
```

---

## Notes

* All methods work seamlessly in both sync and async environments.
* Always use try/except blocks when dealing with external gateways.
* For practical usage, refer to: [ZarinPal Usage Guide](./usage.md)

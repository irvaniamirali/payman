# Zibal API Reference

This page documents the available methods and data models for the **Zibal** payment gateway integration using the **Payman** package. It includes detailed parameter tables and exception mappings.

---

## Instantiating a Gateway

By default, you should use the `Payman` wrapper class to work with any gateway:

```python
from payman import Payman

pay = Payman("zibal", merchant_id="...")
```
This approach allows you to switch gateways dynamically and keeps your code clean and consistent.

## Using the Zibal Gateway Directly

While it's recommended to use the generic `Payman` wrapper for consistency, 
you can also instantiate the Zibal gateway directly:

```python
from payman import Zibal

pay = Zibal(merchant_id="...")
```
This can be useful if you're working exclusively with one gateway and prefer to import it directly.


## Methods

### `payment(params: PaymentRequest | dict | None = None) -> PaymentResponse`

Initiates a new payment request to Zibal.

#### Parameters

**`params`** (`PaymentRequest`)

| Field                    | Type                                                                  | Required | Description                                         |
| ------------------------ | --------------------------------------------------------------------- | -------- | --------------------------------------------------- |
| `amount`                 | `int` (≥ 100)                                                         | ✅        | Payment amount in Rial (minimum: 100)               |
| `callback_url`           | `HttpUrl`                                                             | ✅        | URL to redirect the user after payment              |
| `description`            | `str | None`                                                         | ❌        | Optional payment description                        |
| `order_id`               | `str | None`                                                         | ❌        | Optional merchant order identifier                  |
| `mobile`                 | `constr(min_length=11, max_length=11, pattern="^09\d{9}$") \| None`   | ❌        | Optional buyer mobile number                        |
| `allowed_cards`          | `List[constr(min_length=16, max_length=16, pattern="^\d{16}$")]\| None` | ❌        | Optional list of allowed card PANs                  |
| `ledger_id`              | `str | None`                                                          | ❌        | Optional ledger identifier                          |
| `national_code`          | `constr(min_length=10, max_length=10, pattern="^\d{10}$") \| None`    | ❌        | Optional national code of the buyer                 |
| `check_mobile_with_card` | `bool | None`                                                          | ❌        | Optional mobile/card cross-check flag               |
| `percent_mode`           | `Literal[0,1]` (default: `0`)                                         | ❌        | Revenue-sharing mode: 0=fixed, 1=percent            |
| `fee_mode`               | `Literal[0,1,2]` (default: `0`)                                       | ❌        | Fee payer mode: 0=shopper, 1=merchant, 2=split      |
| `multiplexingInfos`      | `List[MultiplexingInfo]` (default: `[]`)                              | ❌        | Optional multiplexing (split payment) configuration |

#### Returns

**`PaymentResponse`**

| Field      | Type            | Description                                 |
| ---------- | --------------- | ------------------------------------------- |
| `status`   | `Status` (enum) | Payment status code (e.g., `SUCCESS`, etc.) |
| `track_id` | `int`           | Unique transaction tracking ID              |
| `message`  | `str`           | Human-readable result message               |

#### Raises

* `ZibalError` (base error) and its subclasses depending on error code

---

### `lazy_payment(params: PaymentRequest | dict | None = None) -> PaymentResponse`

Initiates a delayed-verification payment. Identical signature and models to `payment()`.

---

### `verify(params: VerifyRequest | dict | None = None) -> VerifyResponse`

Verifies payment after user redirect or callback.

#### Parameters

**`params`** (`VerifyRequest`)

| Field      | Type  | Required | Description                               |
| ---------- | ----- | -------- | ----------------------------------------- |
| `track_id` | `int` | ✅        | Transaction tracking ID returned by Zibal |

#### Returns

**`VerifyResponse`**

| Field               | Type                    | Description                                    |
| ------------------- | ----------------------- | ---------------------------------------------- |
| `result`            | `int`                   | Response status code (100 = success)           |
| `message`           | `str`                   | Result message                                 |
| `amount`            | `int | None`            | Paid amount in Rial                            |
| `status`            | `int | None`           | Bank transaction status (1=success,2=canceled) |
| `paid_at`           | `str | None`           | ISO 8601 payment timestamp                     |
| `card_number`       | `str | None`           | Masked payer card number                       |
| `ref_number`        | `str | None`           | Bank reference number                          |
| `order_id`          | `str | None`           | Merchant order ID                              |
| `description`       | `str | None`           | Additional description                         |
| `track_id`          | `int | None`           | Tracking ID                                    |
| `multiplexingInfos` | `List[MultiplexingInfo]` | Optional split payment details                 |

#### Raises

* `ZibalError` or subclasses

---

### `callback_verify(callback: CallbackParams  | dict | None = None) -> VerifyResponse`

Server-to-server verification using callback payload.

#### Parameters

**`callback`** (`CallbackParams`)

| Field      | Type           | Description                  |
| ---------- | -------------- | ---------------------------- |
| `track_id` | `int`          | Transaction ID from callback |
| `success`  | `int`          | 1 = success, 0 = failure     |
| `order_id` | `str`          | Merchant order ID            |
| `status`   | `Status | int` | Payment status code          |

#### Returns

**`VerifyResponse`** (same as above)

#### Raises

* `ZibalError` or subclasses

---

### `inquiry(params: InquiryRequest | dict | None = None) -> InquiryResponse`

Fetches current transaction status.

#### Parameters

**`params`** (`InquiryRequest`)

| Field      | Type  | Required | Description             |
| ---------- | ----- | -------- | ----------------------- |
| `track_id` | `int` | ✅        | Transaction tracking ID |

#### Returns

**`InquiryResponse`**

| Field               | Type                    | Description                    |
| ------------------- | ----------------------- | ------------------------------ |
| `result`            | `int`                   | Response status code           |
| `message`           | `str`                   | Status message                 |
| `ref_number`        | `int | None`            | Bank reference number          |
| `paid_at`           | `str | None`           | Payment timestamp (ISO 8601)   |
| `verified_at`       | `str | None`           | Verification timestamp         |
| `status`            | `int`                   | Payment status                 |
| `amount`            | `int`                   | Amount of transaction          |
| `order_id`          | `str`                   | Merchant order ID              |
| `description`       | `str`                   | Transaction description        |
| `card_number`       | `str | None`           | Masked card number             |
| `wage`              | `int`                   | Associated wage                |
| `created_at`        | `str`                   | Transaction creation timestamp |
| `multiplexingInfos` | `List[MultiplexingInfo]` | Revenue sharing details        |

---

### `get_payment_redirect_url(track_id: int) -> str`

Builds the URL for redirecting the user to Zibal’s payment page.

#### Parameters

* `track_id` (`int`): Tracking ID from `payment()` or `lazy_payment()`.

#### Returns

* `str`: Complete redirect URL.

Example:

```python
url = pay.get_payment_redirect_url(track_id=123456)
```

Result: `https://gateway.zibal.ir/start/123456`

---

> **Note**: Methods can be used in synchronous or asynchronous contexts. Just use `await` in async functions.

## Exception Handling

All Zibal-specific errors inherit from `ZibalError`. The gateway automatically raises the proper subclass based on the status code.

Zibal error subclasses:

* `MerchantNotFoundError`
* `MerchantInactiveError`
* `InvalidMerchantError`
* `AmountTooLowError`
* `InvalidCallbackUrlError`
* `InvalidPercentModeError`
* `InvalidMultiplexingBeneficiariesError`
* `InactiveMultiplexingBeneficiaryError`
* `MissingSelfBeneficiaryError`
* `AmountMismatchInMultiplexingError`
* `InsufficientWalletBalanceForFeesError`
* `AmountExceedsLimitError`
* `InvalidNationalCodeError`
* `AlreadyConfirmedError`
* `PaymentNotSuccessfulError`
* `InvalidTrackIdError`

---

## Sandbox Testing

> 🧪 **Test Mode:** To use Zibal in sandbox mode, set your `merchant_id` to the string `"zibal"`. This simulates transactions for development purposes.
>
> ```python
> from payman import Zibal
>
> pay = Zibal(merchant_id="zibal")
> ```

This lets you safely test the entire payment flow without processing real transactions.

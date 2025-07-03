# Payman

**Payman** is a Python package for integrating with Iranian payment gateways like **Zarinpal** and **Zibal**.
It provides a clean and flexible interface for handling payments in both sync and async Python applications.

---

## What is Payman?

Payman provides everything you need to work with popular Iranian payment gateways:

- Requesting payments
- Redirecting users to the payment page
- Verifying completed transactions
- Handling gateway-specific errors and inconsistencies

It provides a unified and developer-friendly interface that works consistently across multiple providers.


## Key Features
- **Simple and consistent API**  
 You can focus on your business logic — HTTP calls, serialization, and gateway-specific details are handled internally.

- **Supports both sync and async**  
 Compatible with synchronous and asynchronous code, including FastAPI, Flask, scripts, and background tasks.

- **Pydantic models for inputs and outputs**  
  Type-safe, auto-validating models make integration predictable and IDE-friendly.

- **Modular and extensible design**  
 Each gateway integration is separated. You can include only what you need or extend the package with your own gateway.

- **Unified error handling**  
 Common exception classes are used across gateways, with optional gateway-specific errors when needed.

- **Includes test coverage and mock support**  
 The package includes tests and gateway simulations to help with development and integration.

- **Suitable for real projects**  
 Designed to be usable in real applications, from small services to larger deployments.


## Supported Gateways

Currently supported gateways include:

- **[Zarinpal](https://www.zarinpal.com/)**
- **[Zibal](https://zibal.ir/)**

More providers (like IDPay, NextPay, etc.) are planned for future releases.


## Quick Example
Here's how to quickly request a payment using ZarinPal:

```python
from payman.gateways.zarinpal import ZarinPal, Status
from payman.gateways.zarinpal.models import PaymentRequest, VerifyRequest

merchant_id = "YOUR_MERCHANT_ID"
amount = 10000  # IRR

pay = ZarinPal(merchant_id=merchant_id)

# 1. Create Payment
create_resp = pay.payment(
    PaymentRequest(
        amount=amount,
        callback_url="https://your-site.com/callback",
        description="Test Order"
    )
)
    
if create_resp.success:
    authority = create_resp.authority
    print("Redirect user to:", pay.get_payment_redirect_url(authority))
else:
    print(f"Create failed: {create_resp.message} (code {create_resp.code})")

# 2. After user returns to callback_url, verify the payment:
verify_resp = pay.verify(
    VerifyRequest(authority=authority, amount=amount)
)

if verify_resp.success:
    print("Payment successful:", verify_resp.ref_id)
elif verify_resp.already_verified:
    print("Already verified.")
else:
    print("Verification failed:", verify_resp)
```

You can also use the package in async mode with frameworks like FastAPI.

## Documentation Sections
To help you get started with Payman, check out the following pages:

- [Installation](./installation.md) – How to install and set up Payman.
 
- [Usage Guide](./usage.md) – How to work with different gateways.

- [API Reference](./api.md) – Full reference for all available methods and classes.


## Contributing

We welcome contributions, feedback, and bug reports.
Visit our [GitHub repository](https://github.com/irvaniamirali/payman) to check issues, submit pull requests, or suggest improvements.


## License
Payman is licensed under the GNU GPL v3 license.
You are free to use, modify, and distribute it under the terms of this license.

Need help? Want to request a new gateway? Open an issue on GitHub or contact the maintainer.

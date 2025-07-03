# Payman — Unified Payment Gateway Integration for Python

**Payman** is a Python package for integrating with Iranian payment gateways like **Zarinpal** and **Zibal**.
It provides a clean and flexible interface for handling payments in both sync and async Python applications.

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


## Supported Payment Gateways (Currently)
- [ZarinPal](https://www.zarinpal.com/)
- [Zibal](https://zibal.ir/)
- *More gateways will be added soon...*

## Installation

```bash
pip install payman
```

## Quick Start: ZarinPal Integration (Create, Redirect, Verify)

Here's a simple example using ZarinPal:

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

## Full Documentation
For detailed instructions on using ZarinPal and other gateways with Payman, including all parameters, response codes, and integration tips, please refer to the complete guide:
- [documentation](./docs/index.md)


## License

Licensed under the GNU General Public License v3.0 (GPL-3.0). See the LICENSE file for details.

## Contributing

Contributions to Payman are welcome and highly appreciated. If you wish to contribute, please follow these guidelines:

- Fork the repository and create a new branch for your feature or bugfix.  
- Ensure your code adheres to the project's coding standards and passes all tests.  
- Write clear, concise commit messages and provide documentation for new features.  
- Submit a pull request with a detailed description of your changes for review.

By contributing, you agree that your work will be licensed under the project's license.

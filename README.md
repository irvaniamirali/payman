# Payman — Unified Payment Gateway Integration for Python

Payman is a Python package that simplifies integration with multiple Iranian payment gateways using async and sync APIs with a clean and unified interface.

## Key Features
- Unified API for multiple gateways
- Sync and Async support (auto-detected)
- Modular and extensible architecture
- Clean Pythonic codebase

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
import asyncio
from payman.gateways.zarinpal import ZarinPal
from payman.gateways.zarinpal.models import PaymentRequest, VerifyRequest

merchant_id = "YOUR_MERCHANT_ID"
amount = 1000

pay = ZarinPal(merchant_id=merchant_id)

# 1. Create Payment
create_resp = pay.payment(
    PaymentRequest(
        amount=amount,
        callback_url="https://your-site.com/callback",
        description="Test Order"
    )
)
    
if create_resp.code == 100:
    authority = create_resp.authority
    print("Redirect user to:", pay.get_payment_redirect_url(authority))
else:
    print(f"Create failed: {create_resp.message} (code {create_resp.code})")

# 2. After user returns to callback_url, verify the payment:
verify_resp = pay.verify(
    VerifyRequest(authority=authority, amount=amount)
)

if verify_resp.code == 100:
    print("Payment successful:", verify_resp.ref_id)
elif verify_resp.code == 101:
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

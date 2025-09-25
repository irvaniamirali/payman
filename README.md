# Payman — Unified Payment Gateway Integration for Python

**Payman** is a Python package for integrating with Iranian payment gateways like **ZarinPal** and **Zibal**.
It provides a clean and flexible interface for handling payments in both sync and async Python applications.

## Key Features
- **Simple and consistent API**  
 You can focus on your business logic — HTTP calls, serialization, and gateway-specific details are handled internally.

- **Supports Async**  
 Compatible with asynchronous code, including FastAPI and background tasks.

- **Pydantic models for inputs and outputs**  
  Type-safe, auto-validating models make integration predictable and IDE-friendly.

- **Modular and extensible design**  
 Each gateway integration is separated. You can include only what you need or extend the package with your own gateway.

- **Unified error handling**  
 Common exception classes are used across gateways, with optional gateway-specific errors when needed.

- **Suitable for real projects**  
 Designed to be usable in real applications, from small services to larger deployments.


## Supported Payment Gateways (Currently)
- [Zibal](https://zibal.ir/)
- *More gateways will be added soon...*

## Installation

```bash
pip install -U payman[zibal]
```

## Quick Start: Async Zibal Integration (Create, Redirect, Verify)

```python
import asyncio

from payman import Payman

gateway = Payman("zibal", merchant_id="abc")

async def main():
    payment_request = await gateway.initiate_payment(
        amount=10_000,
        callback_url="https://your-site.com/callback",
        description="Test payment"
    )

    if not payment_request.success:
        print(f"Payment creation failed: {payment_request.message}")
        return

    print("Redirect user to:", gateway.get_payment_redirect_url(payment_request.track_id))

    payment_verification = await gateway.verify_payment(track_id=payment_request.track_id)

    if payment_verification.success:
        print("Payment successful. Ref ID:", payment_verification.ref_id)
    elif payment_verification.already_verified:
        print("Payment already verified.")
    else:
        print("Payment verification failed.")

asyncio.run(main())
```

## Full Documentation
For detailed instructions on using Zibal and other gateways with Payman, including all parameters, response codes, and integration tips, please refer to the complete guide:
- [documentation](https://irvaniamirali.github.io/payman)


## License

Licensed under the GNU General Public License v3.0 (GPL-3.0). See the LICENSE file for details.

## Contributing

Contributions to Payman are welcome and highly appreciated. If you wish to contribute, please follow these guidelines:

- Fork the repository and create a new branch for your feature or bugfix.  
- Ensure your code adheres to the project's coding standards and passes all tests.  
- Write clear, concise commit messages and provide documentation for new features.  
- Submit a pull request with a detailed description of your changes for review.

By contributing, you agree that your work will be licensed under the project's license.

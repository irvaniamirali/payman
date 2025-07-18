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

- **Suitable for real projects**  
 Designed to be usable in real applications, from small services to larger deployments.


## Supported Payment Gateways (Currently)
- [ZarinPal](https://www.zarinpal.com/)
- [Zibal](https://zibal.ir/)
- *More gateways will be added soon...*

## Installation

```bash
pip install -U payman
```

## Quick Start: Async Zibal Integration (Create, Redirect, Verify)

```python
import asyncio
from payman import Payman

pay = Payman("zibal", merchant_id="...")

async def main():
    create = await pay.payment(
        amount=10_000,
        callback_url="https://your-site.com/callback",
        description="Test"
    )

    if not create.success:
        print(f"Create failed: {create.message}")
        return

    print("Redirect to:", pay.get_payment_redirect_url(create.track_id))

    verify = await pay.verify(track_id=create.track_id)

    if verify.success:
        print("Paid:", verify.ref_id)
    elif verify.already_verified:
        print("Already verified.")
    else:
        print("Verify failed.")

asyncio.run(main())
```

### Sync Zibal Integration (Create, Redirect, Verify)

```python
from payman import Payman

pay = Payman("zibal", merchant_id="...")

create = pay.payment(
    amount=10_000,
    callback_url="https://your-site.com/callback",
    description="Test"
)

if not create.success:
    print(f"Create failed: {create.message}")
    exit(1)

print("Redirect to:", pay.get_payment_redirect_url(create.track_id))

verify = pay.verify(track_id=create.track_id)

if verify.success:
    print("Paid:", verify.ref_id)
elif verify.already_verified:
    print("Already verified.")
else:
    print("Verify failed.")
```

## Full Documentation
For detailed instructions on using ZarinPal and other gateways with Payman, including all parameters, response codes, and integration tips, please refer to the complete guide:
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

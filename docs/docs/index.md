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

- **Suitable for real projects**  
 Designed to be usable in real applications, from small services to larger deployments.


## Supported Gateways

Currently supported gateways include:

- **[Zarinpal](https://www.zarinpal.com/)**
- **[Zibal](https://zibal.ir/)**

More providers (like IDPay, NextPay, etc.) are planned for future releases.


## Quick Example
Here's how to quickly request a payment using Zibal:

```python
import asyncio
from payman import Payman
from payman.errors import GatewayError

pay = Payman("zibal", merchant_id="...")

async def process_payment():
    try:
        # Step 1: Create payment request
        payment = await pay.payment(
            amount=25_000,
            callback_url="https://your-site.com/callback",
            description="Order #123"
        )
    except GatewayError as e:
        print(f"[Error] Payment request failed: {e}")
        return

    if not payment.success:
        print(f"[Create Failed] {payment.message} (code: {payment.code})")
        return

    print(f"[Redirect] {pay.get_payment_redirect_url(payment.track_id)}")

    # Simulate waiting for user to return from gateway
    await asyncio.sleep(2)  # Just for example purposes

    try:
        # Step 2: Verify transaction
        verify = await pay.verify(track_id=payment.track_id)
    except GatewayError as e:
        print(f"[Error] Verification failed: {e}")
        return

    if verify.success:
        print(f"[Success] Payment confirmed. Ref ID: {verify.ref_id}")
    elif verify.already_verified:
        print("[Notice] Payment already verified.")
    else:
        print(f"[Verify Failed] {verify.message} (code: {verify.code})")

asyncio.run(process_payment())
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

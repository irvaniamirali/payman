# Payman

**Payman** is a modern, unified Python SDK for integrating with Iranian payment gateways. It provides a clean, type-safe, and flexible interface for handling payments in asynchronous Python applications.

---

## What is Payman?

Payman simplifies payment gateway integration by providing everything you need to work with popular Iranian payment gateways:

- **Payment initiation** - Create payment requests with a single method call
- **User redirection** - Seamlessly redirect users to payment pages
- **Payment verification** - Verify completed transactions securely
- **Error handling** - Comprehensive error handling with gateway-specific exceptions
- **Type safety** - Full Pydantic model support for inputs and outputs

The library abstracts away the complexity of different gateway APIs, providing a consistent interface that works across multiple providers.

## Key Features

### 🚀 **Simple and Consistent API**
Focus on your business logic while Payman handles HTTP calls, serialization, and gateway-specific details internally.

### ⚡ **Async Support**
Compatible with asynchronous code, including FastAPI, and background tasks.

### 🛡️ **Type Safety with Pydantic**
Type-safe, auto-validating models make integration predictable and IDE-friendly with full autocomplete support.

### 🔧 **Modular and Extensible Design**
Each gateway integration is separated. Include only what you need or extend the package with your own gateway implementations.

### 🎯 **Unified Error Handling**
Common exception classes across gateways, with optional gateway-specific errors when needed for detailed error handling.

### 🏗️ **Production Ready**
Designed for real applications, from small services to large-scale deployments with comprehensive logging and retry mechanisms.

## Supported Gateways

Currently supported payment gateways:

- **[Zibal](https://zibal.ir/)** - Complete integration with all features
- **[Zarinpal](https://www.zarinpal.com/)** - Coming soon

More providers (IDPay, NextPay, etc.) are planned for future releases.

## Quick Start

Here's how to quickly integrate payments using Zibal:

```python
import asyncio
from payman import Payman, GatewayError

# Initialize the payment gateway
pay = Payman("zibal", merchant_id="your-merchant-id")

async def process_payment():
    try:
        # Step 1: Create payment request
        response = await pay.initiate_payment(
            amount=25_000,
            callback_url="https://your-site.com/callback",
            description="Order #123",
            order_id="order-123"
        )
        
        if not response.success:
            print(f"Payment creation failed: {response.message}")
            return

        # Step 2: Redirect user to payment page
        payment_url = pay.get_payment_redirect_url(response.track_id)
        print(f"Redirect user to: {payment_url}")

        # Step 3: Verify payment (after user returns)
        verify_response = await pay.verify_payment(track_id=response.track_id)
        
        if verify_response.success:
            print(f"Payment successful! Ref ID: {verify_response.ref_number}")
        else:
            print(f"Payment verification failed: {verify_response.message}")

    except GatewayError as e:
        print(f"Gateway error: {e}")

# Run the payment flow
asyncio.run(process_payment())
```

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

# Payman

**Payman** is a modern and extensible Python package that simplifies integration with Iranian payment gateways such as **Zarinpal**, **Zibal**, and others.

Whether you're building a small e-commerce site or a complex microservice system, Payman helps you manage payments with **clean**, **flexible**, and **Pythonic** code — fully supporting both **synchronous** and **asynchronous** environments.

---

## What is Payman?

Payman provides everything you need to work with popular Iranian payment gateways:

- Requesting payments
- Redirecting users to the payment page
- Verifying completed transactions
- Handling gateway-specific errors and inconsistencies

It provides a unified and developer-friendly interface that works consistently across multiple providers.


## Key Features
- **Clean, developer-friendly API**  
  Focus on business logic — the low-level HTTP and serialization details are abstracted away.

- **Sync and Async support out-of-the-box**  
  Works seamlessly in both synchronous and asynchronous environments: FastAPI, Flask, scripts, or background jobs.

- **Pydantic-based request & response models**  
  Type-safe, auto-validating models make integration predictable and IDE-friendly.

- **Fully modular architecture**  
  Each gateway is isolated and extensible — plug in only what you need or add your own.

- **Consistent error handling**  
  Unified exception classes across all gateways, with gateway-specific subclasses for clarity.

- **Well-tested and reliable**  
  Built with test coverage, mock gateway simulations, and robust edge case handling.

- **Production-grade design**  
  Suitable for real-world use in high-traffic environments and mission-critical systems.


## Supported Gateways

Currently supported gateways include:

- **Zarinpal**
- **Zibal**

More providers (like IDPay, NextPay, etc.) are planned for future releases.


## Quick Example
Here's how to quickly request a payment using Zarinpal:

```python
from payman import ZarinPal
from payman.gateways.zarinpal.models import PaymentRequest, VerifyRequest

# Initialize the gateway with your merchant ID
pay = ZarinPal(merchant_id="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")

amount = 10000  # IRR

# Create a payment request
payment_response = pay.payment(
    PaymentRequest(
        amount=amount,
        callback_url="https://your-site.com/callback",
        description="Test Payment"
    )
)

authority = payment_response.authority

# Get the redirect URL and show it to the user
redirect_url = pay.get_payment_redirect_url(authority)

# Verify payment
verify_response = pay.verify(
    VerifyRequest(
        amount=amount,
        authority=authority
    )
)

ref_id = verify_response.ref_id
print(f"Ref ID: {ref_id}")
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

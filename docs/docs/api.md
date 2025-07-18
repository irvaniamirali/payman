# Payman API Reference

Welcome to the **Payman API** documentation.  
This section provides a unified interface for interacting with multiple Iranian payment gateways, including:

- [ZarinPal](./gateways/zarinpal/api.md)
- [Zibal](./gateways/zibal/api.md)

---

##️ Usage Overview

Payman provides a consistent and developer-friendly API for initiating, verifying, and reversing payments — regardless of the gateway provider. All gateways follow the same public interface and support both **synchronous** and **asynchronous** usage out-of-the-box.

# Example

```python
from payman import Payman

gateway = Payman("zarinpal", merchant_id="YOUR-ID")
response = await gateway.payment(...)
```

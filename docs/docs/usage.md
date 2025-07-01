# Usage Guide

This guide will help you understand how to use Payman in your project and integrate with specific gateways.

---

## Supported Gateways

Each gateway comes with its own usage guide and example code. Click on the links below to view detailed documentation:

- [ZarinPal](gateways/zarinpal/usage.md)
- [Zibal](./gateways/zibal/usage.md)

---

## Common Workflow

Regardless of the gateway, the typical payment flow includes:

1. **Creating a payment request**
2. **Redirecting the user to the payment gateway**
3. **Handling the callback**
4. **Verifying the payment**

Payman standardizes this flow across all gateways, so once you're familiar with one, switching to another is easy.

For advanced usage or contributing custom gateways, see the [API Reference](./api.md).

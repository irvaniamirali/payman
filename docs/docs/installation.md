# Installation

This page will help you install and set up **Payman** in your Python project in just a few steps.

---

## Requirements

- **Python 3.10 or higher** - Payman uses modern Python features and type hints
- **pip** - Python package installer

Check your Python version:

```bash
python --version
# or
python3 --version
```

## Installation Methods

### Method 1: Install from PyPI (Recommended)

The easiest way to install Payman is via PyPI:

```bash
pip install payman
```

### 👉 If you need a specific payment gateway plugin (e.g., Zibal), install Payman with extras:
```bash
pip install payman[zibal]
```

### Method 2: Install from GitHub (Development)

If you want the latest development version with bleeding-edge features:

```bash
pip install git+https://github.com/irvaniamirali/payman.git
```

### Method 3: Install from Source

For development or if you want to modify the source code:

```bash
git clone https://github.com/irvaniamirali/payman.git
cd payman
pip install -e .
```

## Virtual Environment Setup (Recommended)

It's highly recommended to use a virtual environment to keep dependencies isolated:

### Using `venv` (Built-in)

```bash
# Create virtual environment
python -m venv payman-env

# Activate (Linux/macOS)
source payman-env/bin/activate

# Activate (Windows)
payman-env\Scripts\activate

# Install Payman
pip install payman
```

### Using `uv` (Fast)

```bash
# Create and activate environment
uv venv payman-env
source payman-env/bin/activate  # Linux/macOS
# payman-env\Scripts\activate   # Windows

# Install Payman
uv pip install payman
```

## Verify Installation

Test your installation by running this simple script:

```python
from payman import Payman

# This should work without errors
pay = Payman("zibal", merchant_id="test")
print("Payman installed successfully!")
```

## Dependencies

Payman automatically installs these dependencies:

- **pydantic** - Data validation and settings management
- **httpx** - Modern HTTP client for async requests
- **email-validator** - Email validation support
- **typing-extensions** - Extended typing support

## Troubleshooting

### Common Issues

**ImportError: No module named 'payman'**
- Make sure you're in the correct virtual environment
- Verify installation with `pip list | grep payman`

**Python version too old**
- Payman requires Python 3.10+
- Upgrade Python or use a version manager like `pyenv`

**Permission denied errors**
- Use `--user` flag: `pip install --user payman`
- Or use a virtual environment (recommended)

### Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/irvaniamirali/payman/issues)
2. Review the [Usage Guide](./usage.md)
3. Join our community discussions

## Next Steps

Once installed, you can:

1. Read the [Usage Guide](./usage.md) to learn how to integrate payments
2. Check out the [API Reference](./api.md) for detailed documentation
3. Explore [Zibal Integration](./gateways/zibal/usage.md) for specific gateway usage

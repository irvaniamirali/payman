class BaseURLBuilder(str):
    _BASE_DOMAIN = {
        True: "sandbox.zarinpal.com",
        False: "www.zarinpal.com"
    }

    def __new__(cls, sandbox: bool, version: int):
        domain = cls._BASE_DOMAIN[sandbox]
        url = f"https://{domain}/pg/v{version}/payment"
        return str.__new__(cls, url)

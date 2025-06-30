class BaseURLBuilder(str):
    __BASE_DOMAIN = {
        True: "sandbox.zarinpal.com",
        False: "www.zarinpal.com"
    }

    def __new__(cls, sandbox: bool, version: int):
        domain = cls.__BASE_DOMAIN[sandbox]
        url = f"https://{domain}/pg/v{version}/payment"
        return str.__new__(cls, url)

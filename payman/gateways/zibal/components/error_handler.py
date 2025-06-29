from payman.errors import PaymentGatewayManager


class ErrorHandler:
    def handle(self, response: dict):
        if response.get("result") != 100:
            raise PaymentGatewayManager.handle_error(
                "Zibal", response.get("result"), response.get("message")
            )

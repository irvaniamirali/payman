from payman.errors import GatewayManager


class ErrorHandler:
    def handle(self, response: dict):
        if response.get("result") != 100:
            raise GatewayManager.handle_error(
                "Zibal", response.get("result"), response.get("message")
            )

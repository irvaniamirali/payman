from .base import PaymentGatewayError

ERROR_CODE_MAPPINGS = {
    "ZarinPal": "payman.gateways.zarinpal.errors.ZARINPAL_ERRORS",
    "Zibal": "payman.gateways.zibal.errors.ZIBAL_ERRORS",
}


class PaymentGatewayManager:
    @staticmethod
    def handle_error(gateway_name: str, error_code: int, error_message: str) -> PaymentGatewayError:
        """Handles errors based on the gateway name and error code."""
        error_mapping = PaymentGatewayManager._get_error_mapping(gateway_name)

        if error_mapping:
            error_class = error_mapping.get(error_code)
            if error_class:
                return error_class(error_message)

        return PaymentGatewayError(
            f"Unknown error code: {error_code} - {error_message}"
        )

    @staticmethod
    def _get_error_mapping(gateway_name: str):
        """Fetches the error mapping for the specified gateway."""
        from importlib import import_module

        mapping_path = ERROR_CODE_MAPPINGS.get(gateway_name)
        if mapping_path:
            module_path, mapping_name = mapping_path.rsplit(".", 1)
            module = import_module(module_path)
            return getattr(module, mapping_name)
        return None

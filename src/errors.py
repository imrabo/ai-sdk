class SDKError(Exception):
    code: str

    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code


class SDKValidationError(SDKError):
    def __init__(self, message: str):
        super().__init__(message, "sdk_validation_error")


class ValidationError(SDKValidationError):
    def __init__(self, message: str):
        super().__init__(message)



class UnsupportedCapabilityError(SDKError):
    provider: str | None

    def __init__(self, message: str, provider: str | None = None):
        super().__init__(message, "unsupported_capability")
        self.provider = provider


class ProviderError(SDKError):
    provider_id: str | None
    details: dict | None

    def __init__(
        self, message: str, provider_id: str | None = None, details: dict | None = None
    ):
        super().__init__(message, "provider_error")
        self.provider_id = provider_id
        self.details = details


class TransportError(SDKError):
    def __init__(self, message: str):
        super().__init__(message, "transport_error")


class TimeoutError(SDKError):
    def __init__(self, message: str):
        super().__init__(message, "timeout")

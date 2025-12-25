from .types import Message, GenerationOptions
from .errors import SDKValidationError


def validate_messages(messages: list[Message]) -> None:
    if not isinstance(messages, list) or len(messages) == 0:
        raise SDKValidationError("messages must be a non-empty list")

    for m in messages:
        if m.role not in ("system", "user", "assistant"):
            raise SDKValidationError(f"invalid message role: {m.role}")
        if not isinstance(m.content, str):
            raise SDKValidationError("message content must be a string")


def validate_generation_options(options: GenerationOptions | None) -> None:
    if options is None:
        return
    if options.max_tokens is not None and options.max_tokens <= 0:
        raise SDKValidationError("options.max_tokens must be > 0")
    if options.temperature is not None and not (0.0 <= options.temperature <= 2.0):
        raise SDKValidationError("options.temperature must be between 0 and 2")
    if options.top_p is not None and not (0.0 <= options.top_p <= 1.0):
        raise SDKValidationError("options.top_p must be between 0 and 1")

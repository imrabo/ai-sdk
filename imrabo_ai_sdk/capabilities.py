from .types import Provider, InternalRequest
from .errors import UnsupportedCapabilityError


def ensure_capabilities(
    provider: Provider, req: InternalRequest, needs_streaming: bool = False
) -> None:
    caps = provider.capabilities()
    if needs_streaming and not caps.streaming:
        raise UnsupportedCapabilityError(
            f"Provider '{provider.id}' does not support streaming", provider.id
        )

    if (
        req.options
        and req.options.max_tokens is not None
        and caps.max_tokens is not None
    ):
        if req.options.max_tokens > caps.max_tokens:
            raise UnsupportedCapabilityError(
                f"Requested max_tokens ({req.options.max_tokens}) exceeds provider '{provider.id}' max of {caps.max_tokens}",
                provider.id,
            )

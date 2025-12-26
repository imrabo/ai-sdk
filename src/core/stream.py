from typing import Iterable
from ..types import GenerateRequest, StreamChunk
from ..normalize import normalize_request
import src.config.resolve_provider as resolve_provider_module
from ..capabilities import ensure_capabilities


def stream(request: GenerateRequest) -> Iterable[StreamChunk]:
    internal = normalize_request(request)

    provider = resolve_provider_module.resolve_provider(request.runtime, request.model)

    ensure_capabilities(provider, internal, needs_streaming=True)

    # Provider.stream returns an iterable/generator of StreamChunk
    for chunk in provider.stream(internal):
        yield chunk

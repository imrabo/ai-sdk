from ..types import GenerateRequest, GenerateResult
from ..normalize import normalize_request
import imrabo_ai_sdk.config.resolve_provider as resolve_provider_module
from ..capabilities import ensure_capabilities


def generate(request: GenerateRequest) -> GenerateResult:
    internal = normalize_request(request)

    provider = resolve_provider_module.resolve_provider(request.runtime, request.model)

    ensure_capabilities(provider, internal, needs_streaming=False)

    result = provider.generate(internal)
    return result

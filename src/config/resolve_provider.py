from typing import Optional
from ..types import Provider, RuntimeConfig
from ..providers.registry import get_provider_for_runtime


def resolve_provider(
    runtime: Optional[RuntimeConfig], model: Optional[str]
) -> Provider:
    # Delegate to providers registry
    return get_provider_for_runtime(runtime, model)

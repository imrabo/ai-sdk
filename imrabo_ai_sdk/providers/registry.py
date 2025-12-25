from typing import Optional
from .generic_url import GenericURLProvider
from .ollama import OllamaProvider
from .kernel import KernelProvider
from ..types import Provider, RuntimeConfig


def get_provider_for_runtime(
    runtime: Optional[RuntimeConfig], model: Optional[str]
) -> Provider:
    if runtime is None:
        raise NotImplementedError(
            "No runtime provided; provider resolution requires runtime config"
        )

    if runtime.type == "url":
        endpoint = runtime.endpoint or ""
        # Heuristic: if endpoint contains 'ollama' use OllamaProvider
        if "ollama" in (endpoint or ""):
            return OllamaProvider(endpoint=endpoint, headers=runtime.headers)
        # Default to GenericURLProvider
        return GenericURLProvider(
            id="generic-url", endpoint=endpoint, headers=runtime.headers
        )

    if runtime.type == "kernel":
        return KernelProvider()

    raise NotImplementedError(f"Unsupported runtime type: {runtime.type}")

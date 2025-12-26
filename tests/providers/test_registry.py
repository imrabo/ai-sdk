from src.config.resolve_provider import resolve_provider
from src.types import RuntimeConfig


def test_resolve_generic_url():
    rc = RuntimeConfig(type="url", endpoint="http://example.com")
    provider = resolve_provider(rc, model="m")
    assert provider is not None
    assert provider.id == "generic-url"


def test_resolve_ollama_heuristic():
    rc = RuntimeConfig(type="url", endpoint="http://localhost:11434/ollama")
    provider = resolve_provider(rc, model="m")
    assert provider.id == "ollama"


def test_resolve_kernel_stub():
    rc = RuntimeConfig(type="kernel")
    provider = resolve_provider(rc, model="m")
    assert provider.id == "kernel"

import pytest
from imrabo_ai_sdk.core.generate import generate
from imrabo_ai_sdk.core.stream import stream
from imrabo_ai_sdk.types import (
    GenerateRequest,
    Message,
    GenerationOptions,
    StreamChunk,
    Capabilities,
)
from imrabo_ai_sdk.errors import UnsupportedCapabilityError

import imrabo_ai_sdk.config.resolve_provider as resolver


class FakeProvider:
    def __init__(self, caps: Capabilities, output: str = "hello"):
        self.id = "fake"
        self._caps = caps
        self._output = output

    def capabilities(self) -> Capabilities:
        return self._caps

    def generate(self, req):
        return type("R", (), {"output": self._output, "tokens": 1})

    def stream(self, req):
        # yield some token chunks then done
        yield StreamChunk(type="token", value="h")
        yield StreamChunk(type="token", value="i")
        yield StreamChunk(type="done")


def test_generate_uses_provider(monkeypatch):
    fake = FakeProvider(Capabilities(streaming=True, tools=False, json=False))
    monkeypatch.setattr(resolver, "resolve_provider", lambda runtime, model: fake)

    req = GenerateRequest(model="x", messages=[Message(role="user", content="hi")])
    res = generate(req)
    assert res.output == "hello"


def test_stream_tokens_and_done(monkeypatch):
    fake = FakeProvider(Capabilities(streaming=True, tools=False, json=False))
    monkeypatch.setattr(resolver, "resolve_provider", lambda runtime, model: fake)

    req = GenerateRequest(
        model="x", messages=[Message(role="user", content="stream me")]
    )
    chunks = list(stream(req))
    types = [c.type for c in chunks]
    values = [c.value for c in chunks if c.type == "token"]

    assert types[-1] == "done"
    assert "".join(values) == "hi"


def test_stream_unsupported(monkeypatch):
    fake = FakeProvider(Capabilities(streaming=False, tools=False, json=False))
    monkeypatch.setattr(resolver, "resolve_provider", lambda runtime, model: fake)

    req = GenerateRequest(
        model="x", messages=[Message(role="user", content="stream me")]
    )
    with pytest.raises(UnsupportedCapabilityError):
        list(stream(req))


def test_max_tokens_enforced(monkeypatch):
    fake = FakeProvider(
        Capabilities(streaming=True, tools=False, json=False, max_tokens=10)
    )
    monkeypatch.setattr(resolver, "resolve_provider", lambda runtime, model: fake)

    req = GenerateRequest(
        model="x",
        messages=[Message(role="user", content="hi")],
        options=GenerationOptions(max_tokens=100),
    )
    with pytest.raises(UnsupportedCapabilityError):
        generate(req)

import pytest
import httpx
from src.providers.generic_url import GenericURLProvider
from src.types import InternalRequest, Message


def test_generate_calls_endpoint(monkeypatch):
    def handler(request):
        return httpx.Response(200, json={"output": "hello"})

    transport = httpx.MockTransport(handler)

    class MockClient(httpx.Client):
        def __init__(self, *args, **kwargs):
            super().__init__(transport=transport, *args, **kwargs)

    monkeypatch.setattr(httpx, "Client", MockClient)

    provider = GenericURLProvider(id="g", endpoint="http://example.com/api/generate")
    req = InternalRequest(
        model="m", messages=[Message(role="user", content="hi")], options=None
    )
    res = provider.generate(req)
    assert res.output == "hello"


def test_stream_parses_chunks(monkeypatch):
    def handler(request):
        body = b"h\ni\nDONE\n"
        return httpx.Response(200, content=body)

    transport = httpx.MockTransport(handler)

    class MockClient(httpx.Client):
        def __init__(self, *args, **kwargs):
            super().__init__(transport=transport, *args, **kwargs)

    monkeypatch.setattr(httpx, "Client", MockClient)

    provider = GenericURLProvider(id="g", endpoint="http://example.com/api/stream")
    req = InternalRequest(
        model="m", messages=[Message(role="user", content="stream")], options=None
    )
    chunks = list(provider.stream(req))
    assert [c.type for c in chunks if c.type != "done"] == ["token", "token"]
    assert "".join([c.value for c in chunks if c.type == "token"]) == "hi"

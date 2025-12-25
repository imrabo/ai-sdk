import httpx
import pytest
from imrabo_ai_sdk.providers.generic_url import GenericURLProvider
from imrabo_ai_sdk.types import InternalRequest, Message


def test_generate_calls_endpoint(monkeypatch):
    # Mock httpx.Client.post to return a response with JSON
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
    # Simulate stream by returning content with newlines
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


def test_stream_unsupported_flag():
    provider = GenericURLProvider(id="g", endpoint="http://x", supports_streaming=False)
    req = InternalRequest(
        model="m", messages=[Message(role="user", content="stream")], options=None
    )
    with pytest.raises(RuntimeError):
        list(provider.stream(req))

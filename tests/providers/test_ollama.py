import httpx
from src.providers.ollama import OllamaProvider
from src.types import InternalRequest, Message


def test_ollama_generate(monkeypatch):
    def handler(request):
        return httpx.Response(200, json={"output": "ollama says hi"})

    transport = httpx.MockTransport(handler)

    class MockClient(httpx.Client):
        def __init__(self, *args, **kwargs):
            super().__init__(transport=transport, *args, **kwargs)

    monkeypatch.setattr(httpx, "Client", MockClient)

    p = OllamaProvider(endpoint="http://localhost:11434")
    res = p.generate(
        InternalRequest(model="m", messages=[Message(role="user", content="hi")])
    )
    assert res.output == "ollama says hi"


def test_ollama_stream(monkeypatch):
    def handler(request):
        body = b"hey\nthere\nDONE\n"
        return httpx.Response(200, content=body)

    transport = httpx.MockTransport(handler)

    class MockClient(httpx.Client):
        def __init__(self, *args, **kwargs):
            super().__init__(transport=transport, *args, **kwargs)

    monkeypatch.setattr(httpx, "Client", MockClient)

    p = OllamaProvider(endpoint="http://localhost:11434")
    chunks = list(
        p.stream(
            InternalRequest(model="m", messages=[Message(role="user", content="hi")])
        )
    )
    assert [c.type for c in chunks if c.type != "done"] == ["token", "token"]
    assert "".join([c.value for c in chunks if c.type == "token"]) == "heythere"

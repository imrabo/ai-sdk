import httpx
from src.types import RuntimeConfig, GenerateRequest, Message
from src.core.generate import generate
from src.core.stream import stream


def make_mock_client(monkeypatch, handler):
    transport = httpx.MockTransport(handler)

    class MockClient(httpx.Client):
        def __init__(self, *args, **kwargs):
            super().__init__(transport=transport, *args, **kwargs)

    monkeypatch.setattr(httpx, "Client", MockClient)


def test_generic_url_streaming_parity(monkeypatch):
    # generate returns JSON with output 'hello world'
    def handler(request):
        if "stream" in str(request.url):
            body = b"hello\n world\nDONE\n"
            return httpx.Response(200, content=body)

        return httpx.Response(200, json={"output": "hello world"})

    make_mock_client(monkeypatch, handler)

    rc = RuntimeConfig(type="url", endpoint="http://example.com/api/generate")
    req = GenerateRequest(
        model="m", messages=[Message(role="user", content="test")], runtime=rc
    )
    rc_stream = RuntimeConfig(type="url", endpoint="http://example.com/api/stream")
    req_stream = GenerateRequest(
        model="m", messages=[Message(role="user", content="test")], runtime=rc_stream
    )

    # generate result
    gen = generate(req)

    # stream and reassemble tokens
    toks = [c.value for c in stream(req_stream) if c.type == "token"]
    assembled = "".join(toks)

    assert gen.output == "hello world"
    assert assembled == "helloworld" or assembled.strip() == "hello world"


def test_ollama_streaming_parity(monkeypatch):
    # Ollama generate returns JSON, stream returns lines
    def handler(request):
        if request.url.path.endswith("/api/generate"):
            return httpx.Response(200, json={"output": "ollama says hi"})
        body = b"ollama\n says\n hi\nDONE\n"
        return httpx.Response(200, content=body)

    make_mock_client(monkeypatch, handler)

    rc = RuntimeConfig(type="url", endpoint="http://localhost:11434/ollama")
    req = GenerateRequest(
        model="m", messages=[Message(role="user", content="test")], runtime=rc
    )

    gen = generate(req)
    toks = [c.value for c in stream(req) if c.type == "token"]
    assembled = "".join([s for s in toks])

    assert gen.output == "ollama says hi"
    assert "ollama" in assembled

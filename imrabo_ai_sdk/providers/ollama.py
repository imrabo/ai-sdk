from typing import Iterable
from ..types import Provider, InternalRequest, GenerateResult, StreamChunk, Capabilities
from ..transport.http import post_json, post_stream


class OllamaProvider(Provider):
    def __init__(
        self, endpoint: str = "http://localhost:11434", headers: dict | None = None
    ):
        self.id = "ollama"
        self.endpoint = endpoint
        self.headers = headers or {}

    def capabilities(self) -> Capabilities:
        # Ollama supports streaming and JSON models by design in this integration
        return Capabilities(streaming=True, tools=False, json=True, max_tokens=None)

    def generate(self, req: InternalRequest) -> GenerateResult:
        payload = {
            "model": req.model,
            "messages": [{"role": m.role, "content": m.content} for m in req.messages],
        }
        resp = post_json(
            f"{self.endpoint}/api/generate",
            headers=self.headers,
            json=payload,
            timeout=None,
        )
        output = resp.get("output") or resp.get("text") or ""
        return GenerateResult(output=str(output), tokens=None, metadata=resp)

    def stream(self, req: InternalRequest) -> Iterable[StreamChunk]:
        payload = {
            "model": req.model,
            "messages": [{"role": m.role, "content": m.content} for m in req.messages],
            "stream": True,
        }
        for raw in post_stream(
            f"{self.endpoint}/api/stream",
            headers=self.headers,
            json=payload,
            timeout=None,
        ):
            try:
                text = raw.decode("utf-8")
            except Exception:
                text = ""
            for line in text.splitlines():
                if line.strip().upper() == "DONE":
                    yield StreamChunk(type="done")
                else:
                    yield StreamChunk(type="token", value=line)
        yield StreamChunk(type="done")

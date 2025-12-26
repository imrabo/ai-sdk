from typing import Iterable
from ..types import (
    Provider,
    InternalRequest,
    GenerateResult,
    StreamChunk,
    Capabilities,
)
from ..transport.http import post_json, post_stream


class GenericURLProvider(Provider):
    def __init__(self, id: str, endpoint: str, headers: dict | None = None):
        self.id = id
        self.endpoint = endpoint
        self.headers = headers

    def capabilities(self) -> Capabilities:
        return Capabilities(streaming=True, tools=False, json=False)

    def generate(self, req: InternalRequest) -> GenerateResult:
        payload = {
            "model": req.model,
            "messages": [{"role": m.role, "content": m.content} for m in req.messages],
        }
        resp = post_json(
            self.endpoint, headers=self.headers, json=payload, timeout=None
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
            self.endpoint, headers=self.headers, json=payload, timeout=None
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

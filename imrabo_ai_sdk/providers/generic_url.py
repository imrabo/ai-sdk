from typing import Iterable, Dict
from ..types import Provider, InternalRequest, GenerateResult, StreamChunk, Capabilities
from ..transport.http import post_json, post_stream


class GenericURLProvider(Provider):
    def __init__(
        self,
        id: str,
        endpoint: str,
        headers: Dict[str, str] | None = None,
        supports_streaming: bool = True,
    ):
        self.id = id
        self.endpoint = endpoint
        self.headers = headers or {}
        self._supports_streaming = supports_streaming

    def capabilities(self) -> Capabilities:
        return Capabilities(
            streaming=self._supports_streaming, tools=False, json=True, max_tokens=None
        )

    def generate(self, req: InternalRequest) -> GenerateResult:
        # Minimal envelope for a generic server. Providers adapt as needed.
        payload = {
            "model": req.model,
            "messages": [{"role": m.role, "content": m.content} for m in req.messages],
            "options": {
                "max_tokens": req.options.max_tokens if req.options else None,
                "temperature": req.options.temperature if req.options else None,
                "top_p": req.options.top_p if req.options else None,
                "stop": req.options.stop if req.options else None,
            },
        }

        # Try a few common generate endpoints to account for endpoint roots
        endpoints_to_try = [
            self.endpoint,
            f"{self.endpoint.rstrip('/')}/api/generate",
            f"{self.endpoint.rstrip('/')}/generate",
        ]
        last_exc = None
        for ep in endpoints_to_try:
            try:
                resp = post_json(ep, headers=self.headers, json=payload, timeout=None)
                # Expecting a minimal JSON response with an "output" field
                output = (
                    resp.get("output") or resp.get("text") or resp.get("result") or ""
                )
                return GenerateResult(output=str(output), tokens=None, metadata=resp)
            except Exception as e:
                last_exc = e
                continue

        # If all attempts failed, raise the last error
        raise RuntimeError("generic provider failed to generate") from last_exc

    def stream(self, req: InternalRequest) -> Iterable[StreamChunk]:
        if not self._supports_streaming:
            raise RuntimeError("streaming not supported")

        payload = {
            "model": req.model,
            "messages": [{"role": m.role, "content": m.content} for m in req.messages],
            "options": {
                "max_tokens": req.options.max_tokens if req.options else None,
                "temperature": req.options.temperature if req.options else None,
                "top_p": req.options.top_p if req.options else None,
                "stop": req.options.stop if req.options else None,
            },
        }

        # Try common stream endpoints if a root endpoint is given
        endpoints_to_try = [
            self.endpoint,
            f"{self.endpoint.rstrip('/')}/api/stream",
            f"{self.endpoint.rstrip('/')}/stream",
        ]

        # Deduplicate while preserving order
        seen = set()
        unique_endpoints = []
        for e in endpoints_to_try:
            if e not in seen:
                seen.add(e)
                unique_endpoints.append(e)

        for ep in unique_endpoints:
            try:
                for raw in post_stream(
                    ep, headers=self.headers, json=payload, timeout=None
                ):
                    try:
                        text = raw.decode("utf-8")
                    except Exception:
                        text = ""

                    # Split lines — each non-empty line is treated as a token emission
                    for line in text.splitlines():
                        # Special DONE marker allowed
                        if line.strip().upper() == "DONE":
                            yield StreamChunk(type="done")
                        else:
                            yield StreamChunk(type="token", value=line)

                # Successful endpoint processed — stop trying further endpoints
                break
            except Exception:
                # Try next endpoint if present
                continue

        # Ensure done is emitted at the end
        yield StreamChunk(type="done")

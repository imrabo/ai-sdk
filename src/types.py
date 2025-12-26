from dataclasses import dataclass
from typing import Literal, Optional, Protocol, Iterable, Any, List


@dataclass(frozen=True)
class Message:
    role: Literal["system", "user", "assistant"]
    content: str


@dataclass(frozen=True)
class GenerationOptions:
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stop: Optional[List[str]] = None


@dataclass(frozen=True)
class RuntimeConfig:
    type: Literal["url", "kernel"]
    endpoint: Optional[str] = None
    headers: Optional[dict[str, str]] = None
    timeout_ms: Optional[int] = None


@dataclass(frozen=True)
class GenerateRequest:
    model: str
    messages: List[Message]
    runtime: Optional[RuntimeConfig] = None
    tools: Optional[List[Any]] = None  # ToolDefinition: future
    options: Optional[GenerationOptions] = None


@dataclass(frozen=True)
class GenerateResult:
    output: str
    tokens: Optional[int] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass(frozen=True)
class StreamChunk:
    type: Literal["token", "tool_call", "done", "error"]
    value: Optional[Any] = None


@dataclass(frozen=True)
class Capabilities:
    streaming: bool
    tools: bool
    json: bool
    max_tokens: Optional[int] = None


@dataclass(frozen=True)
class InternalRequest:
    model: str
    messages: List[Message]
    tools: Optional[List[Any]] = None
    options: Optional[GenerationOptions] = None


# Provider protocol — the extension surface
class Provider(Protocol):
    id: str

    def capabilities(self) -> Capabilities: ...

    def generate(self, req: InternalRequest) -> GenerateResult: ...

    def stream(self, req: InternalRequest) -> Iterable[StreamChunk]: ...

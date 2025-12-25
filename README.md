imrabo AI SDK (Python)

imrabo AI SDK v1 is a **provider-agnostic invocation layer** for AI models. It exposes a tiny, stable public API intended to be durable and unopinionated.

Public API

- `generate(request: GenerateRequest) -> GenerateResult`
- `stream(request: GenerateRequest) -> Iterable[StreamChunk]`

Quick usage example

```python
from imrabo_ai_sdk import generate, stream
from imrabo_ai_sdk.types import GenerateRequest, Message, RuntimeConfig

req = GenerateRequest(
    model='gpt-xyz',
    messages=[Message(role='user', content='Hello')],
    runtime=RuntimeConfig(type='url', endpoint='http://example.com')
)

res = generate(req)
print(res.output)

# Streaming example
for chunk in stream(req):
    if chunk.type == 'token':
        print(chunk.value, end='')
    elif chunk.type == 'done':
        print('\n-- done --')
```

Documentation

- `docs/sdk_principles.md` — design principles & non-goals
- `docs/sdk_contract.md` — formal API contract and conformance
- `docs/provider_adapters.md` — how to implement a provider

License & Versioning

This SDK is designed for **additive-only evolution**. Any breaking change requires a v2 and a migration path.

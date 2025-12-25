# imrabo AI SDK — SDK Contract (Python)

This document is the authoritative specification for the Python SDK implementation. It mirrors the locked design and includes the public API, types, streaming model, error model, conformance tests, and provider contract.

(See repository `docs/` for the canonical spec used for implementation and tests.)

Public API

- generate(request: GenerateRequest) -> GenerateResult
- stream(request: GenerateRequest) -> Iterable[StreamChunk]

Streaming model

- Tokens emitted as `StreamChunk(type='token', value=...')`
- `done` chunk emitted at end
- Errors raised or streamed as `StreamChunk(type='error')` where applicable

Provider adapter rules

- Providers implement the `Provider` Protocol in `imrabo_ai_sdk.types`
- Providers must be stateless and not mutate requests
- Capabilities must be declared and enforced by the core

Error model

- SDKValidationError
- UnsupportedCapabilityError
- ProviderError
- TransportError
- TimeoutError

Conformance tests

- Core validation tests (message roles, generation options)
- Streaming tests (token order, done, errors)
- Provider tests (mock transport)
- Integration parity tests

This file exists to assist reviewers and implementers; it should be kept in sync with `docs/sdk_principles.md` and `docs/provider_adapters.md`.

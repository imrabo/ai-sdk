# Usage

This page collects examples, best practices and notes about using the SDK.

- Public functions: `generate(request: GenerateRequest) -> GenerateResult`, `stream(request: GenerateRequest) -> Iterable[StreamChunk]`
- Always validate your runtime and model values before calling the SDK.
- If you request streaming but your runtime/provider does not support streaming, the SDK raises `UnsupportedCapabilityError`.

Refer to `docs/sdk_contract.md` for full type definitions and examples.

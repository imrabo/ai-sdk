# Provider Adapter Guidelines

This document explains how to implement a provider adapter for the imrabo AI SDK.

Requirements:
- Implement the `Provider` protocol from `imrabo_ai_sdk.types`.
- Declare explicit `Capabilities`.
- Do not mutate `InternalRequest`.
- Do not hold persistent state, do not import other providers.
- Streaming must follow the `StreamChunk` semantics.

Anti-patterns:
- Adding provider-specific flags to public types.
- Swallowing errors or retrying silently.
- Performing filesystem or process management.

Kernel Provider:
- Kernel provider is a stub in v1. It MUST raise NotImplementedError for both `generate` and `stream`.
- Kernel providers are optional and intended for future local execution support; they are not special-cased by the core.

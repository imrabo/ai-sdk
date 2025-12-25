# imrabo-ai-sdk — SDK Contract (Formal Spec)

> Locked specification for the imrabo AI SDK public API, extension surfaces, provider contract, and conformance tests. This document is the canonical source for implementers and reviewers.

---

## 0. Purpose & Scope 🔒

This document defines the *API contract* for the imrabo AI SDK. The SDK is a provider-agnostic invocation layer that exposes a single stable surface for calling AI models (local or remote) and does not own execution.

Non-goals (explicit): runtime management, process management, agent frameworks, memory and persistence, UI, or CLIs. The SDK is purely an invocation and normalization layer.

---

## 1. High-level Principles (referenced in `docs/sdk-principles.md`) ✅

- Invocation over execution
- Capabilities over promises
- Streaming first
- URL-first, kernel-second
- Adapters adapt — core never bends
- Additive evolution only

These rules are normative and must be enforced by validation and tests.

---

## 2. Public API (v1) — The Product Surface ✨

### 2.1 Entry Points

The SDK exposes exactly these two public operations:

```ts
// core/generate.ts
export function generate(request: GenerateRequest): Promise<GenerateResult>

// core/stream.ts
export function stream(request: GenerateRequest): AsyncIterable<StreamChunk>
```

No additional helpers, provider-specific shims, or sugar functions are part of the public v1 surface.

### 2.2 Types — Public (frozen)

```ts
interface GenerateRequest {
  model: string
  messages: Message[]

  runtime?: RuntimeConfig
  tools?: ToolDefinition[]
  options?: GenerationOptions
}

interface Message {
  role: 'system' | 'user' | 'assistant'
  content: string
}

interface RuntimeConfig {
  type: 'url' | 'kernel'
  endpoint?: string        // http(s)://... (required for type=url)
  headers?: Record<string, string>
  timeoutMs?: number
}

interface GenerationOptions {
  maxTokens?: number
  temperature?: number
  topP?: number
  stop?: string[]
}

interface GenerateResult {
  output: string
  tokens?: number
  metadata?: Record<string, any>
}
```

Rules: no provider-specific fields allowed in these interfaces. Default values are not implied by the SDK — callers must supply explicit choices where needed.

---

## 3. Streaming Model (non-negotiable) ⚡️

Streaming is a first-class mode. The public `stream` operation returns an AsyncIterable of StreamChunk:

```ts
interface StreamChunk {
  type: 'token' | 'tool_call' | 'done' | 'error'
  value?: string | ToolCall
}
```

Rules:
- Tokens must arrive incrementally in the order they are generated.
- Providers that cannot stream must set `capabilities().streaming === false`.
- If a caller requests streaming but the resolved provider reports streaming=false, the SDK must throw `UnsupportedCapabilityError` (no silent downgrade).
- `done` is sent once when generation is complete; `error` may be emitted as the final chunk for streaming errors.
- Tool interactions (if supported) are flagged via `tool_call` chunk type.

Note: The SDK does not standardize wire-level SSE vs chunked vs websocket — that is a provider implementation detail. The provider must expose streaming semantics through the `stream` method defined in the provider contract.

---

## 4. Capabilities System (contract)

```ts
interface Capabilities {
  streaming: boolean
  tools: boolean
  json: boolean
  maxTokens?: number
}
```

Enforcement rules:
- The SDK checks `provider.capabilities()` prior to execution.
- If the request asks for a feature not supported by the provider (e.g., `tools` or streaming), the SDK throws `UnsupportedCapabilityError` with deterministic messaging.
- Capability checks are deterministic and must be exercised early.

---

## 5. Provider Adapter Contract (ONLY extension point) 🔌

```ts
interface Provider {
  id: string

  capabilities(): Capabilities

  generate(req: InternalRequest): Promise<GenerateResult>

  stream(req: InternalRequest): AsyncIterable<StreamChunk>
}
```

Hard rules for providers:
- A provider must be a pure implementation: no side effects, no internal persistent state, and no importing other providers.
- Providers MUST NOT mutate incoming requests; SDK sends a normalized InternalRequest.
- Providers must not swallow or transform errors silently; they must raise typed errors as specified.
- Providers must not perform automatic retries unless explicitly exposed by configuration (and such behavior must be transparent to the SDK and tests).

Provider Registration:
- Providers are registered in `providers/index.ts` and loaded by `config/resolveProvider.ts` using deterministic rules (e.g., `runtime.type` and `runtime.endpoint` for url types).

---

## 6. Internal Request Normalization and Validation ✅

Public requests are normalized into `InternalRequest` before being passed to providers.

```ts
interface InternalRequest {
  model: string
  messages: Message[]
  tools?: ToolDefinition[]
  options?: GenerationOptions
}
```

Normalizer responsibilities:
- Validate message ordering and role values.
- Enforce or check `options.maxTokens` against provider `capabilities().maxTokens` if present.
- Reject unsupported combinations (e.g., tools requested when provider has tools=false).
- Produce deterministic, immutable InternalRequest objects for providers to consume.

All validation errors raised here are `SDKValidationError` with deterministic messages and error codes for programmatic handling.

---

## 7. Error Model (typed & deterministic) 🚨

Error types (exported):
- `SDKValidationError`
- `UnsupportedCapabilityError`
- `ProviderError`
- `TransportError`
- `TimeoutError`

Guidelines:
- All errors must contain a machine-friendly `code` string and a deterministic human message.
- Providers should wrap provider-specific errors in `ProviderError` with a consistent shape: `{ code, message, providerId, details? }`.
- SDK must never swallow or obfuscate provider errors.

Example error object:
```json
{
  "name": "UnsupportedCapabilityError",
  "code": "streaming_not_supported",
  "message": "Provider 'foo' does not support streaming",
  "provider": "foo"
}
```

---

## 8. Internal Architecture & Import Rules 🏗️

Minimal structure (implementation folder names are normative):
```
core/
  generate.ts
  stream.ts
  validate.ts
  normalize.ts
  capabilities.ts
  errors.ts
providers/
  generic_url.ts  // MUST be first
  ollama.ts
  kernel.ts       // later
  index.ts
transport/
  http.ts
  streaming.ts
config/
  resolveProvider.ts
docs/
  sdk-contract.md
```

Import rules:
- `core` must not import from `providers`.
- `providers` may depend on `transport` but not on `core` or other providers.
- `transport` must not contain SDK logic; it's focused on HTTP and streaming primitives.

Violation of these rules is considered an architectural bug.

---

## 9. Provider Implementation Order (recommended)

Phase 1 — **Generic URL Provider (MANDATORY FIRST)**
- Implement `providers/generic_url.ts` that supports an opinionated mapping to common HTTP AI endpoints (OpenAI-compatible, OpenCode-style, Ollama-style). This demonstrates the correctness of the adapter contract.

Phase 2 — **Ollama Provider**
- Thin implementation with streaming-first semantics and compatibility tests against the local Ollama server.

Phase 3 — **Kernel Provider (optional)**
- Local kernel adapter; only after core has stabilized.

---

## 10. Conformance Tests & Acceptance Criteria ✅

A provider is conformant when it passes both unit and integration tests. Minimum test cases:

Public contract tests (core):
- `generate()` rejects invalid message sequences and role values (SDKValidationError).
- `stream()` throws `UnsupportedCapabilityError` when provider.streaming === false.
- Normalization enforces token limits when capability declares `maxTokens`.
- Error types and codes are preserved through the stack.

Provider tests (generic URL & Ollama):
- Provider.capabilities() returns correct capabilities for the configured runtime.
- `stream()` yields `token` chunks incrementally for streaming endpoints.
- `generate()` returns same final text as streamed `done` concatenation.
- `tool_call` chunks appear when a provider supports tools and the model emits a tool invocation.

Integration tests:
- Switch runtime between Ollama/OpenAI/URL via `RuntimeConfig` only and verify identical API behavior.
- Streaming parity tests: ensure `generate()` and `stream()` produce consistent outputs and metadata.

Acceptance criteria (same as Completion Criteria in the design document):
1. User can swap providers via configuration only.
2. Streaming works identically across providers.
3. Unsupported features fail loudly.
4. No daemon required.
5. CLI can be built on top of the SDK without modifying providers.

---

## 11. Versioning & Compatibility Policy

- v1 is additive-only. Fields cannot be renamed or reinterpreted in v1.
- Any breaking changes require a v2 with an explicit migration plan.
- Tests must be written that assert backwards compatibility for minor releases.

---

## 12. Security & Privacy Notes 🔐

- The SDK itself makes no assumptions about model safety or content moderation. Those are the caller's responsibility.
- Providers must not leak local secrets in error messages or metadata. Providers should sanitize headers and sensitive values before including them in logs or errors.

---

## 13. Documentation & Onboarding

- `docs/sdk-principles.md` contains the frozen principles (copy the list from the design doc).
- `docs/sdk-contract.md` (this file) is the official spec and is authoritative for reviewers and implementers.
- Add a small `examples/` folder with minimal `generate` and `stream` examples for each provider.

---

## 14. Conformance Checklist (quick) ✅

- [ ] `generate` and `stream` implemented
- [ ] Normalizer validates messages and roles
- [ ] Capabilities checked before provider invocation
- [ ] Provider contract documented and enforced in tests
- [ ] Streaming parity tests present
- [ ] Error types present and deterministic
- [ ] `docs/sdk-principles.md` authored

---

## 15. Final Lock Statement

> The SDK is a contract, not a product feature. It must be boring, strict, and predictable. Breaking these rules requires a documented migration path and a v2.

---

*End of spec.*

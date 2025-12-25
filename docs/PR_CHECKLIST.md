# PR Review Checklist — imrabo AI SDK

Use this checklist for every PR touching `src/` or `docs/`.

- ✅ **Public API unchanged** — No renames or semantic changes to `generate` / `stream` / types in `imrabo_ai_sdk.types`.
- ✅ **No provider logic in core** — `imrabo_ai_sdk/core/*` must not import `providers`.
- ✅ **Capabilities enforced** — All places that invoke providers must validate capabilities first.
- ✅ **Streaming parity** — Streaming behavior must be tested; providers must stream tokens incrementally.
- ✅ **No TODOs in src/** — Remove any TODO/FIXME from source files before merge.
- ✅ **Typed errors** — Errors must be one of the typed SDK errors and deterministic.
- ✅ **Tests added/updated** — New behavior must be covered by deterministic tests.
- ✅ **Docs updated** — Update `docs/` if any public behavior changes.
- ✅ **No forbidden concepts** — Ensure PR does not introduce agents, storage, vector DBs, process management, CLI, UI, or editor hooks.

If all checks pass, the PR is approved for merge.

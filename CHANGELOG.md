# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-12-26
### Added
- Initial implementation of imrabo AI SDK v1 (Python)
  - Public API: `generate` and `stream`
  - Core validation, normalization, capabilities enforcement
  - Providers: Generic URL (full), Ollama (full), Kernel (stub)
  - Transport layer with streaming support using httpx
  - Tests: unit, provider, and integration streaming parity tests
  - Documentation: SDK principles, contract, provider adapters
  - CI: GitHub Actions for lint and tests


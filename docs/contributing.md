# Contributing

Thanks for considering contributing. A few project rules to follow:

- Keep the SDK small and boring: do not add execution, agents, persistence, or CLI logic.
- Do not add provider-specific flags to public types.
- Validate capabilities before invocation and add tests for capability enforcement.
- Core (under `imrabo_ai_sdk/core`) must not import `providers`.
- Add tests and update docs for any public change.

Run tests and lint locally:

```bash
python -m pip install -e .[docs]
python -m pip install -r requirements-dev.txt  # if present
python -m ruff check .
python -m pytest
```

Before creating a release see `RELEASE.md` and ensure the CHANGELOG and docs are updated.

Release checklist — imrabo AI SDK

Before creating a release/tag:

1. Ensure all tests pass locally and in CI (`pytest` and `ruff`) ✅
2. Bump version in `pyproject.toml` (if not already set) ✅
3. Update `CHANGELOG.md` with release notes ✅
4. Create a signed Git tag `vX.Y.Z` and push tag to remote ✅
5. Create GitHub Release referencing the tag and paste changelog notes ✅
6. Publish package to PyPI (use `twine` or GitHub Actions) — ensure credentials are set and package name `imrabo-ai-sdk` available ✅
7. Add release notes and update `README.md` if necessary ✅

Automated steps that may be implemented later:
- GitHub Actions release workflow to build and upload wheels and sdists on tag
- Automated CHANGELOG generation from merge commits (optional)

Notes:
- Releases must be additive for v1 (no breaking changes). Any breaking change must be v2.
- Ensure LICENSE file is included in distribution.

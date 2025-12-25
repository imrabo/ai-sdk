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

GitHub Actions release workflow behavior
- On push of a tag matching `v*.*.*` the workflow will build distributions and **create a draft GitHub Release** with the `dist/` artifacts attached.
- The workflow will only upload to PyPI automatically if the repository secret `PYPI_API_TOKEN` is set. If the secret is not present, the PyPI upload is skipped and a draft GitHub Release with artifacts is still created.

Troubleshooting GitHub Pages / docs deploy
- If the docs workflow fails with `Permission to <owner>/<repo>.git denied to github-actions[bot]`:
  - Ensure the docs workflow has `permissions: contents: write` and `pages: write` (we set this in `.github/workflows/docs.yml`).
  - Make sure `actions/checkout` uses `persist-credentials: true` (the workflow now sets this) so the `GITHUB_TOKEN` can push commits.
  - If you have branch protection rules on `gh-pages`, allow GitHub Actions to push to protected branches or use a different publishing strategy (e.g., publish via a deploy key or a personal token).
- If the workflow fails with `Version 3.1 was not found` from `actions/setup-python`: pin a concrete Python minor version like `3.11` in the workflow (we now use `3.11`).

Publishing to PyPI via "Release published"
- There is now an **Upload Python Package on Release** workflow (`.github/workflows/upload-to-pypi-on-release.yml`) that will run when a GitHub Release is **published** (`type: published`).
- Behavior:
  - It builds `dist/` and uploads the distributions to a job-scoped artifact.
  - It then downloads those artifacts in a separate job and uses `pypa/gh-action-pypi-publish` to publish the package to PyPI.
  - The `pypi` environment is configured for the publishing job; we recommend protecting that environment and requiring approvals before allowing the job to run.
  - The workflow will **fail early with a clear error** if the environment secret `PYPI_API_TOKEN` is not configured — this prevents silent publish attempts.

How to create the protected `pypi` environment and add the token
1. Go to your repository → Settings → Environments → New environment, and create an environment named `pypi`.
2. Under the `pypi` environment, add a new secret named `PYPI_API_TOKEN` with the value of your PyPI API token (create one at https://pypi.org/ if you don't have one).
3. Configure environment protection rules (optional but recommended): require reviewers or approvals before deployment.
4. When you publish a GitHub Release and the job reaches the `pypi` environment, an approval will be required; after approval the workflow will use the `PYPI_API_TOKEN` secret to publish the package.

Notes:
- Releases must be additive for v1 (no breaking changes). Any breaking change must be v2.
- Ensure LICENSE file is included in distribution.
Notes:
- Releases must be additive for v1 (no breaking changes). Any breaking change must be v2.
- Ensure LICENSE file is included in distribution.

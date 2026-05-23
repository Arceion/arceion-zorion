# Releasing arceion-zorion to PyPI

This guide explains how to release arceion-zorion to PyPI using GitHub Actions workflows.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Release Process](#release-process)
4. [Testing on TestPyPI](#testing-on-testpypi)
5. [Production Release](#production-release)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- Push access to the GitHub repository
- PyPI account(s) at [pypi.org](https://pypi.org) and optionally [test.pypi.org](https://test.pypi.org)
- PyPI API tokens (generated from your account settings)

**⚠️ NOTE:** See [.PUBLISH_SETUP.md](./.PUBLISH_SETUP.md) for detailed authentication setup (API tokens vs Trusted Publishers)

## Setup

### Step 1: Generate PyPI API Tokens

1. Go to [PyPI Account Settings → API tokens](https://pypi.org/manage/account/tokens/)
2. Create a new token:
   - **Name:** `arceion-zorion-github-actions`
   - **Scope:** "Entire account" or "Project: arceion-zorion" (if available)
   - **Copy the token** (you can only see it once)

3. Repeat for [TestPyPI](https://test.pypi.org/manage/account/tokens/) if testing

### Step 2: Add GitHub Secrets

1. Go to your repository → **Settings → Secrets and variables → Actions**
2. Create new repository secrets:

   **For Production PyPI:**
   - **Name:** `PYPI_API_TOKEN`
   - **Value:** Your PyPI API token

   **For TestPyPI (optional, for testing):**
   - **Name:** `TEST_PYPI_API_TOKEN`
   - **Value:** Your TestPyPI API token

### Step 3: Update Version Number

Edit `pyproject.toml` and update the version field:

```toml
[project]
name = "arceion-zorion"
version = "0.1.0"  # Update this to match your release
```

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 0.1.0)
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

## Release Process

### Option 1: Release via GitHub (Recommended)

This is the easiest method and triggers the publish workflow automatically.

#### Step 1: Commit Version Update

```bash
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
git push origin main
```

#### Step 2: Create a Release on GitHub

1. Go to your repository → **Releases → Draft a new release**
2. Click "Choose a tag" and enter your version: `v0.2.0`
3. Click "+ Create new tag on publish"
4. Fill in release details:
   - **Title:** `Release v0.2.0`
   - **Description:** Add changelog and highlights
5. Click "Publish release"

The workflow will automatically:
- ✅ Run tests
- ✅ Build distributions
- ✅ Publish to PyPI
- ✅ Attach artifacts to the release

### Option 2: Manual Test Release on TestPyPI

Use this to validate before publishing to production.

#### Step 1: Trigger Manual Workflow

1. Go to repository → **Actions → Publish to PyPI**
2. Click "Run workflow"
3. Select `testpypi` from the dropdown
4. Click "Run workflow"

#### Step 2: Monitor the Build

The workflow runs in stages:
1. **Test** → Runs pytest
2. **Build** → Builds distribution
3. **Publish** → Uploads to TestPyPI

Check the workflow run for any errors. If all pass, you can proceed to production.

#### Step 3: Test Installation from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ arceion-zorion==0.2.0
```

Verify the package works as expected.

### Option 3: Production Release via Manual Workflow

If you need to manually publish to production:

1. Update `pyproject.toml` with new version
2. Commit and push
3. Go to repository → **Actions → Publish to PyPI**
4. Click "Run workflow"
5. Select `pypi` from the dropdown
6. Click "Run workflow"

## Testing on TestPyPI

### Why Test?

TestPyPI is a safe sandbox to validate:
- Package metadata is correct
- Distribution files are valid
- Installation works
- No breaking changes
- Dependencies resolve correctly

### Workflow

```bash
# 1. Test locally first
pip install -e ".[dev]"
pytest

# 2. Trigger TestPyPI build via manual workflow (see Option 2 above)

# 3. Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ arceion-zorion==X.Y.Z

# 4. Verify functionality
python -c "import arceion.zorion; print(arceion.zorion.__version__)"

# 5. If satisfied, create GitHub release for production PyPI
```

## Production Release

### Prerequisites

- ✅ Version bumped in `pyproject.toml`
- ✅ All tests passing
- ✅ Successfully tested on TestPyPI (if recommended)
- ✅ Changelog reviewed
- ✅ Commit pushed to main/master

### Create Release

1. Go to repository → **Releases → Draft a new release**
2. Click "Choose a tag" and create: `v0.2.0` (matches pyproject.toml version)
3. Add release notes (what changed, who should update, any migration notes)
4. Click "Publish release"

The `publish.yml` workflow will:
- ✅ Run all tests
- ✅ Build wheel and source distributions
- ✅ Validate metadata with `twine check`
- ✅ Upload to PyPI
- ✅ Attach distribution files to the release

### Verify Publication

```bash
# Check PyPI
curl -s https://pypi.org/pypi/arceion-zorion/json | python -m json.tool

# Install from PyPI
pip install arceion-zorion==0.2.0

# Verify
python -c "import arceion.zorion; print('✓ Installed successfully')"
```

## Troubleshooting

### "Error: Invalid token"

**Issue:** PYPI_API_TOKEN secret is incorrect or expired

**Solution:**
1. Go to [pypi.org/manage/account/tokens/](https://pypi.org/manage/account/tokens/)
2. Delete the old token
3. Generate a new token
4. Update the GitHub secret with the new value
5. Retry the release

### "400 Bad Request: The name 'arceion-zorion' is not available"

**Issue:** Package name already taken on PyPI

**Solution:**
- Check if package exists: `pip search arceion-zorion` or visit pypi.org
- Change package name in `pyproject.toml` if needed
- Ensure `[project]` section has `name = "arceion-zorion"`

### "409 File already exists"

**Issue:** Trying to publish a version that already exists

**Solution:**
- Increment version in `pyproject.toml` (e.g., 0.1.0 → 0.1.1)
- Commit, push, and retry
- Each version can only be published once (PyPI doesn't allow overwriting)

### "FAILED: twine check dist/*"

**Issue:** Package metadata is invalid

**Solution:**
1. Check `pyproject.toml` for syntax errors
2. Verify required fields: `name`, `version`, `description`
3. Check long description is valid reStructuredText (README.md should be parsed)
4. Run locally: `python -m build && twine check dist/*`

### Workflow Shows "No tests found"

**Issue:** Test discovery failed

**Solution:**
```bash
# Verify test structure
ls -R arceion/zorion/tests/

# Should see: __init__.py, test_*.py files

# Run locally to debug
pytest arceion/zorion/tests/ -v
```

### "ModuleNotFoundError" during tests

**Issue:** Dependencies not installed in workflow

**Solution:**
- Check `pip install -e ".[dev]"` succeeds locally
- Verify `pyproject.toml` has `[project.optional-dependencies]` section with `dev` group
- Include all test dependencies

## Rollback

If you accidentally published a broken version:

1. **Immediate:** Users can downgrade to previous version
   ```bash
   pip install arceion-zorion==0.1.0
   ```

2. **Mark as Yanked:** Go to PyPI Package Settings → Delete/Yank the version
   - PyPI will show "This version is yanked"
   - Users will be warned when installing
   - Pip won't auto-install yanked versions

3. **Release Patch:** For critical bugs
   - Fix the code
   - Bump patch version (0.1.1 → 0.1.2)
   - Release immediately

## Version Numbering

Follow [PEP 440](https://www.python.org/dev/peps/pep-0440/) and [Semantic Versioning](https://semver.org/):

| Change | Version | Example |
|--------|---------|---------|
| Breaking changes | MAJOR | 0.1.0 → 1.0.0 |
| New features | MINOR | 0.1.0 → 0.2.0 |
| Bug fixes | PATCH | 0.1.0 → 0.1.1 |
| Pre-release | alpha/beta/rc | 0.2.0a1, 0.2.0rc1 |

## Best Practices

1. **Always test on TestPyPI first** for major releases
2. **Update CHANGELOG.md** with release notes
3. **Tag releases** in git: `git tag -a v0.2.0 -m "Release 0.2.0"`
4. **Use semantic versioning** for clarity
5. **Keep secrets safe** — never commit tokens or API keys
6. **Document breaking changes** in release notes
7. **Run tests locally** before releasing
8. **Review dependency versions** before releasing

## References

- [PyPI Help](https://pypi.org/help/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
- [PEP 440 — Version Identification](https://www.python.org/dev/peps/pep-0440/)

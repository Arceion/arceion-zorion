# PyPI API Token Setup - Quick Start

Follow these steps to set up API token authentication for publishing to PyPI.

## Step 1: Generate PyPI API Token ⚙️

1. **Go to PyPI:**
   - Visit: https://pypi.org/manage/account/tokens/

2. **Click "Add API token"**

3. **Fill in the token details:**
   - **Name:** `arceion-zorion-github`
   - **Scope:** Select "Entire account"
   - Click **"Create token"**

4. **Copy the token immediately** (you'll only see it once!)
   - It will look like: `pypi-AgEIcHlwaS5vcmc...`

✅ Keep this token safe for Step 2!

---

## Step 2: Add Token to GitHub Secrets 🔐

1. **Go to your GitHub repository:**
   - URL: `https://github.com/Arceion/arceion-zorion`

2. **Navigate to Secrets:**
   - Click **Settings** tab
   - Left sidebar: **Secrets and variables** → **Actions**

3. **Create repository secret:**
   - Click **"New repository secret"** button

4. **Enter secret details:**
   - **Name:** `PYPI_API_TOKEN`
   - **Value:** Paste your token from Step 1
   - Click **"Add secret"**

✅ Token is now safely stored in GitHub!

---

## Step 3: Verify Setup ✓

The workflow is already configured to use your token:

```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}  # Uses your token
```

No additional workflow changes needed!

---

## Step 4: Test on TestPyPI (Optional but Recommended) 🧪

Before releasing to production, test on TestPyPI:

1. **Go to TestPyPI:**
   - Visit: https://test.pypi.org/manage/account/tokens/
   - Repeat Steps 1-2 above (create token, add as `TEST_PYPI_API_TOKEN`)

2. **Run test workflow:**
   - Go to your GitHub repo → **Actions** tab
   - Click **"Publish to PyPI"** workflow
   - Click **"Run workflow"** button
   - Select dropdown: `testpypi`
   - Click **"Run workflow"**

3. **Monitor the run:**
   - Wait for job to complete
   - Should succeed with message: "Publishing distributions to test.pypi.org"

4. **Test the installation:**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ arceion-zorion==0.1.0
   ```
   Should install successfully!

✅ If test passes, you're ready for production!

---

## Step 5: Release to Production 🚀

1. **Update version in `pyproject.toml`:**
   ```toml
   [project]
   version = "0.2.0"  # Change from 0.1.0
   ```

2. **Commit and push:**
   ```bash
   git add pyproject.toml
   git commit -m "chore: bump version to 0.2.0"
   git push origin master
   ```

3. **Create GitHub Release:**
   - Go to GitHub repo → **Releases** tab
   - Click **"Draft a new release"**
   - **Tag version:** `v0.2.0` (matches pyproject.toml)
   - **Release title:** `Release v0.2.0`
   - **Description:** Add changelog/highlights
   - Click **"Publish release"**

✅ Workflow automatically publishes to PyPI!

4. **Verify publication:**
   ```bash
   pip install arceion-zorion==0.2.0
   python -c "import arceion.zorion; print('✓ Published!')"
   ```

---

## Troubleshooting

### ❌ "invalid-publisher" error
**Cause:** Token not added to GitHub secrets

**Fix:**
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Check that `PYPI_API_TOKEN` secret exists
3. Verify the secret value is your PyPI token (not empty)

### ❌ "Unauthorized: Invalid authentication"
**Cause:** Token is invalid or expired

**Fix:**
1. Go to https://pypi.org/manage/account/tokens/
2. Find your token in the list
3. If expired, click **"Revoke"** and create new token
4. Update GitHub secret with new token

### ❌ "This package name is taken"
**Cause:** Someone else already published `arceion-zorion` to PyPI

**Fix:**
- Check https://pypi.org/project/arceion-zorion/
- If it's your package, you should own it
- If not, change the package name in `pyproject.toml` and retry

### ❌ Workflow shows pending but never runs
**Cause:** GitHub can't pull artifact from previous job

**Fix:**
1. Go to **Actions** tab
2. Find the failed workflow run
3. Click it and check build job logs
4. Fix any build errors
5. Retry the workflow

---

## Security Notes 🔒

✅ **Your token is safe because:**
- It's stored in GitHub's encrypted secrets vault
- Only visible to you and authorized workflows
- Never appears in logs or output
- Can be revoked anytime on PyPI

✅ **Best practices:**
- Create separate tokens for different use cases
- Use "Entire account" scope only if needed
- Revoke tokens you don't use anymore
- Rotate tokens periodically

---

## Next Steps

1. ✅ Generate PyPI API token (Step 1)
2. ✅ Add token to GitHub Secrets (Step 2)
3. ✅ (Optional) Test on TestPyPI (Step 4)
4. ✅ Create GitHub Release to publish (Step 5)

You're ready to publish! 🎉

<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.67

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.67** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): ${{ }} expressions are interpolated directly inside run: shell command strings. In mcp-security-index.yml the 'Publish to gh-pages' step embeds `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` directly in a git remote URL: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. In sync-repo-metadata.yml the 'Update GitHub repo description' step embeds `${{ github.repository }}` directly in a shell command: `gh repo edit "${{ github.repository }}" --description "$desc"`. Any ${{ ... }} expression inside a run: block is substituted by the Actions template engine before the shell ever sees it, enabling injection of shell metacharacters.

Locations:

- `.github/workflows/mcp-security-index.yml:76`
- `.github/workflows/sync-repo-metadata.yml:22`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and the only job (`test`) also has no job-level `permissions:` key. Without explicit permissions the workflow inherits the repository's default token permissions, which may be broader than necessary.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (the job-level block already lists the specific scopes needed: security-events: write, id-token: write, contents: read).

Locations:

- `.github/workflows/scorecard.yml:7`

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions by mutable tags or branch names instead of immutable 40-character commit SHAs, making them vulnerable to supply-chain attacks if the referenced tag is moved or the action is compromised.

cve-watcher.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/cache@v6`, `actions/github-script@v9`.

docker-nightly.yml: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master` (branch ref — especially dangerous), `github/codeql-action/upload-sarif@v4`.

mcp-security-index.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

release.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `pypa/gh-action-pypi-publish@v1.14.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7` (×2), `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`.

sync-rule-count.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/cve-watcher.yml:23`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/mcp-security-index.yml:23`
- `.github/workflows/release.yml:50`
- `.github/workflows/sync-rule-count.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, missing-permissions, broad-permissions, unpinned-uses

**Notes:**

Fixed all four findings:

1. **script-injection**: In mcp-security-index.yml, moved `secrets.GITHUB_TOKEN` and `github.repository` from the git remote URL shell string into an `env:` block, referencing them as `${GITHUB_TOKEN}` and `${GITHUB_REPOSITORY}`. In sync-repo-metadata.yml, moved `github.repository` into an `env:` block and referenced it as `$GITHUB_REPOSITORY` in the shell command.

2. **missing-permissions**: Added `permissions: contents: read` top-level block to ci.yml.

3. **broad-permissions**: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml (the job-level block already has the specific permissions needed: security-events: write, id-token: write, contents: read).

4. **unpinned-uses**: Pinned all actions to full 40-character commit SHAs with tag comments:
   - actions/checkout@v7.0.1 → 3d3c42e5aac5ba805825da76410c181273ba90b1
   - actions/setup-python@v7.0.0 → 5fda3b95a4ea91299a34e894583c3862153e4b97
   - actions/cache@v6 → 55cc8345863c7cc4c66a329aec7e433d2d1c52a9
   - actions/github-script@v9 → 3a2844b7e9c422d3c10d287c895573f7108da1b3
   - docker/setup-buildx-action@v4 → bb05f3f5519dd87d3ba754cc423b652a5edd6d2c
   - docker/login-action@v4 → dbcb813823bdd20940b903addbd779551569679f
   - docker/build-push-action@v7 → 53b7df96c91f9c12dcc8a07bcb9ccacbed38856a
   - aquasecurity/trivy-action@master → 2736533278103862a861f4a35ebac3e97854d956
   - github/codeql-action/upload-sarif@v4 → d1ba80a13dd99fba24a470575428917156a28b43
   - pypa/gh-action-pypi-publish@v1.14.2 → dc37677b2e1c63e2034f94d8a5b11f265b73ba33
   - actions/attest-build-provenance@v4 → 0f67c3f4856b2e3261c31976d6725780e5e4c373
   - sigstore/gh-action-sigstore-python@v3.5.0 → 790bc6befb9d733738f18d8f895854b453640ec9
   - actions/upload-artifact@v7 → 043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
   - actions/download-artifact@v8 → 3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c
   - softprops/action-gh-release@v3 → 3d0d9888cb7fd7b750713d6e236d1fcb99157228


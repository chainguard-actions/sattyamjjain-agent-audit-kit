<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.50

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.50** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of immutable 40-character commit SHAs, making them vulnerable to supply-chain attacks.

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9

docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

release.yml: actions/checkout@v7.0.0 (×3), actions/setup-python@v6.3.0 (×2), pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/docker-nightly.yml:50`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:47`
- `.github/workflows/release.yml:79`
- `.github/workflows/release.yml:113`
- `.github/workflows/sync-rule-count.yml:22`

### permissions (severity: medium)

missing-permissions: ci.yml has no top-level `permissions:` key and the single job also has no `permissions:` key. Without an explicit permissions block the workflow runs with default token permissions, which may include write access to contents and other scopes.

Locations:

- `.github/workflows/ci.yml:1`

### permissions (severity: medium)

broad-permissions: scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all available scopes rather than the minimal set required, violating the principle of least privilege.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): GitHub Actions expressions are interpolated directly inside `run:` shell command strings, allowing template substitution to inject shell metacharacters before the shell parses the command.

1. sync-repo-metadata.yml: `gh repo edit "${{ github.repository }}" --description "$desc"` — the `github.repository` context value is expanded directly into the shell command string.

2. mcp-security-index.yml: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both `secrets.GITHUB_TOKEN` and `github.repository` are interpolated directly into the shell command string in the 'Publish to gh-pages' run block.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:85`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, permissions, script-injection

**Notes:**

Fixed all 4 findings across 7 workflow files:

1. **unpinned-uses**: Pinned all mutable action references to full 40-char commit SHAs with tag comments in cve-watcher.yml (checkout, setup-python, cache, github-script), docker-nightly.yml (checkout, setup-buildx-action, login-action, build-push-action, trivy-action, codeql-action/upload-sarif), mcp-security-index.yml (checkout, setup-python), release.yml (checkout×3, setup-python×2, pypi-publish, setup-buildx-action, login-action, build-push-action×2, trivy-action, attest-build-provenance, sigstore-python, upload-artifact, download-artifact, action-gh-release), and sync-rule-count.yml (checkout, setup-python).

2. **missing-permissions**: Added `permissions: contents: read` top-level block to ci.yml.

3. **broad-permissions**: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml (job-level permissions already provide the specific scopes needed).

4. **script-injection**: (a) sync-repo-metadata.yml: moved `${{ github.repository }}` into env var `REPOSITORY` and referenced as `$REPOSITORY` in shell. (b) mcp-security-index.yml: moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env vars `GITHUB_TOKEN` and `REPOSITORY` and referenced as `${GITHUB_TOKEN}` and `${REPOSITORY}` in shell.


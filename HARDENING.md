<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.57

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.57** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference actions by mutable tags, branch names, or version strings instead of immutable 40-character commit SHAs, making them vulnerable to supply-chain attacks.

- cve-watcher.yml: `actions/checkout@v7.0.0`, `actions/setup-python@v6.3.0`, `actions/cache@v5`, `actions/github-script@v9`
- docker-nightly.yml: `actions/checkout@v7.0.0`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`
- mcp-security-index.yml: `actions/checkout@v7.0.0`, `actions/setup-python@v6.3.0`
- release.yml: `actions/checkout@v7.0.0`, `actions/setup-python@v6.3.0`, `pypa/gh-action-pypi-publish@v1.14.0`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.4.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`
- sync-rule-count.yml: `actions/checkout@v7.0.0`, `actions/setup-python@v6.3.0`

Locations:

- `.github/workflows/cve-watcher.yml:21`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:57`
- `.github/workflows/sync-rule-count.yml:27`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and no job-level `permissions:` key on any of its jobs. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents by default on many repos).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is broader than necessary. Specific minimal permissions should be used instead.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): GitHub Actions expressions are interpolated directly inside `run:` shell command strings, bypassing shell quoting and allowing template-substituted values to be parsed as shell syntax before the shell ever sees them.

1. sync-repo-metadata.yml: `gh repo edit "${{ github.repository }}" --description "$desc"` — `${{ github.repository }}` is expanded by the Actions template engine directly into the shell command string.

2. mcp-security-index.yml: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — `${{ github.repository }}` is expanded directly into the shell command string.

Locations:

- `.github/workflows/sync-repo-metadata.yml:27`
- `.github/workflows/mcp-security-index.yml:74`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four finding types:

1. unpinned-uses: Pinned all action references across cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml to full 40-char commit SHAs. Actions pinned: actions/checkout@9c091bb, actions/setup-python@ece7cb0, actions/cache@caa2961, actions/github-script@3a2844b, docker/setup-buildx-action@bb05f3f, docker/login-action@af1e73f, docker/build-push-action@53b7df9, aquasecurity/trivy-action@c07df6f, github/codeql-action/upload-sarif@e4fba86, pypa/gh-action-pypi-publish@cef2210, actions/attest-build-provenance@0f67c3f, sigstore/gh-action-sigstore-python@5b79a39, actions/upload-artifact@043fb46, actions/download-artifact@3e5f45b, softprops/action-gh-release@3d0d988.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml (job-level permissions already specify the minimal required scopes).

4. script-injection: In sync-repo-metadata.yml, moved `${{ github.repository }}` to env var REPO_NAME. In mcp-security-index.yml, moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` to env vars GITHUB_TOKEN and GITHUB_REPOSITORY, referencing them as shell variables in the run block.


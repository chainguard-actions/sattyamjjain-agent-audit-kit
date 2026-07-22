<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.48

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.48** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags (e.g., @v7.0.0, @v4, @master) instead of immutable 40-character commit SHAs. This exposes the workflow to supply-chain attacks if the referenced tag is moved or the action is compromised.

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9
docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4
mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0
release.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3
sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/cve-watcher.yml:23`
- `.github/workflows/cve-watcher.yml:27`
- `.github/workflows/cve-watcher.yml:47`
- `.github/workflows/docker-nightly.yml:20`
- `.github/workflows/docker-nightly.yml:23`
- `.github/workflows/docker-nightly.yml:26`
- `.github/workflows/docker-nightly.yml:36`
- `.github/workflows/docker-nightly.yml:55`
- `.github/workflows/docker-nightly.yml:62`
- `.github/workflows/mcp-security-index.yml:25`
- `.github/workflows/mcp-security-index.yml:30`
- `.github/workflows/release.yml:57`
- `.github/workflows/release.yml:61`
- `.github/workflows/release.yml:67`
- `.github/workflows/release.yml:79`
- `.github/workflows/release.yml:83`
- `.github/workflows/release.yml:87`
- `.github/workflows/release.yml:97`
- `.github/workflows/release.yml:103`
- `.github/workflows/release.yml:120`
- `.github/workflows/release.yml:131`
- `.github/workflows/release.yml:140`
- `.github/workflows/release.yml:145`
- `.github/workflows/sync-rule-count.yml:27`
- `.github/workflows/sync-rule-count.yml:32`

### script-injection (severity: high)

Two workflow run: blocks directly interpolate ${{ ... }} expressions into shell command strings (sub-rule a), allowing template substitution to inject arbitrary shell metacharacters before the shell ever parses the command.

1. .github/workflows/sync-repo-metadata.yml: `gh repo edit "${{ github.repository }}" --description "$desc"` — the github.repository context value is interpolated directly into the shell command string.

2. .github/workflows/mcp-security-index.yml: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both secrets.GITHUB_TOKEN and github.repository are interpolated directly into the shell command string. These should be passed via env: variables instead.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:86`

### missing-permissions (severity: medium)

The workflow file ci.yml has no top-level permissions: key and no job-level permissions: key on any of its jobs. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents by default on many repositories).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow file scorecard.yml sets top-level permissions: read-all, which grants read access to all repository scopes. This is broader than necessary and should be replaced with specific minimal permissions (e.g., only security-events: write, id-token: write, contents: read as the job-level block already specifies).

Locations:

- `.github/workflows/scorecard.yml:7`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all mutable action references to full 40-char commit SHAs across cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. Actions pinned: actions/checkout@9c091bb, actions/setup-python@ece7cb0, actions/cache@caa2961, actions/github-script@3a2844b, docker/setup-buildx-action@bb05f3f, docker/login-action@af1e73f, docker/build-push-action@53b7df9, aquasecurity/trivy-action@c07df6f, github/codeql-action/upload-sarif@e4fba86, pypa/gh-action-pypi-publish@cef2210, actions/attest-build-provenance@0f67c3f, sigstore/gh-action-sigstore-python@5b79a39, actions/upload-artifact@043fb46, actions/download-artifact@3e5f45b, softprops/action-gh-release@3d0d988.

2. script-injection: Fixed two locations - (a) sync-repo-metadata.yml line 31: moved ${{ github.repository }} into env var REPOSITORY; (b) mcp-security-index.yml line 86: moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env vars GITHUB_TOKEN and REPOSITORY.

3. missing-permissions: Added top-level `permissions: contents: read` to ci.yml.

4. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write).


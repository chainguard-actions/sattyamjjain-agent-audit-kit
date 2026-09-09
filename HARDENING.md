<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.97

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.97** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference actions using mutable tags or version strings instead of full 40-character commit SHA pins. This exposes the workflow to supply-chain attacks if the referenced tag is moved or the action is compromised.

Affected references include:
- ci.yml: `actions/setup-python@v7`
- cve-deferral-date.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`
- cve-watcher.yml: `actions/checkout@v7.0.1` (×2), `actions/setup-python@v7` (×2), `actions/cache@v6`, `actions/github-script@v9` (×2)
- docker-nightly.yml: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`, `actions/github-script@v9`
- link-check.yml: `actions/checkout@v7.0.1` (×2), `lycheeverse/lychee-action@v2`, `actions/setup-python@v7`
- mcp-security-index.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/github-script@v9`
- release.yml: `actions/checkout@v7.0.1` (×many), `actions/setup-python@v7` (×many), `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7` (×2), `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `pypa/gh-action-pypi-publish@v1.14.2`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`
- sync-rule-count.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`

Locations:

- `.github/workflows/ci.yml:63`
- `.github/workflows/cve-deferral-date.yml:30`
- `.github/workflows/cve-watcher.yml:30`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/link-check.yml:42`
- `.github/workflows/mcp-security-index.yml:27`
- `.github/workflows/release.yml:62`
- `.github/workflows/sync-rule-count.yml:26`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and none of its jobs (test, counts) define job-level permissions either. Without explicit permissions, the workflow runs with the default token permissions, which may be overly broad (e.g., write access to contents and packages on some repository configurations).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`, `id-token: write`).

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): In mcp-security-index.yml, the 'Publish to gh-pages' run: block directly interpolates `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into a shell command string:

  git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"

Any `${{ ... }}` expression interpolated directly inside a `run:` shell command is a script injection risk — the YAML template substitution happens before the shell ever sees the string, bypassing shell quoting. These values should be passed via `env:` variables and referenced as `$ENV_VAR` in the shell script instead.

Locations:

- `.github/workflows/mcp-security-index.yml:127`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings across 8 workflow files:

1. unpinned-uses: Pinned all 16 distinct action references to full 40-char commit SHAs with tag comments in ci.yml, cve-deferral-date.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml (which had no permissions block at all).

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: `contents: read`, `security-events: write`, `id-token: write` (matching what the job-level block already specified).

4. script-injection: Fixed the 'Publish to gh-pages' step in mcp-security-index.yml by moving `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into an `env:` block as GH_TOKEN and GH_REPOSITORY, then referencing them as shell variables `${GH_TOKEN}` and `${GH_REPOSITORY}` in the run script.


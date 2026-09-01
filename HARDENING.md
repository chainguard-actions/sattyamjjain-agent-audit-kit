<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.91

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.91** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of immutable full-length SHA commit hashes, making them vulnerable to supply-chain attacks.

**ci.yml**: `actions/setup-python@v7`

**cve-watcher.yml**: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/cache@v6`, `actions/github-script@v9`

**docker-nightly.yml**: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master` (branch ref — highest risk), `github/codeql-action/upload-sarif@v4`, `actions/github-script@v9`

**link-check.yml**: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`, `actions/setup-python@v7`

**mcp-security-index.yml**: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/github-script@v9`

**release.yml**: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `pypa/gh-action-pypi-publish@v1.14.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master` (branch ref), `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`

**sync-rule-count.yml**: `actions/checkout@v7.0.1`, `actions/setup-python@v7`

Locations:

- `.github/workflows/ci.yml:26`
- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:26`
- `.github/workflows/link-check.yml:38`
- `.github/workflows/mcp-security-index.yml:27`
- `.github/workflows/release.yml:57`
- `.github/workflows/sync-rule-count.yml:27`

### missing-permissions (severity: medium)

The workflow file `ci.yml` has no top-level `permissions:` key and none of its jobs define job-level `permissions:` blocks. Without explicit permissions, the workflow runs with the default token permissions, which may be overly broad (e.g., `contents: write` on some repository configurations).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow file `scorecard.yml` sets `permissions: read-all` at the top level. This grants read access to all repository scopes and should be replaced with specific minimal permissions (the job-level block already narrows it, but the top-level `read-all` is still overly broad per the check definition).

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): The `Publish to gh-pages` step in `mcp-security-index.yml` directly interpolates `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` inside a `run:` shell command string. Any `${{ ... }}` expression inside a `run:` block is a script-injection risk because the value is substituted into the shell command before the shell parses it. The offending line is:

```
git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"
```

The safe pattern is to pass these values via `env:` variables and reference them as `$GITHUB_TOKEN` / `$GITHUB_REPOSITORY` in the shell script.

Locations:

- `.github/workflows/mcp-security-index.yml:110`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings: (1) Pinned all unpinned action references across ci.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml to full commit SHAs using lookup_action_sha. (2) Added 'permissions: contents: read' top-level block to ci.yml. (3) Replaced 'permissions: read-all' with 'permissions: contents: read' in scorecard.yml. (4) Fixed script injection in mcp-security-index.yml by moving ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into the step's env: block and referencing them as ${GH_TOKEN} and ${GH_REPOSITORY} in the shell script.


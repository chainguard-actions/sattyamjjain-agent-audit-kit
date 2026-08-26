<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.90

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.90** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use tag-based or branch-based `uses:` references instead of full 40-character SHA commit pins, making them vulnerable to supply-chain attacks if the referenced tag or branch is moved.

- ci.yml: `actions/setup-python@v6`
- cve-watcher.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/cache@v6`, `actions/github-script@v9`
- docker-nightly.yml: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`, `actions/github-script@v9`
- link-check.yml: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`, `actions/setup-python@v6`
- mcp-security-index.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/github-script@v9`
- release.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `pypa/gh-action-pypi-publish@v1.14.2`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`, `github/codeql-action/upload-sarif@v4`
- sync-rule-count.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`

Locations:

- `.github/workflows/ci.yml:55`
- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:23`
- `.github/workflows/link-check.yml:37`
- `.github/workflows/mcp-security-index.yml:26`
- `.github/workflows/release.yml:57`
- `.github/workflows/sync-rule-count.yml:26`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and neither the `test` job nor the `counts` job defines a job-level `permissions:` block. Without explicit permissions, the workflow runs with the default (potentially broad) token permissions.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

mcp-security-index.yml directly interpolates `${{ github.repository }}` inside a `run:` shell command string (sub-rule a). The offending line is: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any `${{ ... }}` expression in a `run:` block flows through YAML template substitution before the shell processes it, enabling injection if the value contains shell metacharacters. Use the `$GITHUB_REPOSITORY` environment variable instead.

Locations:

- `.github/workflows/mcp-security-index.yml:107`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. **unpinned-uses**: Pinned all tag/branch-based `uses:` references to full 40-character SHA commits across all 7 workflow files (ci.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml). Original tag names preserved as inline comments.

2. **missing-permissions**: Added `permissions: contents: read` top-level block to ci.yml (which had no permissions block at all).

3. **broad-permissions**: Replaced `permissions: read-all` in scorecard.yml with `permissions: contents: read`. The job-level permissions block already specifies the additional scopes needed (security-events: write, id-token: write).

4. **script-injection**: Fixed mcp-security-index.yml line 107 by moving `${{ secrets.GITHUB_TOKEN }}` into the step's `env:` block as `GH_TOKEN`, and replaced `${{ github.repository }}` with the built-in `$GITHUB_REPOSITORY` environment variable in the `git remote add` shell command.


<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.98

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.98** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference external actions using mutable tags or branch names instead of full 40-character SHA commit hashes, making them vulnerable to supply-chain attacks.

ci.yml: `actions/setup-python@v7` (in the counts job)

cve-deferral-date.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`

cve-watcher.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/cache@v6`, `actions/github-script@v9`

docker-nightly.yml: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`, `actions/github-script@v9`

link-check.yml: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`, `actions/setup-python@v7`

mcp-security-index.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/github-script@v9`

release.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`, `pypa/gh-action-pypi-publish@v1.14.2`

sync-rule-count.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`

Locations:

- `.github/workflows/ci.yml:65`
- `.github/workflows/cve-deferral-date.yml:30`
- `.github/workflows/cve-watcher.yml:30`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/link-check.yml:40`
- `.github/workflows/mcp-security-index.yml:26`
- `.github/workflows/release.yml:57`
- `.github/workflows/sync-rule-count.yml:22`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and neither the `test` job nor the `counts` job defines a job-level `permissions:` block. Without explicit permissions, the workflow inherits the default token permissions (which may be read/write depending on repository settings), violating the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants overly broad read access across all scopes and should be replaced with specific minimal permissions for each scope actually needed.

Locations:

- `.github/workflows/scorecard.yml:10`

### script-injection (severity: high)

Sub-rule (a): In mcp-security-index.yml, the 'Publish to gh-pages' run: block directly interpolates `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` inside a shell command string:

  git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"

Any `${{ ... }}` expression interpolated directly inside a `run:` block is a script-injection risk — the value is substituted by the YAML template engine before the shell ever sees it, bypassing shell quoting. The safe pattern is to pass these values via an `env:` block and reference them as `$GITHUB_TOKEN` / `$GITHUB_REPOSITORY` in the shell script.

Locations:

- `.github/workflows/mcp-security-index.yml:119`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings across 8 workflow files:

1. unpinned-uses: Pinned all 16 unique action references to full 40-character SHA hashes across ci.yml, cve-deferral-date.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. All SHAs were resolved using lookup_action_sha.

2. missing-permissions: Added top-level `permissions: contents: read` to ci.yml which had no permissions block.

3. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml. The job-level permissions block already specifies the specific scopes needed (security-events: write, id-token: write, contents: read).

4. script-injection: Fixed the 'Publish to gh-pages' step in mcp-security-index.yml by moving `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into an `env:` block (as GH_TOKEN and GH_REPOSITORY), then referencing them as shell variables `${GH_TOKEN}` and `${GH_REPOSITORY}` in the run script, preventing template injection.


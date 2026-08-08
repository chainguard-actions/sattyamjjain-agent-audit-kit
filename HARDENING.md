<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.70

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.70** was hardened automatically. 10 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): A `${{ github.repository }}` expression is interpolated directly inside a `run:` shell command. Line 31: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. An attacker who can influence the repository name (or who calls this workflow from a fork) could inject shell metacharacters. The value should be passed via an `env:` variable and expanded as `"$REPO"` in the shell.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`

### script-injection (severity: high)

Sub-rule (a): Two `${{ }}` expressions are interpolated directly inside a `run:` shell command. Line 85: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Both `secrets.GITHUB_TOKEN` and `github.repository` are expanded by the Actions template engine before the shell sees the string, meaning any newlines or shell metacharacters in those values execute as shell code. Both values should be passed via `env:` variables and referenced as `"$TOKEN"` / `"$REPO"` in the shell.

Locations:

- `.github/workflows/mcp-security-index.yml:85`

### unpinned-uses (severity: high)

All `uses:` references in this workflow use mutable tag or branch refs instead of immutable 40-character SHA digests, making the workflow vulnerable to supply-chain attacks if any referenced action is compromised or its tag is moved. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/cache@v6`, `actions/github-script@v9`.

Locations:

- `.github/workflows/cve-watcher.yml:19`

### unpinned-uses (severity: high)

All `uses:` references in this workflow use mutable tag or branch refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7` (×2), `aquasecurity/trivy-action@master` (branch ref — especially dangerous), `github/codeql-action/upload-sarif@v4`.

Locations:

- `.github/workflows/docker-nightly.yml:18`

### unpinned-uses (severity: high)

All `uses:` references in this workflow use mutable tag refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`.

Locations:

- `.github/workflows/link-check.yml:28`

### unpinned-uses (severity: high)

All `uses:` references in this workflow use mutable tag refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/mcp-security-index.yml:22`

### unpinned-uses (severity: high)

Numerous `uses:` references in this workflow use mutable tag or branch refs instead of immutable 40-character SHA digests. Failing references include: `actions/checkout@v7.0.1` (×4 jobs), `actions/setup-python@v7.0.0` (×4 jobs), `pypa/gh-action-pypi-publish@v1.14.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7` (×2), `aquasecurity/trivy-action@master` (branch ref), `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`.

Locations:

- `.github/workflows/release.yml:47`

### unpinned-uses (severity: high)

All `uses:` references in this workflow use mutable tag refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/sync-rule-count.yml:28`

### missing-permissions (severity: medium)

The workflow file has no top-level `permissions:` key and the single `test` job also has no `permissions:` key. Without explicit permissions, the workflow inherits the repository's default token permissions (which may be `read-all` or `write-all` depending on org settings), violating the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow has a top-level `permissions: read-all` which grants overly broad read access to all scopes. This should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`) matching only what each job actually needs.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 10 findings across 8 workflow files:

1. script-injection (sync-repo-metadata.yml): Moved ${{ github.repository }} to env var REPO.
2. script-injection (mcp-security-index.yml): Moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} to env vars GH_TOKEN and REPO.
3. unpinned-uses (cve-watcher.yml): Pinned actions/checkout, actions/setup-python, actions/cache, actions/github-script to full SHAs.
4. unpinned-uses (docker-nightly.yml): Pinned actions/checkout, docker/setup-buildx-action, docker/login-action, docker/build-push-action, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif to full SHAs.
5. unpinned-uses (link-check.yml): Pinned actions/checkout and lycheeverse/lychee-action to full SHAs.
6. unpinned-uses (mcp-security-index.yml): Pinned actions/checkout and actions/setup-python to full SHAs.
7. unpinned-uses (release.yml): Pinned all 13 unpinned action references across 4 jobs to full SHAs.
8. unpinned-uses (sync-rule-count.yml): Pinned actions/checkout and actions/setup-python to full SHAs.
9. missing-permissions (ci.yml): Added top-level permissions: contents: read.
10. broad-permissions (scorecard.yml): Replaced permissions: read-all with specific minimal permissions (contents: read, security-events: write, id-token: write).


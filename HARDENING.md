<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.76

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.76** was hardened automatically. 10 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): `${{ github.repository }}` is directly interpolated inside a `run:` shell command string. The offending line is: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. This allows the repository name (a github.* context value) to be substituted directly into the shell command before execution.

Locations:

- `.github/workflows/sync-repo-metadata.yml:23`

### script-injection (severity: high)

Sub-rule (a): `${{ github.repository }}` is directly interpolated inside a `run:` shell command string. The offending line is: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. The github.* context value is substituted directly into the shell command before execution.

Locations:

- `.github/workflows/mcp-security-index.yml:72`

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to tags or version strings instead of full 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/cache@v6`, `actions/github-script@v9`.

Locations:

- `.github/workflows/cve-watcher.yml:21`

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to tags or version strings instead of full 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7` (twice), `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`.

Locations:

- `.github/workflows/docker-nightly.yml:19`

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to tags or version strings instead of full 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`.

Locations:

- `.github/workflows/link-check.yml:29`

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to tags or version strings instead of full 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/mcp-security-index.yml:22`

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to tags or version strings instead of full 40-character SHA digests. Failing references: `actions/checkout@v7.0.1` (multiple jobs), `actions/setup-python@v7.0.0` (multiple jobs), `pypa/gh-action-pypi-publish@v1.14.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7` (twice), `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`.

Locations:

- `.github/workflows/release.yml:55`

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to tags or version strings instead of full 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/sync-rule-count.yml:27`

### missing-permissions (severity: medium)

The workflow file has no top-level `permissions:` key and the single job `test` also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow has a top-level `permissions: read-all` which grants overly broad read access to all scopes. This should be replaced with specific minimal permissions scoped to what each job actually needs.

Locations:

- `.github/workflows/scorecard.yml:8`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 10 findings across 8 workflow files:

1. script-injection (sync-repo-metadata.yml line 23): Moved `${{ github.repository }}` out of the `run:` shell command into an `env:` block as `REPO`, referenced as `"$REPO"` in the shell.

2. script-injection (mcp-security-index.yml line 72): Moved both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` out of the `run:` shell command into an `env:` block as `GH_TOKEN` and `REPO`, referenced as `${GH_TOKEN}` and `${REPO}` in the shell.

3. unpinned-uses (cve-watcher.yml): Pinned actions/checkout@v7.0.1→SHA, actions/setup-python@v7.0.0→SHA, actions/cache@v6→SHA, actions/github-script@v9→SHA.

4. unpinned-uses (docker-nightly.yml): Pinned actions/checkout@v7.0.1→SHA, docker/setup-buildx-action@v4→SHA, docker/login-action@v4→SHA, docker/build-push-action@v7→SHA, aquasecurity/trivy-action@master→SHA, github/codeql-action/upload-sarif@v4→SHA.

5. unpinned-uses (link-check.yml): Pinned actions/checkout@v7.0.1→SHA, lycheeverse/lychee-action@v2→SHA.

6. unpinned-uses (mcp-security-index.yml): Pinned actions/checkout@v7.0.1→SHA, actions/setup-python@v7.0.0→SHA.

7. unpinned-uses (release.yml): Pinned all 13 action references across 6 jobs to full commit SHAs.

8. unpinned-uses (sync-rule-count.yml): Pinned actions/checkout@v7.0.1→SHA, actions/setup-python@v7.0.0→SHA.

9. missing-permissions (ci.yml): Added top-level `permissions: contents: read`.

10. broad-permissions (scorecard.yml): Replaced `permissions: read-all` with `permissions: contents: read` (job-level already has specific security-events: write, id-token: write, contents: read).


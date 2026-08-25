<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.88

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.88** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable tags or branch names instead of full 40-character SHA commit hashes, making them vulnerable to supply-chain attacks if the referenced action is compromised or its tag is moved.

Failing references include:
- ci.yml: `actions/setup-python@v6`
- cve-watcher.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/cache@v6`, `actions/github-script@v9`
- docker-nightly.yml: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`, `actions/github-script@v9`
- link-check.yml: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`, `actions/setup-python@v6`
- mcp-security-index.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/github-script@v9`
- release.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`, `pypa/gh-action-pypi-publish@v1.14.2`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`
- sync-rule-count.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`

Note: `aquasecurity/trivy-action@master` is particularly dangerous as it pins to a mutable branch.

Locations:

- `.github/workflows/ci.yml:54`
- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/cve-watcher.yml:25`
- `.github/workflows/cve-watcher.yml:29`
- `.github/workflows/cve-watcher.yml:56`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/docker-nightly.yml:25`
- `.github/workflows/docker-nightly.yml:29`
- `.github/workflows/docker-nightly.yml:38`
- `.github/workflows/docker-nightly.yml:55`
- `.github/workflows/docker-nightly.yml:62`
- `.github/workflows/docker-nightly.yml:78`
- `.github/workflows/link-check.yml:37`
- `.github/workflows/link-check.yml:39`
- `.github/workflows/link-check.yml:72`
- `.github/workflows/link-check.yml:73`
- `.github/workflows/mcp-security-index.yml:27`
- `.github/workflows/mcp-security-index.yml:31`
- `.github/workflows/mcp-security-index.yml:121`
- `.github/workflows/release.yml:55`
- `.github/workflows/release.yml:62`
- `.github/workflows/release.yml:116`
- `.github/workflows/release.yml:118`
- `.github/workflows/release.yml:163`
- `.github/workflows/release.yml:165`
- `.github/workflows/release.yml:181`
- `.github/workflows/release.yml:183`
- `.github/workflows/release.yml:209`
- `.github/workflows/release.yml:211`
- `.github/workflows/release.yml:218`
- `.github/workflows/release.yml:228`
- `.github/workflows/release.yml:230`
- `.github/workflows/release.yml:232`
- `.github/workflows/release.yml:241`
- `.github/workflows/release.yml:245`
- `.github/workflows/release.yml:249`
- `.github/workflows/release.yml:265`
- `.github/workflows/release.yml:278`
- `.github/workflows/release.yml:280`
- `.github/workflows/release.yml:295`
- `.github/workflows/release.yml:302`
- `.github/workflows/release.yml:310`
- `.github/workflows/release.yml:370`
- `.github/workflows/sync-rule-count.yml:22`
- `.github/workflows/sync-rule-count.yml:27`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and neither of its jobs (`test`, `counts`) defines a job-level `permissions:` block. Without explicit permissions, the workflow runs with the default token permissions, which may be overly broad (e.g., `contents: write` on some repository configurations). All jobs in a workflow must have explicit permissions defined.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`, `id-token: write`) scoped to what the workflow actually needs.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all three findings:

1. unpinned-uses: Pinned all mutable tag/branch action references to full 40-char SHAs across 7 workflow files (ci.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml). Particularly important: aquasecurity/trivy-action@master (branch reference) was pinned to its current SHA. All original tags preserved as inline comments.

2. missing-permissions: Added top-level `permissions: contents: read` block to ci.yml which had no permissions block at all.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with `permissions: contents: read`. The job-level block already specifies the specific permissions needed (security-events: write, id-token: write, contents: read) so the top-level only needs to provide the minimal default.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in .github/workflows/mcp-security-index.yml at the 'Publish to gh-pages' step. Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` out of the run: shell command string and into an env: block as GH_TOKEN and GH_REPOSITORY respectively. The shell command now references them as ${GH_TOKEN} and ${GH_REPOSITORY} instead of using direct ${{ }} interpolation.


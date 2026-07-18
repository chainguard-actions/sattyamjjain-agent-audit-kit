<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.46

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.46** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable tags or branch names instead of full 40-character commit SHAs, making them vulnerable to supply-chain attacks.

Failing references in .github/workflows/cve-watcher.yml:
- actions/checkout@v7.0.0
- actions/setup-python@v6.3.0
- actions/cache@v5
- actions/github-script@v9

Failing references in .github/workflows/docker-nightly.yml:
- actions/checkout@v7.0.0
- docker/setup-buildx-action@v4
- docker/login-action@v4
- docker/build-push-action@v7
- aquasecurity/trivy-action@master
- github/codeql-action/upload-sarif@v4

Failing references in .github/workflows/mcp-security-index.yml:
- actions/checkout@v7.0.0
- actions/setup-python@v6.3.0

Failing references in .github/workflows/release.yml:
- actions/checkout@v7.0.0 (multiple jobs)
- actions/setup-python@v6.3.0 (multiple jobs)
- pypa/gh-action-pypi-publish@v1.14.0
- docker/setup-buildx-action@v4
- docker/login-action@v4
- aquasecurity/trivy-action@master
- docker/build-push-action@v7 (multiple steps)
- actions/attest-build-provenance@v4
- sigstore/gh-action-sigstore-python@v3.4.0
- actions/upload-artifact@v7
- actions/download-artifact@v8
- softprops/action-gh-release@v3

Failing references in .github/workflows/sync-rule-count.yml:
- actions/checkout@v7.0.0
- actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:18`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/mcp-security-index.yml:21`
- `.github/workflows/release.yml:44`
- `.github/workflows/sync-rule-count.yml:26`

### permissions (severity: medium)

missing-permissions: .github/workflows/ci.yml has no top-level `permissions:` key and its single job (`test`) also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### permissions (severity: medium)

broad-permissions: .github/workflows/scorecard.yml sets `permissions: read-all` at the top level (line 9). This grants read access to all repository scopes and should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): A `${{ ... }}` GitHub Actions expression is interpolated directly inside a `run:` shell command string.

In .github/workflows/sync-repo-metadata.yml, the 'Update GitHub repo description' step contains:
  `gh repo edit "${{ github.repository }}" --description "$desc" || true`
The `github.repository` context value is injected directly into the shell command before the shell ever sees it, enabling script injection if the value contains shell metacharacters.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`

### script-injection (severity: high)

Sub-rule (a): `${{ ... }}` GitHub Actions expressions are interpolated directly inside a `run:` shell command string.

In .github/workflows/mcp-security-index.yml, the 'Publish to gh-pages' step contains:
  `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`
Both `secrets.GITHUB_TOKEN` and `github.repository` are injected directly into the shell command string before the shell processes it.

Locations:

- `.github/workflows/mcp-security-index.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, permissions, script-injection

**Notes:**

Fixed all 5 findings across 7 workflow files:

1. unpinned-uses: Pinned all mutable tag/branch action references to full 40-char commit SHAs in cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. All 'uses:' lines now include the SHA with the original tag as a comment.

2. missing-permissions (ci.yml): Added top-level 'permissions: contents: read' block.

3. broad-permissions (scorecard.yml): Replaced 'permissions: read-all' with specific minimal permissions: contents: read, security-events: write, id-token: write.

4. script-injection (sync-repo-metadata.yml): Moved ${{ github.repository }} into env block as REPO_NAME; shell now uses $REPO_NAME.

5. script-injection (mcp-security-index.yml): Moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env block as GITHUB_TOKEN and GITHUB_REPOSITORY; shell now uses ${GITHUB_TOKEN} and ${GITHUB_REPOSITORY}.


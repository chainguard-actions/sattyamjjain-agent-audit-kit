<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.83

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.83** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of full 40-character commit SHAs, making them vulnerable to supply-chain attacks.

cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9

docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2

mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, pypa/gh-action-pypi-publish@v1.14.2, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/link-check.yml:37`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:87`
- `.github/workflows/sync-rule-count.yml:28`

### permissions (severity: medium)

missing-permissions: ci.yml has no top-level `permissions:` key and the single job `test` also has no `permissions:` key. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad (e.g., write access to contents).

Locations:

- `.github/workflows/ci.yml:1`

### permissions (severity: medium)

broad-permissions: scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Rule (a): `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly inside a `run:` shell command in the 'Publish to gh-pages' step. The line reads: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any `${{ ... }}` expression inside a `run:` block is substituted by the Actions template engine before the shell sees it, bypassing shell quoting.

Locations:

- `.github/workflows/mcp-security-index.yml:72`

### script-injection (severity: high)

Rule (a): `${{ github.repository }}` is interpolated directly inside a `run:` shell command in the 'Update GitHub repo description' step. The line reads: `gh repo edit "${{ github.repository }}" --description "$desc"`. Any `${{ ... }}` expression inside a `run:` block is substituted by the Actions template engine before the shell sees it, bypassing shell quoting.

Locations:

- `.github/workflows/sync-repo-metadata.yml:26`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, permissions, script-injection

**Notes:**

Fixed all findings across 7 workflow files:

1. unpinned-uses: Pinned all mutable action references to full 40-char SHAs in cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. Actions pinned include: actions/checkout@3d3c42e5, actions/setup-python@5fda3b95, actions/cache@55cc8345, actions/github-script@3a2844b7, docker/setup-buildx-action@bb05f3f5, docker/login-action@dbcb8138, docker/build-push-action@53b7df96, aquasecurity/trivy-action@d2a0b607, github/codeql-action/upload-sarif@ff2f1c62, lycheeverse/lychee-action@e7477775, actions/attest-build-provenance@4d101475, pypa/gh-action-pypi-publish@dc37677b, sigstore/gh-action-sigstore-python@790bc6be, actions/upload-artifact@043fb46d, actions/download-artifact@3e5f45b2, softprops/action-gh-release@3d0d9888.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml (job-level permissions already specify the specific elevated permissions needed for security-events: write and id-token: write).

4. script-injection (mcp-security-index.yml line 72): Moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env vars GH_TOKEN and GH_REPOSITORY, referenced as shell variables in the git remote add command.

5. script-injection (sync-repo-metadata.yml line 26): Moved ${{ github.repository }} into env var GH_REPOSITORY, referenced as shell variable in the gh repo edit command.


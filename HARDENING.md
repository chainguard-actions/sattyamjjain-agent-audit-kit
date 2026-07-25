<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.23

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.23** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): ${{ ... }} expressions are interpolated directly inside run: shell commands. In mcp-security-index.yml the 'Publish to gh-pages' step embeds `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` directly in a git remote URL string inside a run: block: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. In sync-repo-metadata.yml the 'Update GitHub repo description' step embeds `${{ github.repository }}` directly in a shell command: `gh repo edit "${{ github.repository }}" --description "$desc"`. Any ${{ ... }} expression inside a run: block is a script-injection risk because YAML template substitution occurs before the shell ever sees the value.

Locations:

- `.github/workflows/mcp-security-index.yml:72`
- `.github/workflows/sync-repo-metadata.yml:28`

### unpinned-uses (severity: high)

Multiple workflow files reference actions by mutable tags or branch names instead of full 40-character commit SHAs, making them vulnerable to supply-chain attacks. Failing references include:

cve-watcher.yml: actions/checkout@v6, actions/setup-python@v6.2.0, actions/cache@v5, actions/github-script@v9

docker-nightly.yml: actions/checkout@v6, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

mcp-security-index.yml: actions/checkout@v6, actions/setup-python@v6.2.0

release.yml: actions/checkout@v6, actions/setup-python@v6.2.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.3.0, actions/upload-artifact@v7, actions/download-artifact@v4, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v6, actions/setup-python@v6.2.0

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/mcp-security-index.yml:23`
- `.github/workflows/release.yml:50`
- `.github/workflows/sync-rule-count.yml:33`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: key and no job-level permissions: key on any of its jobs. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents by default on many repositories).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets a top-level `permissions: read-all` which grants read access to all repository scopes. This is overly broad; it should be replaced with specific minimal permissions (e.g., security-events: write, id-token: write, contents: read) matching only what the workflow actually needs.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. script-injection: In mcp-security-index.yml, moved `secrets.GITHUB_TOKEN` and `github.repository` from the git remote URL string in the run: block into an env: block (GH_TOKEN, GH_REPOSITORY), referencing them as plain shell variables. In sync-repo-metadata.yml, moved `github.repository` from the gh repo edit command into an env: block (GH_REPOSITORY).

2. unpinned-uses: Pinned all 16 unpinned action references across cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml to full 40-character commit SHAs with tag comments for readability. SHAs were resolved using lookup_action_sha.

3. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml (the workflow only reads code and runs tests).

4. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions matching what the workflow actually needs: `contents: read`, `security-events: write`, `id-token: write`.


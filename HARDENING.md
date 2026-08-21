<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.85

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.85** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Direct ${{ ... }} expression interpolation inside run: shell commands. (a) In sync-repo-metadata.yml, `${{ github.repository }}` is interpolated directly into a shell command: `gh repo edit "${{ github.repository }}" --description "$desc"`. (b) In mcp-security-index.yml, both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly into a shell command: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any ${{ ... }} expression inside a run: block is a script-injection risk because the value is substituted into the shell command string before the shell parses it.

Locations:

- `.github/workflows/sync-repo-metadata.yml:27`
- `.github/workflows/mcp-security-index.yml:72`

### unpinned-uses (severity: high)

Multiple workflow files reference actions using mutable version tags or branch names instead of immutable 40-character SHA digests, making them vulnerable to supply-chain attacks if the tag is moved or the branch is compromised. Failing references include: cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9; docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4; link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2; mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0; release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3, pypa/gh-action-pypi-publish@v1.14.2; sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

Locations:

- `.github/workflows/cve-watcher.yml:21`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/link-check.yml:29`
- `.github/workflows/mcp-security-index.yml:20`
- `.github/workflows/release.yml:50`
- `.github/workflows/sync-rule-count.yml:33`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: key and its single job (test) also has no job-level permissions: key. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be broader than necessary (e.g., write access to contents). A minimal permissions block such as `permissions: contents: read` should be added.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (e.g., only the scopes actually needed: contents: read, security-events: write, id-token: write).

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. script-injection: In sync-repo-metadata.yml, moved ${{ github.repository }} to env block as REPO_NAME. In mcp-security-index.yml, moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} to env block as GH_TOKEN and REPO_NAME, using ${GH_TOKEN} and ${REPO_NAME} in the shell command.

2. unpinned-uses: Pinned all unpinned action references to full 40-char SHAs across 6 workflow files: cve-watcher.yml (checkout, setup-python, cache, github-script), docker-nightly.yml (checkout, setup-buildx-action, login-action, build-push-action x2, trivy-action, upload-sarif), link-check.yml (checkout, lychee-action), mcp-security-index.yml (checkout, setup-python), release.yml (checkout x6, setup-python x5, setup-buildx-action, login-action, build-push-action x2, trivy-action, attest-build-provenance, gh-action-sigstore-python, upload-artifact, download-artifact, action-gh-release, gh-action-pypi-publish), sync-rule-count.yml (checkout, setup-python).

3. missing-permissions: Added top-level `permissions: contents: read` to ci.yml.

4. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write) matching what the job-level already specified.


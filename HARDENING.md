<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.68

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.68** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): ${{ }} expressions are directly interpolated inside run: shell commands. In mcp-security-index.yml, the 'Publish to gh-pages' step embeds ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} directly in a git remote add origin URL within a run: block. These are substituted by the YAML template engine before the shell sees them, making ${{ github.repository }} a script-injection vector (a repository name containing shell metacharacters would be executed). The ${{ secrets.GITHUB_TOKEN }} interpolation also leaks the token value into the shell command string.

Locations:

- `.github/workflows/mcp-security-index.yml:80`

### script-injection (severity: high)

Sub-rule (a): ${{ github.repository }} is directly interpolated inside a run: shell command. In sync-repo-metadata.yml, the 'Update GitHub repo description' step embeds ${{ github.repository }} directly in a gh repo edit command within a run: block. This value is substituted by the YAML template engine before the shell sees it, making it a script-injection vector if the repository name contains shell metacharacters.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable tag or version refs instead of immutable 40-character SHA digests, making them vulnerable to supply-chain attacks if the referenced tag is moved or the action is compromised.

release.yml unpinned refs: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

docker-nightly.yml unpinned refs: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4.

cve-watcher.yml unpinned refs: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9.

mcp-security-index.yml unpinned refs: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

sync-rule-count.yml unpinned refs: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

Locations:

- `.github/workflows/release.yml:52`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/mcp-security-index.yml:24`
- `.github/workflows/sync-rule-count.yml:28`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: key and no job-level permissions: key on any of its jobs. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be broader than necessary (e.g., write access to contents). This violates the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets permissions: read-all at the top level. This grants read access to all available GitHub token scopes (contents, issues, pull-requests, packages, etc.) rather than only the specific scopes needed. Even though the single job overrides with narrower permissions, the top-level read-all is overly broad and should be replaced with specific minimal scopes.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 5 findings across 6 workflow files:

1. script-injection (mcp-security-index.yml): Moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} from the git remote URL into the step's env: block as GH_TOKEN and GH_REPOSITORY, referenced as shell variables.

2. script-injection (sync-repo-metadata.yml): Moved ${{ github.repository }} from the gh repo edit command into the step's env: block as GH_REPOSITORY.

3. unpinned-uses: Pinned all mutable tag/branch references to full 40-character SHA digests across release.yml, docker-nightly.yml, cve-watcher.yml, mcp-security-index.yml, and sync-rule-count.yml. Actions pinned include: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3, github/codeql-action/upload-sarif@v4, actions/cache@v6, actions/github-script@v9.

4. missing-permissions (ci.yml): Added `permissions: contents: read` at the top level.

5. broad-permissions (scorecard.yml): Replaced `permissions: read-all` with `permissions: contents: read` at the top level.


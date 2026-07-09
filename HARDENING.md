<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.48

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **sattyamjjain--agent-audit-kit/v0.3.48** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use mutable version tags or branch names instead of full 40-character SHA commit pins, making them vulnerable to supply-chain attacks if the referenced action is compromised or its tag is moved.

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9

docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

release.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/cve-watcher.yml:23`
- `.github/workflows/cve-watcher.yml:27`
- `.github/workflows/cve-watcher.yml:46`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/docker-nightly.yml:25`
- `.github/workflows/docker-nightly.yml:37`
- `.github/workflows/docker-nightly.yml:56`
- `.github/workflows/docker-nightly.yml:64`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/mcp-security-index.yml:27`
- `.github/workflows/release.yml:44`
- `.github/workflows/release.yml:47`
- `.github/workflows/release.yml:54`
- `.github/workflows/release.yml:64`
- `.github/workflows/release.yml:68`
- `.github/workflows/release.yml:75`
- `.github/workflows/release.yml:82`
- `.github/workflows/release.yml:93`
- `.github/workflows/release.yml:120`
- `.github/workflows/release.yml:130`
- `.github/workflows/release.yml:148`
- `.github/workflows/release.yml:163`
- `.github/workflows/release.yml:175`
- `.github/workflows/release.yml:185`
- `.github/workflows/sync-rule-count.yml:30`
- `.github/workflows/sync-rule-count.yml:35`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: key and no job-level permissions: key on any of its jobs. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents by default in many configurations).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets top-level permissions: read-all, which grants read access to all scopes rather than the minimal specific permissions needed. This should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:7`

### script-injection (severity: high)

GitHub Actions expressions are interpolated directly inside run: shell command strings, which allows template substitution to inject arbitrary shell content before the shell parses the command.

(a) sync-repo-metadata.yml: `gh repo edit "${{ github.repository }}" --description "$desc"` — ${{ github.repository }} is interpolated directly into the shell command string.

(a) mcp-security-index.yml: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} are interpolated directly into the shell command string.

Locations:

- `.github/workflows/sync-repo-metadata.yml:24`
- `.github/workflows/mcp-security-index.yml:72`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all findings across 6 workflow files: (1) unpinned-uses: Pinned all mutable action tags to full 40-char SHAs in cve-watcher.yml (checkout, setup-python, cache, github-script), docker-nightly.yml (checkout, setup-buildx-action, login-action, build-push-action, trivy-action, codeql-action/upload-sarif), mcp-security-index.yml (checkout, setup-python), release.yml (checkout x4, setup-python x2, pypi-publish, setup-buildx-action, login-action, build-push-action x2, trivy-action, attest-build-provenance, sigstore-python, upload-artifact, download-artifact, action-gh-release), sync-rule-count.yml (checkout, setup-python). (2) missing-permissions: Added 'permissions: contents: read' top-level block to ci.yml. (3) broad-permissions: Replaced 'permissions: read-all' with 'permissions: contents: read' in scorecard.yml (job-level permissions already had specific minimal grants). (4) script-injection: In sync-repo-metadata.yml, moved ${{ github.repository }} to env block as GH_REPOSITORY and replaced inline expression with $GH_REPOSITORY in shell; in mcp-security-index.yml, moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} to env block as GH_TOKEN and GH_REPOSITORY and replaced inline expressions with ${GH_TOKEN} and ${GH_REPOSITORY} in shell.


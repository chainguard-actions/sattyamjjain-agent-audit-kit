<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.56

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.56** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use mutable tag or branch refs instead of pinned 40-character SHA commit hashes, making them vulnerable to supply-chain attacks if the referenced action is compromised or the tag is moved.

release.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9

mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/release.yml:43`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/cve-watcher.yml:18`
- `.github/workflows/mcp-security-index.yml:23`
- `.github/workflows/sync-rule-count.yml:28`

### script-injection (severity: high)

${{ }} expressions are interpolated directly inside run: shell command strings, which allows template substitution to inject arbitrary shell commands before the shell ever parses the string.

(a) mcp-security-index.yml — 'Publish to gh-pages' step: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} are interpolated directly into the shell command. Even though secrets.GITHUB_TOKEN is GitHub-controlled, any ${{ ... }} expression inside a run: block is a script-injection risk per the check rules.

(b) sync-repo-metadata.yml — 'Update GitHub repo description' step: `gh repo edit "${{ github.repository }}" --description "$desc"` — ${{ github.repository }} is interpolated directly into the shell command string inside a run: block.

Locations:

- `.github/workflows/mcp-security-index.yml:72`
- `.github/workflows/sync-repo-metadata.yml:30`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and the single job (`test`) also has no `permissions:` key. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents, etc.).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is considered overly broad. It should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`, `id-token: write`).

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all 15 action references across release.yml, docker-nightly.yml, cve-watcher.yml, mcp-security-index.yml, and sync-rule-count.yml to full 40-character SHA commit hashes with tag comments.

2. script-injection: In mcp-security-index.yml, moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} from the 'Publish to gh-pages' run: shell string into the step's env: block (as GH_TOKEN and GH_REPOSITORY). In sync-repo-metadata.yml, moved ${{ github.repository }} from the 'Update GitHub repo description' run: shell string into the step's env: block (as GH_REPOSITORY).

3. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

4. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: contents: read, security-events: write, id-token: write.


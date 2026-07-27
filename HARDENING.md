<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.60

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.60** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use action references pinned to mutable tags or branch names instead of immutable 40-character commit SHAs, making them vulnerable to supply-chain attacks.

.github/workflows/cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v6, actions/github-script@v9

.github/workflows/docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

.github/workflows/mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

.github/workflows/release.yml: actions/checkout@v7.0.0 (multiple), actions/setup-python@v6.3.0 (multiple), pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (multiple), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

.github/workflows/sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:23`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:47`
- `.github/workflows/sync-rule-count.yml:28`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and no job-level `permissions:` key on any of its jobs. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents by default on many repositories).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes rather than the minimal specific permissions required, violating the principle of least privilege.

Locations:

- `.github/workflows/scorecard.yml:10`

### script-injection (severity: high)

Sub-rule (a): GitHub Actions expressions are interpolated directly inside `run:` shell command strings.

In .github/workflows/sync-repo-metadata.yml, the expression `${{ github.repository }}` is interpolated directly into a shell command: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. If the repository name contained shell metacharacters, this could lead to command injection.

In .github/workflows/mcp-security-index.yml, both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly into a shell command: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any `${{ ... }}` expression directly inside a `run:` block is a script-injection risk — the value is substituted into the shell script before the shell parses it.

Locations:

- `.github/workflows/sync-repo-metadata.yml:28`
- `.github/workflows/mcp-security-index.yml:68`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all action references to full 40-char commit SHAs across cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. Actions pinned: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0, actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1, actions/cache@55cc8345863c7cc4c66a329aec7e433d2d1c52a9, actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3, docker/setup-buildx-action@bb05f3f5519dd87d3ba754cc423b652a5edd6d2c, docker/login-action@abd2ef45e78c5afb21d64d4ca52ee8550d9572c7, docker/build-push-action@53b7df96c91f9c12dcc8a07bcb9ccacbed38856a, aquasecurity/trivy-action@c07df6fec6fa692e6fd1200d50aaa1fdd66f03c8, github/codeql-action/upload-sarif@e4fba868fa4b1b91e1fdab776edc8cfbe6e9fb81, pypa/gh-action-pypi-publish@cef221092ed1bacb1cc03d23a2d87d1d172e277b, actions/attest-build-provenance@0f67c3f4856b2e3261c31976d6725780e5e4c373, sigstore/gh-action-sigstore-python@5b79a39c381910c090341a2c9b0bf022c8b387e1, actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a, actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c, softprops/action-gh-release@3d0d9888cb7fd7b750713d6e236d1fcb99157228.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml (job-level permissions already specify minimal specific permissions).

4. script-injection: In sync-repo-metadata.yml, moved ${{ github.repository }} into env var REPOSITORY. In mcp-security-index.yml, moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env vars GITHUB_TOKEN and REPOSITORY, referencing them as plain shell variables in the run block.


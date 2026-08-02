<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.66

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.66** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of immutable 40-character SHA commit hashes, making them vulnerable to supply-chain attacks.

release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9

docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

Locations:

- `.github/workflows/release.yml:47`
- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/mcp-security-index.yml:25`
- `.github/workflows/sync-rule-count.yml:22`

### script-injection (severity: high)

GitHub Actions expressions are directly interpolated inside `run:` shell command strings, violating sub-rule (a). This allows the expression value to be parsed by the shell before quoting can protect it.

1. sync-repo-metadata.yml ("Update GitHub repo description" step): `gh repo edit "${{ github.repository }}" --description "$desc" || true` — `${{ github.repository }}` is interpolated directly into the shell command.

2. mcp-security-index.yml ("Publish to gh-pages" step): `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly into the shell command. These should be passed via `env:` variables and referenced as `$VAR` in the shell.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:86`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and its only job (`test`) also has no job-level `permissions:` key. Without explicit permissions, the workflow runs with the default token permissions, which may be overly broad (write access to contents and other scopes depending on repository settings). All permissions should be explicitly declared using the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml has `permissions: read-all` at the top level. This grants read access to all available scopes (contents, packages, actions, checks, deployments, issues, pull-requests, security-events, etc.), which is overly broad. It should be replaced with specific minimal permissions required by the workflow (e.g., `contents: read`, `security-events: write`, `id-token: write`).

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all action references to full SHA hashes in release.yml (actions/checkout, actions/setup-python, pypa/gh-action-pypi-publish, docker/setup-buildx-action, docker/login-action, docker/build-push-action x2, aquasecurity/trivy-action, actions/attest-build-provenance, sigstore/gh-action-sigstore-python, actions/upload-artifact, actions/download-artifact, softprops/action-gh-release), cve-watcher.yml (actions/checkout, actions/setup-python, actions/cache, actions/github-script), docker-nightly.yml (actions/checkout, docker/setup-buildx-action, docker/login-action, docker/build-push-action, aquasecurity/trivy-action, github/codeql-action/upload-sarif), mcp-security-index.yml (actions/checkout, actions/setup-python), and sync-rule-count.yml (actions/checkout, actions/setup-python). Original tags preserved as comments.

2. script-injection: In sync-repo-metadata.yml, moved ${{ github.repository }} to env var REPO and referenced as $REPO in shell. In mcp-security-index.yml, moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} to env vars GITHUB_TOKEN and REPO and referenced as ${GITHUB_TOKEN} and ${REPO} in shell.

3. missing-permissions: Added top-level `permissions: contents: read` to ci.yml.

4. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: contents: read, security-events: write, id-token: write.


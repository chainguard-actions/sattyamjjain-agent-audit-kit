<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.87

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.87** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of immutable full-length SHA commit hashes, making them vulnerable to supply-chain attacks if the referenced action is compromised or the tag is moved.

Failing references in release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3, pypa/gh-action-pypi-publish@v1.14.2.

Failing references in cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9.

Failing references in docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, actions/github-script@v9.

Failing references in link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2.

Failing references in mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/github-script@v9.

Failing references in sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

Locations:

- `.github/workflows/release.yml:1`
- `.github/workflows/cve-watcher.yml:1`
- `.github/workflows/docker-nightly.yml:1`
- `.github/workflows/link-check.yml:1`
- `.github/workflows/mcp-security-index.yml:1`
- `.github/workflows/sync-rule-count.yml:1`

### missing-permissions (severity: medium)

The workflow file ci.yml has no top-level `permissions:` key and its single job (`test`) also has no job-level `permissions:` key. Without explicit permissions, the workflow runs with the default token permissions, which may be overly broad (e.g., write access to contents on some repository configurations). All jobs in a workflow must have explicit permissions, or a top-level permissions block must be present.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow file scorecard.yml sets `permissions: read-all` at the top level (line 9). This grants read access to all available scopes, which is broader than necessary. The individual job already overrides with specific permissions (security-events: write, id-token: write, contents: read), so the top-level `read-all` should be replaced with a minimal specific set matching only what the workflow actually needs.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all three findings:

1. **unpinned-uses**: Pinned all action references across 6 workflow files (release.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, sync-rule-count.yml) to full SHA commit hashes. Actions pinned: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1, actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97, docker/setup-buildx-action@37fe631027851001ddb9b187196cc803df7f5f0e, docker/login-action@dbcb813823bdd20940b903addbd779551569679f, docker/build-push-action@53b7df96c91f9c12dcc8a07bcb9ccacbed38856a, aquasecurity/trivy-action@d2a0b60797ff03db6132bd4e2b293f9b37081297, actions/attest-build-provenance@4d101475d8b20a2381f78447822ac1eab6504dd8, sigstore/gh-action-sigstore-python@790bc6befb9d733738f18d8f895854b453640ec9, actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a, actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c, softprops/action-gh-release@3d0d9888cb7fd7b750713d6e236d1fcb99157228, pypa/gh-action-pypi-publish@dc37677b2e1c63e2034f94d8a5b11f265b73ba33, actions/cache@55cc8345863c7cc4c66a329aec7e433d2d1c52a9, actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3, github/codeql-action/upload-sarif@db488ddef3bf6cb639b32c2e9a7c0a7ea8271d28, lycheeverse/lychee-action@e7477775783ea5526144ba13e8db5eec57747ce8.

2. **missing-permissions**: Added `permissions: contents: read` top-level block to ci.yml.

3. **broad-permissions**: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: `contents: read`, `security-events: write`, `id-token: write`.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Publish to gh-pages' step of .github/workflows/mcp-security-index.yml. Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` out of the `run:` shell string and into an `env:` block. The shell command now references them as `${GITHUB_TOKEN}` and `${GITHUB_REPOSITORY}` environment variables, preventing YAML template substitution from bypassing shell quoting.


<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.79

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.79** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of full 40-character SHA commit hashes, making them vulnerable to supply-chain attacks.

cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9
docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4
link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2
mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0
release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3
sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/link-check.yml:31`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:55`
- `.github/workflows/sync-rule-count.yml:22`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and the `test` job also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad (e.g., write access to contents). All jobs in a workflow file must have explicit permissions defined.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets a top-level `permissions: read-all`, which grants read access to all repository scopes. This is overly broad and should be replaced with specific minimal permissions (e.g., `security-events: write`, `contents: read`) required by each job.

Locations:

- `.github/workflows/scorecard.yml:8`

### script-injection (severity: high)

Sub-rule (a): A `${{ ... }}` GitHub Actions expression is interpolated directly inside a `run:` shell command string, allowing YAML template substitution to inject arbitrary shell content before the shell processes the command.

1. sync-repo-metadata.yml line ~31: `gh repo edit "${{ github.repository }}" --description "$desc"` — `github.repository` is a github.* context value interpolated directly into the shell command.

2. mcp-security-index.yml line ~86: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — `github.repository` is a github.* context value interpolated directly into the shell command. Both values should be passed via `env:` variables and referenced as `$ENV_VAR` in the shell script.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:86`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all 4 findings across 7 workflow files:

1. unpinned-uses: Pinned all action references to full 40-char SHAs in cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. Actions pinned include: actions/checkout@3d3c42e5, actions/setup-python@5fda3b95, actions/cache@55cc8345, actions/github-script@3a2844b7, docker/setup-buildx-action@bb05f3f5, docker/login-action@dbcb8138, docker/build-push-action@53b7df96, aquasecurity/trivy-action@d2a0b607, github/codeql-action/upload-sarif@ff2f1c62, lycheeverse/lychee-action@e7477775, pypa/gh-action-pypi-publish@dc37677b, actions/attest-build-provenance@4d101475, sigstore/gh-action-sigstore-python@790bc6be, actions/upload-artifact@043fb46d, actions/download-artifact@3e5f45b2, softprops/action-gh-release@3d0d9888.

2. missing-permissions: Added top-level `permissions: contents: read` to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write).

4. script-injection: Fixed both instances by moving github context expressions into env: blocks. In sync-repo-metadata.yml, `${{ github.repository }}` moved to env var REPOSITORY. In mcp-security-index.yml, both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` moved to env vars GITHUB_TOKEN and REPOSITORY respectively.


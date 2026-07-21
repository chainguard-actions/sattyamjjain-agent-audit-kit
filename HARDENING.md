<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.24

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.24** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference third-party actions using mutable version tags instead of full 40-character SHA digests, making them vulnerable to supply-chain attacks if the tag is moved.

cve-watcher.yml: actions/checkout@v6, actions/setup-python@v6.2.0, actions/cache@v5, actions/github-script@v9

docker-nightly.yml: actions/checkout@v6, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

mcp-security-index.yml: actions/checkout@v6, actions/setup-python@v6.2.0

release.yml: actions/checkout@v6, actions/setup-python@v6.2.0, pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.3.0, actions/upload-artifact@v7, actions/download-artifact@v4, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v6, actions/setup-python@v6.2.0

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/mcp-security-index.yml:25`
- `.github/workflows/release.yml:44`
- `.github/workflows/sync-rule-count.yml:20`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and the single `test` job also has no `permissions:` key. The workflow therefore runs with GitHub's default token permissions (which include write access to contents and packages in many contexts), violating the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`, `id-token: write`).

Locations:

- `.github/workflows/scorecard.yml:11`

### script-injection (severity: high)

Two workflow `run:` blocks interpolate GitHub Actions expressions directly into shell commands (sub-rule a), allowing template substitution to inject arbitrary shell content before the shell ever parses the string.

1. sync-repo-metadata.yml (line 31): `gh repo edit "${{ github.repository }}" --description "$desc"` — `github.repository` is interpolated directly into the shell command.

2. mcp-security-index.yml (line 86): `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both `secrets.GITHUB_TOKEN` and `github.repository` are interpolated directly into the shell command. These should be passed via `env:` variables and referenced as `$ENV_VAR` in the shell.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:86`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all mutable action references across 5 workflow files (cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml) to full 40-character SHA digests with tag comments. Actions pinned: actions/checkout@v6, actions/setup-python@v6.2.0, actions/cache@v5, actions/github-script@v9, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, pypa/gh-action-pypi-publish@v1.14.0, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.3.0, actions/upload-artifact@v7, actions/download-artifact@v4, softprops/action-gh-release@v3.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: `contents: read`, `security-events: write`, `id-token: write`.

4. script-injection: (a) sync-repo-metadata.yml: moved `${{ github.repository }}` into env var `REPOSITORY` and referenced as `$REPOSITORY` in shell. (b) mcp-security-index.yml: moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env vars `GITHUB_TOKEN` and `REPOSITORY`, referenced as `${GITHUB_TOKEN}` and `${REPOSITORY}` in shell.


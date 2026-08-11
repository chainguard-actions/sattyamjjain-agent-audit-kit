<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.73

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.73** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): A ${{ }} expression is directly interpolated inside a run: shell command string. In sync-repo-metadata.yml, `${{ github.repository }}` is interpolated directly into a shell command: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. In mcp-security-index.yml, both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly into a shell command: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any ${{ ... }} expression inside a run: block is a script-injection risk because YAML template substitution happens before the shell ever sees the value.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:77`

### unpinned-uses (severity: high)

Multiple workflow files reference actions by mutable version tags or branch names instead of immutable 40-character SHA commit hashes, making them vulnerable to supply-chain attacks. Failing references include: cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9. docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4. link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2. mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0. release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3. sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/docker-nightly.yml:16`
- `.github/workflows/link-check.yml:28`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:57`
- `.github/workflows/sync-rule-count.yml:22`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and the single `test` job also has no `permissions:` key. Without explicit permissions, the workflow inherits the default repository permissions (which can include write access to contents and other scopes), violating the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all available scopes rather than the minimal specific permissions required, violating the principle of least privilege. It should be replaced with specific minimal permissions (e.g., `security-events: write`, `contents: read`, `id-token: write`).

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. script-injection: In sync-repo-metadata.yml, moved `${{ github.repository }}` to a `REPO` env var. In mcp-security-index.yml, moved `${{ secrets.GITHUB_TOKEN }}` to `GH_TOKEN` env var and `${{ github.repository }}` to `REPO` env var; both are now referenced as `${GH_TOKEN}` and `${REPO}` in the shell script.

2. unpinned-uses: Pinned all unpinned action references to full 40-char SHAs with original tag as comment: actions/checkout@v7.0.1→3d3c42e5, actions/setup-python@v7.0.0→5fda3b95, actions/cache@v6→55cc8345, actions/github-script@v9→3a2844b7, docker/setup-buildx-action@v4→bb05f3f5, docker/login-action@v4→dbcb8138, docker/build-push-action@v7→53b7df96, aquasecurity/trivy-action@master→27365332, github/codeql-action/upload-sarif@v4→5595ccaf, lycheeverse/lychee-action@v2→e7477775, pypa/gh-action-pypi-publish@v1.14.2→dc37677b, actions/attest-build-provenance@v4→4d101475, sigstore/gh-action-sigstore-python@v3.5.0→790bc6be, actions/upload-artifact@v7→043fb46d, actions/download-artifact@v8→3e5f45b2, softprops/action-gh-release@v3→3d0d9888.

3. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

4. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: `contents: read`, `security-events: write`, `id-token: write`.


<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.49

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **sattyamjjain--agent-audit-kit/v0.3.49** was hardened automatically. 9 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): ${{ github.repository }} is interpolated directly inside a run: shell command string. In the 'Update GitHub repo description' step: `gh repo edit "${{ github.repository }}" --description "$desc"`. The github.* context value is substituted by the YAML template engine before the shell sees it, enabling script injection.

Locations:

- `.github/workflows/sync-repo-metadata.yml:22`

### script-injection (severity: high)

Sub-rule (a): ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} are interpolated directly inside a run: shell command string in the 'Publish to gh-pages' step: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. These ${{ ... }} expressions are substituted by the YAML template engine before the shell sees them.

Locations:

- `.github/workflows/mcp-security-index.yml:76`

### unpinned-uses (severity: high)

Multiple actions are referenced by tag/version instead of a full 40-character SHA commit hash. Unpinned refs: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9.

Locations:

- `.github/workflows/cve-watcher.yml:18`

### unpinned-uses (severity: high)

Multiple actions are referenced by tag/version instead of a full 40-character SHA commit hash. Unpinned refs: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4.

Locations:

- `.github/workflows/docker-nightly.yml:20`

### unpinned-uses (severity: high)

Multiple actions are referenced by tag/version instead of a full 40-character SHA commit hash. Unpinned refs: actions/checkout@v7.0.0, actions/setup-python@v6.3.0.

Locations:

- `.github/workflows/mcp-security-index.yml:26`

### unpinned-uses (severity: high)

Multiple actions are referenced by tag/version instead of a full 40-character SHA commit hash. Unpinned refs: actions/checkout@v7.0.0 (multiple jobs), actions/setup-python@v6.3.0 (multiple jobs), pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (multiple), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

Locations:

- `.github/workflows/release.yml:43`

### unpinned-uses (severity: high)

Multiple actions are referenced by tag/version instead of a full 40-character SHA commit hash. Unpinned refs: actions/checkout@v7.0.0, actions/setup-python@v6.3.0.

Locations:

- `.github/workflows/sync-rule-count.yml:27`

### missing-permissions (severity: medium)

The workflow file has no top-level permissions: key and the 'test' job also has no job-level permissions: key. Without explicit permissions, the workflow inherits the default repository permissions which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow has a top-level `permissions: read-all` which grants overly broad read access to all scopes. It should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:8`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 9 findings across 7 workflow files:

1. **script-injection** (sync-repo-metadata.yml line 22): Moved `${{ github.repository }}` out of the run: shell string into the step's env: block as `REPO`, referenced as `$REPO` in the shell script.

2. **script-injection** (mcp-security-index.yml line 76): Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` out of the run: shell string into the step's env: block as `GH_TOKEN` and `REPO`, referenced as `${GH_TOKEN}` and `${REPO}` in the shell script.

3. **unpinned-uses** (cve-watcher.yml): Pinned actions/checkout@v7.0.0→SHA 9c091bb2, actions/setup-python@v6.3.0→SHA ece7cb06, actions/cache@v5→SHA caa29612, actions/github-script@v9→SHA 3a2844b7.

4. **unpinned-uses** (docker-nightly.yml): Pinned actions/checkout@v7.0.0→SHA 9c091bb2, docker/setup-buildx-action@v4→SHA bb05f3f5, docker/login-action@v4→SHA af1e73f9, docker/build-push-action@v7→SHA 53b7df96, aquasecurity/trivy-action@master→SHA c07df6fe, github/codeql-action/upload-sarif@v4→SHA 99df26d4.

5. **unpinned-uses** (mcp-security-index.yml): Pinned actions/checkout@v7.0.0→SHA 9c091bb2, actions/setup-python@v6.3.0→SHA ece7cb06.

6. **unpinned-uses** (release.yml): Pinned all 11 unpinned actions to full commit SHAs.

7. **unpinned-uses** (sync-rule-count.yml): Pinned actions/checkout@v7.0.0→SHA 9c091bb2, actions/setup-python@v6.3.0→SHA ece7cb06.

8. **missing-permissions** (ci.yml): Added top-level `permissions: contents: read` block.

9. **broad-permissions** (scorecard.yml): Replaced `permissions: read-all` with specific minimal permissions: `contents: read`, `security-events: write`, `id-token: write`.


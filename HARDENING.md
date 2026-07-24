<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.52

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.52** was hardened automatically. 9 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): ${{ github.repository }} (a github.* context value) is interpolated directly inside a run: shell command string. In sync-repo-metadata.yml line 31: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. An attacker who can influence the repository name could inject shell metacharacters. The value should be passed via an env: variable and the expansion double-quoted.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`

### script-injection (severity: high)

Sub-rule (a): ${{ github.repository }} (a github.* context value) is interpolated directly inside a run: shell command string. In mcp-security-index.yml line 80: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. An attacker who can influence the repository name could inject shell metacharacters. The value should be passed via an env: variable and the expansion double-quoted.

Locations:

- `.github/workflows/mcp-security-index.yml:80`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: key and its only job (test) also has no job-level permissions: key. Without explicit permissions, the workflow inherits the repository default (typically write access to all scopes for private repos, or read access for public repos), which violates the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets top-level `permissions: read-all`, which grants read access to all available scopes. This is overly broad; only the specific permissions required (security-events: write, id-token: write, contents: read) should be granted at the job level, which the job does define — but the top-level read-all still overrides the default and is flagged as broad.

Locations:

- `.github/workflows/scorecard.yml:9`

### unpinned-uses (severity: high)

cve-watcher.yml references multiple actions by mutable version tags instead of full 40-character commit SHAs, making the workflow vulnerable to supply-chain attacks if the tag is moved: actions/checkout@v7.0.0 (line 23), actions/setup-python@v6.3.0 (line 26), actions/cache@v5 (line 31), actions/github-script@v9 (line 51).

Locations:

- `.github/workflows/cve-watcher.yml:23`
- `.github/workflows/cve-watcher.yml:26`
- `.github/workflows/cve-watcher.yml:31`
- `.github/workflows/cve-watcher.yml:51`

### unpinned-uses (severity: high)

docker-nightly.yml references multiple actions by mutable version tags instead of full 40-character commit SHAs: actions/checkout@v7.0.0 (line 20), docker/setup-buildx-action@v4 (line 23), docker/login-action@v4 (line 26), docker/build-push-action@v7 (line 38), aquasecurity/trivy-action@master (line 57) — especially dangerous as @master always tracks the latest commit, github/codeql-action/upload-sarif@v4 (line 64).

Locations:

- `.github/workflows/docker-nightly.yml:20`
- `.github/workflows/docker-nightly.yml:23`
- `.github/workflows/docker-nightly.yml:26`
- `.github/workflows/docker-nightly.yml:38`
- `.github/workflows/docker-nightly.yml:57`
- `.github/workflows/docker-nightly.yml:64`

### unpinned-uses (severity: high)

mcp-security-index.yml references actions by mutable version tags instead of full 40-character commit SHAs: actions/checkout@v7.0.0 (line 24), actions/setup-python@v6.3.0 (line 29).

Locations:

- `.github/workflows/mcp-security-index.yml:24`
- `.github/workflows/mcp-security-index.yml:29`

### unpinned-uses (severity: high)

release.yml references many actions by mutable version tags instead of full 40-character commit SHAs across all its jobs: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master (especially dangerous — tracks latest commit), actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

Locations:

- `.github/workflows/release.yml:47`
- `.github/workflows/release.yml:50`
- `.github/workflows/release.yml:60`
- `.github/workflows/release.yml:75`
- `.github/workflows/release.yml:79`
- `.github/workflows/release.yml:83`
- `.github/workflows/release.yml:96`
- `.github/workflows/release.yml:103`
- `.github/workflows/release.yml:110`
- `.github/workflows/release.yml:130`
- `.github/workflows/release.yml:148`
- `.github/workflows/release.yml:163`
- `.github/workflows/release.yml:175`
- `.github/workflows/release.yml:181`

### unpinned-uses (severity: high)

sync-rule-count.yml references actions by mutable version tags instead of full 40-character commit SHAs: actions/checkout@v7.0.0 (line 26), actions/setup-python@v6.3.0 (line 31).

Locations:

- `.github/workflows/sync-rule-count.yml:26`
- `.github/workflows/sync-rule-count.yml:31`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, missing-permissions, broad-permissions, unpinned-uses

**Notes:**

Fixed all 9 findings across 7 workflow files:

1. script-injection (sync-repo-metadata.yml): Moved `${{ github.repository }}` into env var `REPO`, referenced as `"$REPO"` in shell.

2. script-injection (mcp-security-index.yml): Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env vars `GITHUB_TOKEN` and `REPO`, referenced as `${GITHUB_TOKEN}` and `${REPO}` in shell.

3. missing-permissions (ci.yml): Added `permissions: contents: read` at top-level.

4. broad-permissions (scorecard.yml): Replaced `permissions: read-all` with `permissions: {}` at top-level; job-level permissions remain specific and minimal.

5. unpinned-uses (cve-watcher.yml): Pinned actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9 to full SHAs.

6. unpinned-uses (docker-nightly.yml): Pinned actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4 to full SHAs.

7. unpinned-uses (mcp-security-index.yml): Pinned actions/checkout@v7.0.0, actions/setup-python@v6.3.0 to full SHAs.

8. unpinned-uses (release.yml): Pinned all 12 action references across all jobs to full SHAs (actions/checkout, actions/setup-python, pypa/gh-action-pypi-publish, docker/setup-buildx-action, docker/login-action, docker/build-push-action x2, aquasecurity/trivy-action, actions/attest-build-provenance, sigstore/gh-action-sigstore-python, actions/upload-artifact, actions/download-artifact, softprops/action-gh-release).

9. unpinned-uses (sync-rule-count.yml): Pinned actions/checkout@v7.0.0, actions/setup-python@v6.3.0 to full SHAs.


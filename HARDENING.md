<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.82

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.82** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): `${{ github.repository }}` is directly interpolated inside a `run:` shell command. Line: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. An attacker who can influence the repository name (or who triggers this via workflow_dispatch) could inject shell metacharacters.

Locations:

- `.github/workflows/sync-repo-metadata.yml:30`

### script-injection (severity: high)

Sub-rule (a): `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are directly interpolated inside a `run:` shell command. Line: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any `${{ ... }}` expression directly inside a run: script is a script-injection finding regardless of which context it reads from.

Locations:

- `.github/workflows/mcp-security-index.yml:79`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and its only job (`test`) also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the default repository token permissions, which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all scopes and must be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:9`

### unpinned-uses (severity: high)

Multiple workflow files reference actions by mutable tag or branch instead of a full 40-character commit SHA. Failing references include: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/cache@v6`, `actions/github-script@v9` (cve-watcher.yml); `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4` (docker-nightly.yml); `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2` (link-check.yml); `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0` (mcp-security-index.yml); `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `pypa/gh-action-pypi-publish@v1.14.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3` (release.yml); `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0` (sync-rule-count.yml).

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/link-check.yml:31`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:52`
- `.github/workflows/sync-rule-count.yml:30`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, missing-permissions, broad-permissions, unpinned-uses

**Notes:**

Fixed all 5 findings across 7 workflow files:

1. script-injection (sync-repo-metadata.yml): Moved ${{ github.repository }} into env block as REPO, referenced as $REPO in shell.

2. script-injection (mcp-security-index.yml): Moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env block as GH_TOKEN and REPO, referenced as ${GH_TOKEN} and ${REPO} in shell.

3. missing-permissions (ci.yml): Added top-level 'permissions: contents: read'.

4. broad-permissions (scorecard.yml): Replaced 'permissions: read-all' with specific 'contents: read' and 'actions: read'.

5. unpinned-uses: Pinned all 16 unpinned action references across cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml to full 40-character commit SHAs with original tags preserved as comments.


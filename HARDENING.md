<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.81

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.81** was hardened automatically. 10 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: `${{ github.repository }}` is directly interpolated inside a `run:` shell command string in the 'Update GitHub repo description' step: `gh repo edit "${{ github.repository }}" --description "$desc"`. This allows the repository name to be injected into the shell command before the shell ever sees it.

Locations:

- `.github/workflows/sync-repo-metadata.yml:22`

### script-injection (severity: high)

Rule (a) violation: `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are directly interpolated inside a `run:` shell command string in the 'Publish to gh-pages' step: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any `${{ ... }}` expression inside a run: block is a script-injection finding regardless of context.

Locations:

- `.github/workflows/mcp-security-index.yml:68`

### unpinned-uses (severity: high)

Multiple `uses:` references in cve-watcher.yml are pinned to mutable tags instead of full 40-character commit SHAs: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/cache@v6`, `actions/github-script@v9`.

Locations:

- `.github/workflows/cve-watcher.yml:21`
- `.github/workflows/cve-watcher.yml:25`
- `.github/workflows/cve-watcher.yml:30`
- `.github/workflows/cve-watcher.yml:47`

### unpinned-uses (severity: high)

Multiple `uses:` references in docker-nightly.yml are pinned to mutable tags/branches instead of full 40-character commit SHAs: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7` (twice), `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`.

Locations:

- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/docker-nightly.yml:21`
- `.github/workflows/docker-nightly.yml:25`
- `.github/workflows/docker-nightly.yml:33`
- `.github/workflows/docker-nightly.yml:52`
- `.github/workflows/docker-nightly.yml:60`
- `.github/workflows/docker-nightly.yml:68`

### unpinned-uses (severity: high)

Multiple `uses:` references in link-check.yml are pinned to mutable tags instead of full 40-character commit SHAs: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`.

Locations:

- `.github/workflows/link-check.yml:30`
- `.github/workflows/link-check.yml:33`

### unpinned-uses (severity: high)

Multiple `uses:` references in mcp-security-index.yml are pinned to mutable tags instead of full 40-character commit SHAs: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/mcp-security-index.yml:21`
- `.github/workflows/mcp-security-index.yml:26`

### unpinned-uses (severity: high)

Multiple `uses:` references in release.yml are pinned to mutable tags/branches instead of full 40-character commit SHAs: `actions/checkout@v7.0.1` (multiple jobs), `actions/setup-python@v7.0.0` (multiple jobs), `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7` (twice), `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`.

Locations:

- `.github/workflows/release.yml:48`
- `.github/workflows/release.yml:52`
- `.github/workflows/release.yml:71`
- `.github/workflows/release.yml:75`
- `.github/workflows/release.yml:91`
- `.github/workflows/release.yml:95`
- `.github/workflows/release.yml:111`
- `.github/workflows/release.yml:115`
- `.github/workflows/release.yml:122`
- `.github/workflows/release.yml:131`
- `.github/workflows/release.yml:138`
- `.github/workflows/release.yml:148`
- `.github/workflows/release.yml:155`
- `.github/workflows/release.yml:175`
- `.github/workflows/release.yml:179`
- `.github/workflows/release.yml:195`
- `.github/workflows/release.yml:210`
- `.github/workflows/release.yml:225`
- `.github/workflows/release.yml:240`
- `.github/workflows/release.yml:255`

### unpinned-uses (severity: high)

Multiple `uses:` references in sync-rule-count.yml are pinned to mutable tags instead of full 40-character commit SHAs: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/sync-rule-count.yml:33`
- `.github/workflows/sync-rule-count.yml:38`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and the single job (`test`) also has no `permissions:` key. Without explicit permissions, the workflow inherits the default repository token permissions, which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level, which grants overly broad read access across all scopes. It should be replaced with specific minimal permissions (the job-level permissions already narrow it, but the top-level `read-all` is still a broad-permissions finding).

Locations:

- `.github/workflows/scorecard.yml:11`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 10 findings across 8 workflow files:

1. script-injection (sync-repo-metadata.yml line 22): Moved `${{ github.repository }}` into env block as REPO, referenced as "$REPO" in shell.

2. script-injection (mcp-security-index.yml line 68): Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env block as GH_TOKEN and REPO, referenced as ${GH_TOKEN} and ${REPO} in shell.

3. unpinned-uses (cve-watcher.yml): Pinned actions/checkout@v7.0.1→3d3c42e5, actions/setup-python@v7.0.0→5fda3b95, actions/cache@v6→55cc8345, actions/github-script@v9→3a2844b7.

4. unpinned-uses (docker-nightly.yml): Pinned actions/checkout→3d3c42e5, docker/setup-buildx-action@v4→bb05f3f5, docker/login-action@v4→dbcb8138, docker/build-push-action@v7→53b7df96, aquasecurity/trivy-action@master→d2a0b607, github/codeql-action/upload-sarif@v4→ff2f1c62.

5. unpinned-uses (link-check.yml): Pinned actions/checkout→3d3c42e5, lycheeverse/lychee-action@v2→e7477775.

6. unpinned-uses (mcp-security-index.yml): Pinned actions/checkout→3d3c42e5, actions/setup-python→5fda3b95.

7. unpinned-uses (release.yml): Pinned all 12 action references across all jobs with full SHAs.

8. unpinned-uses (sync-rule-count.yml): Pinned actions/checkout→3d3c42e5, actions/setup-python→5fda3b95.

9. missing-permissions (ci.yml): Added top-level `permissions: contents: read`.

10. broad-permissions (scorecard.yml): Replaced `permissions: read-all` with `permissions: contents: read`.


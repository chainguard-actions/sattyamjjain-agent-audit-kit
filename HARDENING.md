<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.95

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.95** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of full 40-character commit SHA pins. This exposes the pipeline to supply-chain attacks if a tag is moved or a branch is compromised.

ci.yml: `actions/setup-python@v7` (counts job)

cve-deferral-date.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`

cve-watcher.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/cache@v6`, `actions/github-script@v9`

docker-nightly.yml: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`, `actions/github-script@v9`

link-check.yml: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`, `actions/setup-python@v7`

mcp-security-index.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/github-script@v9`

release.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`, `pypa/gh-action-pypi-publish@v1.14.2`

sync-rule-count.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`

Locations:

- `.github/workflows/ci.yml:57`
- `.github/workflows/cve-deferral-date.yml:30`
- `.github/workflows/cve-deferral-date.yml:33`
- `.github/workflows/cve-watcher.yml:30`
- `.github/workflows/cve-watcher.yml:33`
- `.github/workflows/cve-watcher.yml:36`
- `.github/workflows/cve-watcher.yml:47`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/docker-nightly.yml:25`
- `.github/workflows/docker-nightly.yml:28`
- `.github/workflows/docker-nightly.yml:40`
- `.github/workflows/docker-nightly.yml:61`
- `.github/workflows/docker-nightly.yml:70`
- `.github/workflows/docker-nightly.yml:84`
- `.github/workflows/link-check.yml:38`
- `.github/workflows/link-check.yml:41`
- `.github/workflows/link-check.yml:68`
- `.github/workflows/link-check.yml:69`
- `.github/workflows/mcp-security-index.yml:27`
- `.github/workflows/mcp-security-index.yml:30`
- `.github/workflows/mcp-security-index.yml:130`
- `.github/workflows/release.yml:62`
- `.github/workflows/release.yml:65`
- `.github/workflows/release.yml:113`
- `.github/workflows/release.yml:116`
- `.github/workflows/release.yml:155`
- `.github/workflows/release.yml:158`
- `.github/workflows/release.yml:191`
- `.github/workflows/release.yml:194`
- `.github/workflows/release.yml:210`
- `.github/workflows/release.yml:213`
- `.github/workflows/release.yml:232`
- `.github/workflows/release.yml:235`
- `.github/workflows/release.yml:248`
- `.github/workflows/release.yml:251`
- `.github/workflows/release.yml:258`
- `.github/workflows/release.yml:265`
- `.github/workflows/release.yml:270`
- `.github/workflows/release.yml:280`
- `.github/workflows/release.yml:295`
- `.github/workflows/release.yml:302`
- `.github/workflows/sync-rule-count.yml:22`
- `.github/workflows/sync-rule-count.yml:25`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and neither of its jobs (`test`, `counts`) defines job-level permissions. Without explicit permissions, the workflow runs with the default token permissions, which may be overly broad (e.g. write access to contents on push events).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes rather than the minimal specific permissions needed. It should be replaced with specific scopes (e.g. `contents: read`, `security-events: write`, `id-token: write`).

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): mcp-security-index.yml interpolates `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` directly inside a `run:` shell command string. The offending line is:

  git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"

Any `${{ ... }}` expression inside a `run:` block is substituted by the YAML template engine before the shell ever sees the string, bypassing shell quoting. `github.repository` is a `github.*` context value and must be passed via an `env:` variable and referenced as `$GITHUB_REPOSITORY` (which is already available as a default environment variable) rather than interpolated directly.

Locations:

- `.github/workflows/mcp-security-index.yml:119`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all 4 findings across 8 workflow files:

1. unpinned-uses: Pinned all 43 unpinned action references to full 40-char commit SHAs in ci.yml, cve-deferral-date.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. All original tags preserved as comments.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (`contents: read`, `actions: read`).

4. script-injection: In mcp-security-index.yml's 'Publish to gh-pages' step, moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` out of the run: shell string into an env: block (as GH_PAGES_TOKEN and REPO), then referenced them as shell variables ${GH_PAGES_TOKEN} and ${REPO}.


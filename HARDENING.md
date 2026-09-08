<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.96

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.96** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable tags or version strings instead of full 40-character SHA commit hashes, making them vulnerable to supply-chain attacks if the referenced tag is moved or the action is compromised.

Affected references:
- ci.yml: `actions/setup-python@v7`
- cve-deferral-date.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`
- cve-watcher.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/cache@v6`, `actions/github-script@v9`
- docker-nightly.yml: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`, `actions/github-script@v9`
- link-check.yml: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`, `actions/setup-python@v7`
- mcp-security-index.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/github-script@v9`
- release.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `pypa/gh-action-pypi-publish@v1.14.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`
- sync-rule-count.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`

Locations:

- `.github/workflows/ci.yml:63`
- `.github/workflows/cve-deferral-date.yml:30`
- `.github/workflows/cve-deferral-date.yml:34`
- `.github/workflows/cve-watcher.yml:30`
- `.github/workflows/cve-watcher.yml:34`
- `.github/workflows/cve-watcher.yml:38`
- `.github/workflows/cve-watcher.yml:57`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/docker-nightly.yml:26`
- `.github/workflows/docker-nightly.yml:30`
- `.github/workflows/docker-nightly.yml:43`
- `.github/workflows/docker-nightly.yml:64`
- `.github/workflows/docker-nightly.yml:73`
- `.github/workflows/docker-nightly.yml:88`
- `.github/workflows/link-check.yml:37`
- `.github/workflows/link-check.yml:40`
- `.github/workflows/link-check.yml:65`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/mcp-security-index.yml:27`
- `.github/workflows/mcp-security-index.yml:116`
- `.github/workflows/release.yml:68`
- `.github/workflows/release.yml:75`
- `.github/workflows/release.yml:113`
- `.github/workflows/release.yml:117`
- `.github/workflows/release.yml:200`
- `.github/workflows/release.yml:207`
- `.github/workflows/release.yml:247`
- `.github/workflows/release.yml:254`
- `.github/workflows/release.yml:270`
- `.github/workflows/release.yml:277`
- `.github/workflows/release.yml:308`
- `.github/workflows/release.yml:315`
- `.github/workflows/release.yml:323`
- `.github/workflows/release.yml:330`
- `.github/workflows/release.yml:337`
- `.github/workflows/release.yml:344`
- `.github/workflows/release.yml:360`
- `.github/workflows/release.yml:375`
- `.github/workflows/release.yml:395`
- `.github/workflows/release.yml:402`
- `.github/workflows/release.yml:460`
- `.github/workflows/sync-rule-count.yml:22`
- `.github/workflows/sync-rule-count.yml:27`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and neither the `test` job nor the `counts` job defines a job-level `permissions:` block. Without explicit permissions, the workflow runs with the default token permissions (which may include write access to contents, packages, etc.), violating the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets top-level `permissions: read-all`, which grants read access to all repository scopes. This is overly broad and should be replaced with specific minimal permissions (e.g., `contents: read`). The job-level block does narrow some permissions, but the top-level `read-all` still sets an unnecessarily wide baseline.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): mcp-security-index.yml directly interpolates `${{ github.repository }}` inside a `run:` shell command. The expression is embedded in a `git remote add` URL string: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any `${{ ... }}` expression interpolated directly into a `run:` block is a script-injection risk because the value is substituted into the shell command string before the shell parses it. The value should be passed via an `env:` variable and referenced as `$GITHUB_REPOSITORY` instead.

Locations:

- `.github/workflows/mcp-security-index.yml:108`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all 4 findings across 8 workflow files:

1. unpinned-uses: Pinned all 43 unpinned action references to full SHA hashes with tag comments. Files updated: ci.yml, cve-deferral-date.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml.

2. missing-permissions: Added top-level `permissions: contents: read` to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write) matching what the job-level block already used.

4. script-injection: In mcp-security-index.yml, moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` from the git remote add URL in the run: block into the step's env: block as GITHUB_TOKEN and REPOSITORY, then referenced them as shell variables ${GITHUB_TOKEN} and ${REPOSITORY}.


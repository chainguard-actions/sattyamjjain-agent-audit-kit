<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.49

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.49** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use mutable tag or version refs instead of full 40-character SHA commit pins, making them vulnerable to supply-chain attacks if the referenced action is compromised or its tag is moved.

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9
docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4
mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0
release.yml: actions/checkout@v7.0.0 (×4 jobs), actions/setup-python@v6.3.0 (×3), pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3
sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:53`
- `.github/workflows/sync-rule-count.yml:28`

### script-injection (severity: high)

Two workflow run: blocks directly interpolate ${{ }} expressions into shell command strings, violating rule (a). This allows template substitution to inject arbitrary shell metacharacters before the shell parses the command.

1. .github/workflows/sync-repo-metadata.yml — the 'Update GitHub repo description' step interpolates ${{ github.repository }} directly inside a run: shell command: `gh repo edit "${{ github.repository }}" --description "$desc"`. Although github.repository is typically safe, any ${{ }} expression inside a run: block is a script-injection finding per the check rules.

2. .github/workflows/mcp-security-index.yml — the 'Publish to gh-pages' step interpolates both ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} directly inside a run: shell command: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`

Locations:

- `.github/workflows/sync-repo-metadata.yml:26`
- `.github/workflows/mcp-security-index.yml:72`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: key and no job-level permissions: key on its only job ('test'). Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad (write access to contents and other scopes depending on repository settings).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all available scopes and is considered overly broad. It should be replaced with specific minimal permissions (e.g., contents: read, security-events: write) at the job level, which the file already does for the analysis job — the top-level read-all is redundant and overly permissive.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, missing-permissions, broad-permissions

**Notes:**

Fixed all four finding types:

1. unpinned-uses: Pinned all mutable action refs to full SHA in cve-watcher.yml (checkout@v7.0.0→9c091bb, setup-python@v6.3.0→ece7cb0, cache@v5→caa2961, github-script@v9→3a2844b), docker-nightly.yml (checkout, setup-buildx-action@v4→bb05f3f, login-action@v4→af1e73f, build-push-action@v7→53b7df9, trivy-action@master→c07df6f, codeql-action/upload-sarif@v4→7188fc3), mcp-security-index.yml (checkout, setup-python), release.yml (checkout×4, setup-python×2, pypa/gh-action-pypi-publish@v1.14.0→cef2210, setup-buildx-action, login-action, build-push-action×2, trivy-action, attest-build-provenance@v4→0f67c3f, sigstore/gh-action-sigstore-python@v3.4.0→5b79a39, upload-artifact@v7→043fb46, download-artifact@v8→3e5f45b, softprops/action-gh-release@v3→3d0d988), sync-rule-count.yml (checkout, setup-python).

2. script-injection: In sync-repo-metadata.yml moved ${{ github.repository }} to REPO_NAME env var. In mcp-security-index.yml moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} to GITHUB_TOKEN and GITHUB_REPOSITORY env vars.

3. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

4. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml.


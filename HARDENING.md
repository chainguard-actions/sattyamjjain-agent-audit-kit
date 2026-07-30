<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.63

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.63** was hardened automatically. 4 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable tag or branch refs instead of full 40-character SHA commit pins, making them vulnerable to supply-chain attacks if the referenced tag is moved or the action is compromised.

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v6, actions/github-script@v9
docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4
mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0
release.yml: actions/checkout@v7.0.0 (×4), actions/setup-python@v6.3.0 (×2), docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3
sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/cve-watcher.yml:24`
- `.github/workflows/cve-watcher.yml:29`
- `.github/workflows/cve-watcher.yml:50`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/docker-nightly.yml:21`
- `.github/workflows/docker-nightly.yml:27`
- `.github/workflows/docker-nightly.yml:40`
- `.github/workflows/docker-nightly.yml:57`
- `.github/workflows/docker-nightly.yml:66`
- `.github/workflows/mcp-security-index.yml:24`
- `.github/workflows/mcp-security-index.yml:29`
- `.github/workflows/release.yml:37`
- `.github/workflows/release.yml:57`
- `.github/workflows/release.yml:67`
- `.github/workflows/release.yml:75`
- `.github/workflows/release.yml:82`
- `.github/workflows/release.yml:88`
- `.github/workflows/release.yml:100`
- `.github/workflows/release.yml:107`
- `.github/workflows/release.yml:116`
- `.github/workflows/release.yml:130`
- `.github/workflows/release.yml:143`
- `.github/workflows/release.yml:155`
- `.github/workflows/release.yml:163`
- `.github/workflows/release.yml:175`
- `.github/workflows/release.yml:185`
- `.github/workflows/release.yml:196`
- `.github/workflows/sync-rule-count.yml:24`
- `.github/workflows/sync-rule-count.yml:29`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and its single job (`test`) also has no job-level `permissions:` key. This means the workflow runs with the default GitHub token permissions, which may be broader than necessary (e.g., write access to contents and packages by default on some repository configurations).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level, granting read access to all repository scopes. This is overly broad and should be replaced with specific minimal permissions (e.g., `security-events: write`, `id-token: write`, `contents: read`).

Locations:

- `.github/workflows/scorecard.yml:8`

### script-injection (severity: high)

Rule (a) violation: GitHub Actions expressions are interpolated directly inside `run:` shell command strings, bypassing shell quoting and allowing template-substituted values to be parsed as shell syntax before the shell ever sees them.

1. sync-repo-metadata.yml: `gh repo edit "${{ github.repository }}" --description "$desc"` — `${{ github.repository }}` is expanded by the Actions template engine directly into the shell command string.

2. mcp-security-index.yml: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly into the shell command string inside a `run:` block.

Locations:

- `.github/workflows/sync-repo-metadata.yml:30`
- `.github/workflows/mcp-security-index.yml:77`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings across six workflow files:

1. unpinned-uses: Pinned all action references to full 40-char SHAs in cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. SHAs resolved via lookup_action_sha for: actions/checkout@v7.0.0 (9c091bb), actions/setup-python@v6.3.0 (ece7cb0), actions/cache@v6 (55cc834), actions/github-script@v9 (3a2844b), docker/setup-buildx-action@v4 (bb05f3f), docker/login-action@v4 (dbcb813), docker/build-push-action@v7 (53b7df9), aquasecurity/trivy-action@master (c07df6f), github/codeql-action/upload-sarif@v4 (f205ea1), actions/attest-build-provenance@v4 (0f67c3f), sigstore/gh-action-sigstore-python@v3.4.0 (5b79a39), pypa/gh-action-pypi-publish@v1.14.0 (cef2210), actions/upload-artifact@v7 (043fb46), actions/download-artifact@v8 (3e5f45b), softprops/action-gh-release@v3 (3d0d988).

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write).

4. script-injection: (a) sync-repo-metadata.yml: moved `${{ github.repository }}` into env block as REPO, referenced as "$REPO" in shell. (b) mcp-security-index.yml: moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env block as GITHUB_TOKEN and GITHUB_REPOSITORY, referenced as shell env vars in the git remote add command.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Fixed the 'Extract version from tag' step in .github/workflows/release.yml (line 97). The step previously wrote `${GITHUB_REF_NAME#v}` directly to $GITHUB_OUTPUT. The fix sanitizes the value using `safe=$(printf '%s' "${GITHUB_REF_NAME#v}" | tr -d '\n\r')` before writing `version=${safe}` to $GITHUB_OUTPUT, preventing a tag name with embedded newlines from injecting arbitrary key=value pairs into the GitHub Actions output context.


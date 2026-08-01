<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.65

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.65** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Direct expression interpolation inside run: blocks. In sync-repo-metadata.yml, `${{ github.repository }}` is interpolated directly into a shell command (`gh repo edit "${{ github.repository }}" ...`). In mcp-security-index.yml, both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly into a shell command (`git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`). Any ${{ ... }} expression inside a run: block is a script-injection risk because the value is substituted by the YAML template engine before the shell ever sees it, bypassing shell quoting. These should be passed via env: variables instead.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:86`

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions by mutable version tags or branch names instead of immutable full 40-character SHA digests, making them vulnerable to supply-chain attacks if the referenced tag is moved or the action is compromised.

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v6, actions/github-script@v9

docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

release.yml: actions/checkout@v7.0.0 (×4), actions/setup-python@v6.3.0 (×3), pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/mcp-security-index.yml:25`
- `.github/workflows/release.yml:47`
- `.github/workflows/sync-rule-count.yml:24`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: key and the single job (test) also has no job-level permissions: key. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be broader than necessary (e.g., write access to contents). All workflow files should declare minimal explicit permissions.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`, `id-token: write`) scoped to only what the workflow actually needs.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. script-injection: In sync-repo-metadata.yml, moved ${{ github.repository }} to an env: variable REPO and referenced it as $REPO in the run: block. In mcp-security-index.yml, moved both ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} to env: variables GH_TOKEN and REPO, referencing them as ${GH_TOKEN} and ${REPO} in the shell script.

2. unpinned-uses: Pinned all unpinned actions to full 40-character SHA digests with tag comments across cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. SHAs resolved via lookup_action_sha for: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v6, actions/github-script@v9, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, pypa/gh-action-pypi-publish@v1.14.0, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

3. missing-permissions: Added 'permissions: contents: read' top-level block to ci.yml.

4. broad-permissions: Replaced 'permissions: read-all' in scorecard.yml with specific minimal permissions: contents: read, security-events: write, id-token: write.


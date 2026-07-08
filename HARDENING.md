<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.47

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **sattyamjjain--agent-audit-kit/v0.3.47** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use tag-based or branch-based action references instead of pinned 40-character SHA commits, making them vulnerable to supply-chain attacks. Failing references include: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, pypa/gh-action-pypi-publish@v1.14.0, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

Locations:

- `.github/workflows/cve-watcher.yml:14`
- `.github/workflows/docker-nightly.yml:16`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:47`
- `.github/workflows/sync-rule-count.yml:27`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions key and no job-level permissions key on any job. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets top-level permissions to read-all, which grants overly broad read access across all scopes. It should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Rule (a): ${{ github.repository }} is interpolated directly inside a run: shell command. In sync-repo-metadata.yml, the offending line is: gh repo edit "${{ github.repository }}" --description "$desc" || true. In mcp-security-index.yml, the offending line is: git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git". Both expressions flow through YAML template substitution before the shell sees them, enabling script injection.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:72`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all findings: (1) unpinned-uses: Pinned all tag/branch-based action references to full 40-char SHAs in cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml. Actions pinned: actions/checkout@v7.0.0→9c091bb, actions/setup-python@v6.3.0→ece7cb0, actions/cache@v5→caa2961, actions/github-script@v9→3a2844b, docker/setup-buildx-action@v4→bb05f3f, docker/login-action@v4→af1e73f, docker/build-push-action@v7→53b7df9, aquasecurity/trivy-action@master→c07df6f, github/codeql-action/upload-sarif@v4→54f647b, pypa/gh-action-pypi-publish@v1.14.0→cef2210, actions/attest-build-provenance@v4→0f67c3f, sigstore/gh-action-sigstore-python@v3.4.0→5b79a39, actions/upload-artifact@v7→043fb46, actions/download-artifact@v8→3e5f45b, softprops/action-gh-release@v3→718ea10. (2) missing-permissions: Added 'permissions: contents: read' top-level block to ci.yml. (3) broad-permissions: Replaced 'permissions: read-all' with specific 'contents: read' and 'actions: read' in scorecard.yml. (4) script-injection: In sync-repo-metadata.yml, moved ${{ github.repository }} into env block as GITHUB_REPOSITORY and referenced it as $GITHUB_REPOSITORY in the shell command. In mcp-security-index.yml, moved both ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env block and referenced them as ${GITHUB_TOKEN} and ${GITHUB_REPOSITORY} in the shell command.


<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.89

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.89** was hardened automatically. 9 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

ci.yml uses actions/setup-python@v6 (tag ref, not a SHA) in the 'counts' job. All uses: references must be pinned to a full 40-character commit SHA to prevent supply-chain attacks.

Locations:

- `.github/workflows/ci.yml:54`

### unpinned-uses (severity: high)

cve-watcher.yml uses multiple unpinned action refs: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9. All uses: references must be pinned to a full 40-character commit SHA.

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/cve-watcher.yml:25`
- `.github/workflows/cve-watcher.yml:29`
- `.github/workflows/cve-watcher.yml:56`

### unpinned-uses (severity: high)

docker-nightly.yml uses multiple unpinned action refs: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, actions/github-script@v9. All uses: references must be pinned to a full 40-character commit SHA.

Locations:

- `.github/workflows/docker-nightly.yml:28`
- `.github/workflows/docker-nightly.yml:31`
- `.github/workflows/docker-nightly.yml:37`
- `.github/workflows/docker-nightly.yml:44`
- `.github/workflows/docker-nightly.yml:57`
- `.github/workflows/docker-nightly.yml:65`
- `.github/workflows/docker-nightly.yml:82`

### unpinned-uses (severity: high)

link-check.yml uses multiple unpinned action refs: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2, actions/setup-python@v6. All uses: references must be pinned to a full 40-character commit SHA.

Locations:

- `.github/workflows/link-check.yml:38`
- `.github/workflows/link-check.yml:41`
- `.github/workflows/link-check.yml:57`
- `.github/workflows/link-check.yml:58`

### unpinned-uses (severity: high)

mcp-security-index.yml uses multiple unpinned action refs: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/github-script@v9. All uses: references must be pinned to a full 40-character commit SHA.

Locations:

- `.github/workflows/mcp-security-index.yml:28`
- `.github/workflows/mcp-security-index.yml:31`
- `.github/workflows/mcp-security-index.yml:88`

### unpinned-uses (severity: high)

release.yml uses many unpinned action refs: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3. All uses: references must be pinned to a full 40-character commit SHA.

Locations:

- `.github/workflows/release.yml:55`
- `.github/workflows/release.yml:59`
- `.github/workflows/release.yml:113`
- `.github/workflows/release.yml:117`
- `.github/workflows/release.yml:163`
- `.github/workflows/release.yml:167`
- `.github/workflows/release.yml:200`
- `.github/workflows/release.yml:210`
- `.github/workflows/release.yml:220`
- `.github/workflows/release.yml:228`
- `.github/workflows/release.yml:243`
- `.github/workflows/release.yml:260`
- `.github/workflows/release.yml:275`
- `.github/workflows/release.yml:283`
- `.github/workflows/release.yml:295`
- `.github/workflows/release.yml:310`
- `.github/workflows/release.yml:330`
- `.github/workflows/release.yml:340`
- `.github/workflows/release.yml:360`

### unpinned-uses (severity: high)

sync-rule-count.yml uses unpinned action refs: actions/checkout@v7.0.1, actions/setup-python@v7.0.0. All uses: references must be pinned to a full 40-character commit SHA.

Locations:

- `.github/workflows/sync-rule-count.yml:28`
- `.github/workflows/sync-rule-count.yml:33`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: block and neither of its jobs (test, counts) defines a job-level permissions: block. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets top-level permissions: read-all, which grants read access to all repository scopes. This should be replaced with specific minimal permissions required by each job.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 9 findings across 7 workflow files:

1. ci.yml: Added top-level 'permissions: contents: read' block (missing-permissions). Pinned actions/setup-python@v6 → SHA ece7cb06caefa5fff74198d8649806c4678c61a1 (unpinned-uses).

2. cve-watcher.yml: Pinned actions/checkout@v7.0.1 → 3d3c42e5aac5ba805825da76410c181273ba90b1, actions/setup-python@v7.0.0 → 5fda3b95a4ea91299a34e894583c3862153e4b97, actions/cache@v6 → 55cc8345863c7cc4c66a329aec7e433d2d1c52a9, actions/github-script@v9 → 3a2844b7e9c422d3c10d287c895573f7108da1b3.

3. docker-nightly.yml: Pinned checkout, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, actions/github-script@v9 to full SHAs.

4. link-check.yml: Pinned both checkout instances, lycheeverse/lychee-action@v2, and actions/setup-python@v6 to full SHAs.

5. mcp-security-index.yml: Pinned checkout, setup-python, and github-script to full SHAs.

6. release.yml: Pinned all 19 unpinned action references including checkout (×8), setup-python (×7), pypa/gh-action-pypi-publish@v1.14.2, docker actions, trivy-action, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

7. sync-rule-count.yml: Pinned checkout and setup-python to full SHAs.

8. scorecard.yml: Replaced broad 'permissions: read-all' with specific minimal permissions (contents: read, actions: read). Job-level permissions already had specific write scopes.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in .github/workflows/mcp-security-index.yml at the 'Publish to gh-pages' step. Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` out of the run: shell string and into an env: block as GH_TOKEN and GITHUB_REPOSITORY respectively. The git remote add origin command now references them as ${GH_TOKEN} and ${GITHUB_REPOSITORY} shell variables, preventing template-engine substitution before the shell sees the command.


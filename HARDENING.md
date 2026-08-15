<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.78

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.78** was hardened automatically. 10 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} are directly interpolated inside a run: shell command string in the 'Publish to gh-pages' step. The line reads: git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git". Any ${{ ... }} expression inside a run: block is a script-injection risk because the value is substituted into the shell command before the shell parses it.

Locations:

- `.github/workflows/mcp-security-index.yml:71`

### script-injection (severity: high)

Sub-rule (a): ${{ github.repository }} is directly interpolated inside a run: shell command string in the 'Update GitHub repo description' step. The line reads: gh repo edit "${{ github.repository }}" --description "$desc". Any ${{ ... }} expression inside a run: block is a script-injection risk because the value is substituted into the shell command before the shell parses it.

Locations:

- `.github/workflows/sync-repo-metadata.yml:27`

### unpinned-uses (severity: high)

Multiple uses: references in this workflow use mutable tag/version refs instead of immutable 40-character SHA digests, making the workflow vulnerable to supply-chain attacks if the referenced action is compromised or the tag is moved. Failing references: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9.

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/cve-watcher.yml:25`
- `.github/workflows/cve-watcher.yml:30`
- `.github/workflows/cve-watcher.yml:40`

### unpinned-uses (severity: high)

Multiple uses: references in this workflow use mutable tag/version refs instead of immutable 40-character SHA digests. Failing references: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (twice), aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4.

Locations:

- `.github/workflows/docker-nightly.yml:20`
- `.github/workflows/docker-nightly.yml:23`
- `.github/workflows/docker-nightly.yml:27`
- `.github/workflows/docker-nightly.yml:41`
- `.github/workflows/docker-nightly.yml:55`
- `.github/workflows/docker-nightly.yml:63`
- `.github/workflows/docker-nightly.yml:70`

### unpinned-uses (severity: high)

Multiple uses: references in this workflow use mutable tag/version refs instead of immutable 40-character SHA digests. Failing references: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2.

Locations:

- `.github/workflows/link-check.yml:30`
- `.github/workflows/link-check.yml:33`

### unpinned-uses (severity: high)

Multiple uses: references in this workflow use mutable tag/version refs instead of immutable 40-character SHA digests. Failing references: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

Locations:

- `.github/workflows/mcp-security-index.yml:23`
- `.github/workflows/mcp-security-index.yml:27`

### unpinned-uses (severity: high)

Multiple uses: references in this workflow use mutable tag/version refs instead of immutable 40-character SHA digests. Failing references: actions/checkout@v7.0.1 (multiple jobs), actions/setup-python@v7.0.0 (multiple jobs), pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (twice), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

Locations:

- `.github/workflows/release.yml:50`
- `.github/workflows/release.yml:55`
- `.github/workflows/release.yml:100`
- `.github/workflows/release.yml:105`
- `.github/workflows/release.yml:121`
- `.github/workflows/release.yml:126`
- `.github/workflows/release.yml:148`
- `.github/workflows/release.yml:153`
- `.github/workflows/release.yml:160`
- `.github/workflows/release.yml:168`
- `.github/workflows/release.yml:177`
- `.github/workflows/release.yml:185`
- `.github/workflows/release.yml:200`
- `.github/workflows/release.yml:215`
- `.github/workflows/release.yml:232`
- `.github/workflows/release.yml:237`
- `.github/workflows/release.yml:248`
- `.github/workflows/release.yml:265`
- `.github/workflows/release.yml:285`
- `.github/workflows/release.yml:295`
- `.github/workflows/release.yml:310`
- `.github/workflows/release.yml:330`

### unpinned-uses (severity: high)

Multiple uses: references in this workflow use mutable tag/version refs instead of immutable 40-character SHA digests. Failing references: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

Locations:

- `.github/workflows/sync-rule-count.yml:28`
- `.github/workflows/sync-rule-count.yml:33`

### missing-permissions (severity: medium)

The workflow file has no top-level permissions: key and no job-level permissions: key on any job. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents by default in many configurations). Explicit minimal permissions should be declared.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow sets top-level permissions: read-all, which grants read access to all repository scopes. This is overly broad and should be replaced with specific minimal permissions (e.g., contents: read, security-events: write) scoped to what each job actually needs.

Locations:

- `.github/workflows/scorecard.yml:7`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 10 findings across 9 workflow files:

1. script-injection (mcp-security-index.yml): Moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} from run: shell string into env: block as GH_TOKEN and GH_REPOSITORY.

2. script-injection (sync-repo-metadata.yml): Moved ${{ github.repository }} from run: shell string into env: block as GH_REPOSITORY.

3. unpinned-uses (cve-watcher.yml): Pinned actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9 to full commit SHAs.

4. unpinned-uses (docker-nightly.yml): Pinned actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4 to full commit SHAs.

5. unpinned-uses (link-check.yml): Pinned actions/checkout@v7.0.1 and lycheeverse/lychee-action@v2 to full commit SHAs.

6. unpinned-uses (mcp-security-index.yml): Pinned actions/checkout@v7.0.1 and actions/setup-python@v7.0.0 to full commit SHAs.

7. unpinned-uses (release.yml): Pinned all 13 action references across all jobs to full commit SHAs.

8. unpinned-uses (sync-rule-count.yml): Pinned actions/checkout@v7.0.1 and actions/setup-python@v7.0.0 to full commit SHAs.

9. missing-permissions (ci.yml): Added top-level permissions: contents: read.

10. broad-permissions (scorecard.yml): Replaced permissions: read-all with specific minimal permissions: contents: read, security-events: write, id-token: write.


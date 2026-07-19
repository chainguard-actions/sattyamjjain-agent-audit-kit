<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.47

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.47** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of pinned 40-character SHA digests, making them vulnerable to supply-chain attacks.

.github/workflows/cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9

.github/workflows/docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

.github/workflows/mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

.github/workflows/release.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

.github/workflows/sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:14`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/mcp-security-index.yml:23`
- `.github/workflows/release.yml:44`
- `.github/workflows/sync-rule-count.yml:24`

### missing-permissions (severity: medium)

The workflow file ci.yml has no top-level `permissions:` key and the single job `test` also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow file scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions required by each job.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): GitHub Actions expressions are interpolated directly inside `run:` shell command strings, allowing template substitution before the shell processes the value.

1. In sync-repo-metadata.yml, the step 'Update GitHub repo description' contains: `gh repo edit "${{ github.repository }}" --description "$desc"`. The `${{ github.repository }}` expression is expanded by the Actions runner before the shell sees the command, enabling injection of shell metacharacters.

2. In mcp-security-index.yml, the step 'Publish to gh-pages' contains: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. The `${{ github.repository }}` expression is interpolated directly into the shell command string.

Locations:

- `.github/workflows/sync-repo-metadata.yml:26`
- `.github/workflows/mcp-security-index.yml:75`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all mutable action references to full 40-char SHAs across 5 workflow files (cve-watcher.yml, docker-nightly.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml). Actions pinned: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3, pypa/gh-action-pypi-publish@v1.14.0.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml. Job-level permissions already specify the minimal required permissions.

4. script-injection: Fixed two injection points: (a) sync-repo-metadata.yml - moved ${{ github.repository }} into env: block as REPOSITORY; (b) mcp-security-index.yml - moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env: block as GITHUB_TOKEN and REPOSITORY, referencing them as shell variables in the run: block.


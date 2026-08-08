<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.69

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.69** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of full 40-character SHA digests, making them vulnerable to supply-chain attacks.

release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0 (multiple), pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (multiple), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4.

cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9.

mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0.

Locations:

- `.github/workflows/release.yml:53`
- `.github/workflows/release.yml:60`
- `.github/workflows/release.yml:100`
- `.github/workflows/release.yml:107`
- `.github/workflows/release.yml:118`
- `.github/workflows/release.yml:130`
- `.github/workflows/release.yml:136`
- `.github/workflows/release.yml:141`
- `.github/workflows/release.yml:152`
- `.github/workflows/release.yml:157`
- `.github/workflows/release.yml:176`
- `.github/workflows/release.yml:196`
- `.github/workflows/release.yml:210`
- `.github/workflows/release.yml:217`
- `.github/workflows/release.yml:232`
- `.github/workflows/release.yml:249`
- `.github/workflows/release.yml:264`
- `.github/workflows/release.yml:278`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/docker-nightly.yml:27`
- `.github/workflows/docker-nightly.yml:33`
- `.github/workflows/docker-nightly.yml:39`
- `.github/workflows/docker-nightly.yml:56`
- `.github/workflows/docker-nightly.yml:72`
- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/cve-watcher.yml:25`
- `.github/workflows/cve-watcher.yml:30`
- `.github/workflows/cve-watcher.yml:51`
- `.github/workflows/mcp-security-index.yml:24`
- `.github/workflows/mcp-security-index.yml:29`
- `.github/workflows/sync-rule-count.yml:30`
- `.github/workflows/sync-rule-count.yml:36`

### script-injection (severity: high)

Sub-rule (a): GitHub Actions expressions (${{ ... }}) are interpolated directly inside run: shell command strings, allowing template substitution before the shell processes the value.

In sync-repo-metadata.yml, the 'Update GitHub repo description' step uses `gh repo edit "${{ github.repository }}"` directly in a run: block. While github.repository is not attacker-controlled in the same way as github.head_ref, any ${{ }} expression inside a run: block is a script-injection finding per the check rules.

In mcp-security-index.yml, the 'Publish to gh-pages' step uses `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` directly in a run: block. Both ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} are interpolated into the shell command string before the shell executes it.

Locations:

- `.github/workflows/sync-repo-metadata.yml:22`
- `.github/workflows/mcp-security-index.yml:72`

### missing-permissions (severity: medium)

The workflow file ci.yml has no top-level `permissions:` key and the single job ('test') also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad (e.g., write access to contents). This workflow runs on pull_request events, making it especially important to restrict permissions.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow file scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes rather than the minimal set required. The job-level permissions block correctly narrows to specific scopes (security-events: write, id-token: write, contents: read), but the top-level read-all is still overly broad and should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:7`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all action references to full 40-char SHAs in release.yml (actions/checkout, actions/setup-python, pypa/gh-action-pypi-publish, docker/setup-buildx-action, docker/login-action, docker/build-push-action x2, aquasecurity/trivy-action, actions/attest-build-provenance, sigstore/gh-action-sigstore-python, actions/upload-artifact, actions/download-artifact, softprops/action-gh-release, actions/setup-python), docker-nightly.yml (actions/checkout, docker/setup-buildx-action, docker/login-action, docker/build-push-action, aquasecurity/trivy-action, github/codeql-action/upload-sarif), cve-watcher.yml (actions/checkout, actions/setup-python, actions/cache, actions/github-script), mcp-security-index.yml (actions/checkout, actions/setup-python), and sync-rule-count.yml (actions/checkout, actions/setup-python).

2. script-injection: In sync-repo-metadata.yml, moved ${{ github.repository }} into env: block as GH_REPOSITORY. In mcp-security-index.yml, moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env: block as GH_TOKEN and GH_REPOSITORY, with shell script referencing them as ${GH_TOKEN} and ${GH_REPOSITORY}.

3. missing-permissions: Added 'permissions: contents: read' top-level block to ci.yml.

4. broad-permissions: Replaced 'permissions: read-all' in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write) matching what the job actually uses.


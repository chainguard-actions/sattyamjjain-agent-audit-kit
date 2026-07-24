<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.26

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.26** was hardened automatically. 4 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable tag/version refs instead of full 40-character commit SHA pins, making them vulnerable to supply-chain attacks if the referenced tag is moved.

release.yml: actions/checkout@v6.0.2, actions/setup-python@v6.2.0, pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.3.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

docker-nightly.yml: actions/checkout@v6.0.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

cve-watcher.yml: actions/checkout@v6.0.2, actions/setup-python@v6.2.0, actions/cache@v5, actions/github-script@v9

mcp-security-index.yml: actions/checkout@v6.0.2, actions/setup-python@v6.2.0

sync-rule-count.yml: actions/checkout@v6.0.2, actions/setup-python@v6.2.0

Locations:

- `.github/workflows/release.yml:44`
- `.github/workflows/release.yml:47`
- `.github/workflows/release.yml:55`
- `.github/workflows/release.yml:67`
- `.github/workflows/release.yml:72`
- `.github/workflows/release.yml:76`
- `.github/workflows/release.yml:84`
- `.github/workflows/release.yml:91`
- `.github/workflows/release.yml:100`
- `.github/workflows/release.yml:116`
- `.github/workflows/release.yml:131`
- `.github/workflows/release.yml:138`
- `.github/workflows/release.yml:155`
- `.github/workflows/release.yml:168`
- `.github/workflows/release.yml:183`
- `.github/workflows/release.yml:185`
- `.github/workflows/release.yml:188`
- `.github/workflows/docker-nightly.yml:21`
- `.github/workflows/docker-nightly.yml:24`
- `.github/workflows/docker-nightly.yml:28`
- `.github/workflows/docker-nightly.yml:40`
- `.github/workflows/docker-nightly.yml:57`
- `.github/workflows/docker-nightly.yml:66`
- `.github/workflows/cve-watcher.yml:19`
- `.github/workflows/cve-watcher.yml:23`
- `.github/workflows/cve-watcher.yml:28`
- `.github/workflows/cve-watcher.yml:55`
- `.github/workflows/mcp-security-index.yml:21`
- `.github/workflows/mcp-security-index.yml:25`
- `.github/workflows/sync-rule-count.yml:24`
- `.github/workflows/sync-rule-count.yml:29`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and its only job (`test`) also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be broader than necessary.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:8`

### script-injection (severity: high)

Sub-rule (a): sync-repo-metadata.yml directly interpolates `${{ github.repository }}` inside a `run:` shell command: `gh repo edit "${{ github.repository }}" --description "$desc"`. Any `${{ ... }}` expression inside a run: block is substituted by the Actions template engine before the shell parses the string, allowing an attacker who can influence the context value to inject shell metacharacters.

Locations:

- `.github/workflows/sync-repo-metadata.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all 15 unique action references across release.yml, docker-nightly.yml, cve-watcher.yml, mcp-security-index.yml, and sync-rule-count.yml to full 40-character commit SHAs using lookup_action_sha. Each pin retains the original tag as a comment (e.g., '# v6.0.2').

2. missing-permissions: Added 'permissions: contents: read' top-level block to ci.yml, which had no permissions key at all.

3. broad-permissions: Replaced 'permissions: read-all' in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write) that match exactly what the job-level already specified.

4. script-injection: In sync-repo-metadata.yml, moved '${{ github.repository }}' from inside the run: shell command into an env: block as REPO, then referenced it as "$REPO" in the shell script to prevent template injection.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Publish to gh-pages' step of .github/workflows/mcp-security-index.yml. Moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} out of the run: shell command string into an env: block as GH_TOKEN and GH_REPOSITORY respectively. The shell script now references these as plain environment variables (${GH_TOKEN} and ${GH_REPOSITORY}), preventing YAML template substitution from injecting attacker-controlled values directly into the shell command.


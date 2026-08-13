<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.74

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.74** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): ${{ github.repository }} (a github.* context expression) is interpolated directly inside a run: shell command string. In sync-repo-metadata.yml the offending line is: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. In mcp-security-index.yml the offending line is: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Both expressions are substituted by the YAML template engine before the shell ever sees them, allowing injection of shell metacharacters if the repository name were attacker-influenced.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:79`

### unpinned-uses (severity: high)

Multiple workflow files reference actions by mutable version tags or branch names instead of full 40-character commit SHAs, making them vulnerable to supply-chain attacks if the referenced tag or branch is moved.

cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9

docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2

mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

release.yml: actions/checkout@v7.0.1 (multiple jobs), actions/setup-python@v7.0.0 (multiple jobs), docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (twice), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, pypa/gh-action-pypi-publish@v1.14.2, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

Locations:

- `.github/workflows/cve-watcher.yml:21`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/link-check.yml:33`
- `.github/workflows/mcp-security-index.yml:23`
- `.github/workflows/release.yml:56`
- `.github/workflows/sync-rule-count.yml:33`

### missing-permissions (severity: medium)

ci.yml has no top-level permissions: key and the single job 'test' also has no job-level permissions: key. Without explicit permissions the workflow inherits the repository default (typically contents: write for the default branch), granting broader access than necessary.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets top-level `permissions: read-all`, which grants read access to all repository scopes. This is overly broad and should be replaced with specific minimal permissions (e.g. security-events: write, id-token: write, contents: read) matching only what the workflow actually needs.

Locations:

- `.github/workflows/scorecard.yml:10`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all four findings:

1. script-injection: In sync-repo-metadata.yml, moved `${{ github.repository }}` into an env var `REPO` and referenced it as `$REPO` in the shell. In mcp-security-index.yml, moved both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env vars `GH_TOKEN` and `REPO`, referencing them as `${GH_TOKEN}` and `${REPO}` in the git remote URL.

2. unpinned-uses: Pinned all mutable tag/branch references to full 40-char SHAs with tag comments preserved:
   - actions/checkout@v7.0.1 → @3d3c42e5aac5ba805825da76410c181273ba90b1
   - actions/setup-python@v7.0.0 → @5fda3b95a4ea91299a34e894583c3862153e4b97
   - actions/cache@v6 → @55cc8345863c7cc4c66a329aec7e433d2d1c52a9
   - actions/github-script@v9 → @3a2844b7e9c422d3c10d287c895573f7108da1b3
   - docker/setup-buildx-action@v4 → @bb05f3f5519dd87d3ba754cc423b652a5edd6d2c
   - docker/login-action@v4 → @dbcb813823bdd20940b903addbd779551569679f
   - docker/build-push-action@v7 → @53b7df96c91f9c12dcc8a07bcb9ccacbed38856a
   - aquasecurity/trivy-action@master → @2736533278103862a861f4a35ebac3e97854d956
   - github/codeql-action/upload-sarif@v4 → @5595ccaf912efad79be6eef63a5619ff05969be3
   - lycheeverse/lychee-action@v2 → @e7477775783ea5526144ba13e8db5eec57747ce8
   - actions/attest-build-provenance@v4 → @4d101475d8b20a2381f78447822ac1eab6504dd8
   - pypa/gh-action-pypi-publish@v1.14.2 → @dc37677b2e1c63e2034f94d8a5b11f265b73ba33
   - sigstore/gh-action-sigstore-python@v3.5.0 → @790bc6befb9d733738f18d8f895854b453640ec9
   - actions/upload-artifact@v7 → @043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
   - actions/download-artifact@v8 → @3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c
   - softprops/action-gh-release@v3 → @3d0d9888cb7fd7b750713d6e236d1fcb99157228

3. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

4. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: `contents: read`, `security-events: write`, `id-token: write`.


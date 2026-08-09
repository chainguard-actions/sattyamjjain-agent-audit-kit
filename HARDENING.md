<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.71

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.71** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of immutable 40-character SHA digests, making them vulnerable to supply-chain attacks.

cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9
docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master (branch ref!), github/codeql-action/upload-sarif@v4
link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2
mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0
release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master (branch ref!), actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3, actions/setup-python@v7.0.0
sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

Locations:

- `.github/workflows/cve-watcher.yml:21`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/link-check.yml:29`
- `.github/workflows/mcp-security-index.yml:19`
- `.github/workflows/release.yml:97`
- `.github/workflows/sync-rule-count.yml:29`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and its single job (`test`) also has no job-level `permissions:` key. Without an explicit permissions block the workflow runs with the default (broad) GITHUB_TOKEN permissions, which include write access to contents and other scopes depending on repository settings.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets top-level `permissions: read-all`, which grants read access to all repository scopes. This is overly broad and should be replaced with the specific minimal permissions required (e.g., `security-events: write`, `id-token: write`, `contents: read`).

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Rule (a) violation: `${{ github.repository }}` is interpolated directly inside a `run:` shell command. The YAML template engine substitutes this value before the shell parses the command, so a repository name containing shell metacharacters could inject arbitrary commands.

Offending line: `gh repo edit "${{ github.repository }}" --description "$desc" || true`

Fix: pass the value via an `env:` variable and reference it as `"$REPO"` in the shell script.

Locations:

- `.github/workflows/sync-repo-metadata.yml:28`

### script-injection (severity: high)

Rule (a) violation: `${{ github.repository }}` (and `${{ secrets.GITHUB_TOKEN }}`) are interpolated directly inside a `run:` shell command that constructs a git remote URL. The `github.repository` value flows through YAML template substitution before the shell sees it, allowing a repository name with shell metacharacters to inject commands.

Offending line: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`

Fix: pass `github.repository` via an `env:` variable (e.g., `REPO: ${{ github.repository }}`) and reference it as `"$REPO"` in the shell script.

Locations:

- `.github/workflows/mcp-security-index.yml:72`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all findings across 7 workflow files:

1. unpinned-uses: Pinned all mutable action references (@v*, @master) to full 40-char SHA digests with tag comments in cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, and sync-rule-count.yml.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write).

4. script-injection (sync-repo-metadata.yml line 28): Moved `${{ github.repository }}` into env var REPO, referenced as `"$REPO"` in shell.

5. script-injection (mcp-security-index.yml line 72): Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env vars GITHUB_TOKEN and REPO, referenced as `${GITHUB_TOKEN}` and `${REPO}` in shell.


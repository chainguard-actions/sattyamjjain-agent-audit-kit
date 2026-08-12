<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.72

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.72** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use `uses:` references pinned to mutable version tags or branch names instead of immutable 40-character SHA digests, making them vulnerable to supply-chain attacks if the referenced action is compromised or its tag is moved.

Affected references include:
- cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9
- docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4
- link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2
- mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0
- release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, pypa/gh-action-pypi-publish@v1.14.2, docker/setup-buildx-action@v4, docker/login-action@v4, aquasecurity/trivy-action@master, docker/build-push-action@v7, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3
- sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/link-check.yml:31`
- `.github/workflows/mcp-security-index.yml:24`
- `.github/workflows/release.yml:56`
- `.github/workflows/sync-rule-count.yml:30`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and no job-level `permissions:` key on any of its jobs. Without explicit permissions, the workflow runs with GitHub's default token permissions, which may be broader than necessary (e.g., write access to contents). All jobs in the file should declare minimal explicit permissions.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`, `id-token: write`) scoped to what the workflow actually needs.

Locations:

- `.github/workflows/scorecard.yml:7`

### script-injection (severity: high)

Two workflow `run:` blocks directly interpolate `${{ ... }}` expressions into shell commands, violating sub-rule (a). Before the shell executes the command, GitHub Actions performs template substitution, so a specially crafted value could inject arbitrary shell commands.

1. sync-repo-metadata.yml line 31: `gh repo edit "${{ github.repository }}" --description "$desc" || true` — `${{ github.repository }}` is interpolated directly into the shell command. Use the `GITHUB_REPOSITORY` environment variable instead: `gh repo edit "$GITHUB_REPOSITORY" ...`.

2. mcp-security-index.yml line 75: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly into the shell command. Use environment variables (`$GITHUB_TOKEN`, `$GITHUB_REPOSITORY`) instead.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:75`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all mutable tag/branch references to full 40-char SHA digests across 6 workflow files (cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml). All original tags preserved as comments.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml. The job-level already had specific minimal permissions (security-events: write, id-token: write, contents: read).

4. script-injection: (a) sync-repo-metadata.yml: replaced `${{ github.repository }}` in the `gh repo edit` command with the built-in `$GITHUB_REPOSITORY` env var. (b) mcp-security-index.yml: moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into the step's `env:` block and referenced them as `${GITHUB_TOKEN}` and `${GITHUB_REPOSITORY}` in the shell command.


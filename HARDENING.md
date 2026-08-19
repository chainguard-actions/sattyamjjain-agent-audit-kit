<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.84

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.84** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable tags or branch names instead of full 40-character SHA commit hashes, making them vulnerable to supply-chain attacks.

cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9
docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4
link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2
mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0
release.yml: actions/checkout@v7.0.1 (×7 jobs), actions/setup-python@v7.0.0 (×7 jobs), docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3, pypa/gh-action-pypi-publish@v1.14.2
sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/link-check.yml:32`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:52`
- `.github/workflows/sync-rule-count.yml:28`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and none of its jobs define job-level `permissions:` blocks. Without explicit permissions, the workflow inherits the default repository token permissions, which may be broader than necessary (e.g. write access to contents).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (the job-level block already narrows to `security-events: write`, `id-token: write`, `contents: read`, so the top-level `read-all` is unnecessary).

Locations:

- `.github/workflows/scorecard.yml:8`

### script-injection (severity: high)

GitHub Actions expressions are interpolated directly inside `run:` shell command strings, violating sub-rule (a). Before the shell executes the command, GitHub substitutes the expression value into the string without any quoting or escaping, enabling command injection if the value contains shell metacharacters.

(1) sync-repo-metadata.yml — `gh repo edit "${{ github.repository }}" --description "$desc"` in the 'Update GitHub repo description' step. The `github.repository` context value is substituted directly into the shell command.

(2) mcp-security-index.yml — `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` in the 'Publish to gh-pages' step. Both `secrets.GITHUB_TOKEN` and `github.repository` are interpolated directly into the shell command string.

Locations:

- `.github/workflows/sync-repo-metadata.yml:27`
- `.github/workflows/mcp-security-index.yml:80`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all action references across 6 workflow files (cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml) to full 40-character SHA hashes with original tags preserved as comments. Used lookup_action_sha to resolve real SHAs for all 14 distinct actions.

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write) matching what the job-level block already specifies.

4. script-injection: Fixed two instances:
   - sync-repo-metadata.yml: Moved `${{ github.repository }}` into env block as REPOSITORY, referenced as $REPOSITORY in shell.
   - mcp-security-index.yml: Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env block as GITHUB_TOKEN and REPOSITORY, referenced as ${GITHUB_TOKEN} and ${REPOSITORY} in shell.


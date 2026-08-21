<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.86

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.86** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of immutable 40-character SHA commit hashes, making them vulnerable to supply-chain attacks if the referenced tag is moved or the branch is updated.

Affected references:
- cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/cache@v6, actions/github-script@v9
- docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, actions/github-script@v9
- link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2
- mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, actions/github-script@v9
- release.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, pypa/gh-action-pypi-publish@v1.14.2, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3, actions/setup-python@v7.0.0
- sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.0.0

Note: aquasecurity/trivy-action@master is especially dangerous as it pins to a mutable branch.

Locations:

- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/docker-nightly.yml:26`
- `.github/workflows/link-check.yml:30`
- `.github/workflows/mcp-security-index.yml:19`
- `.github/workflows/release.yml:55`
- `.github/workflows/sync-rule-count.yml:26`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` block and its single job (`test`) also has no job-level `permissions:` block. Without explicit permissions, the workflow inherits the default token permissions, which may be overly broad (write access to contents and other scopes depending on repository settings).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all available scopes rather than the minimal set required, violating the principle of least privilege. It should be replaced with specific minimal permissions (e.g., `security-events: write`, `id-token: write`, `contents: read`).

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): sync-repo-metadata.yml directly interpolates `${{ github.repository }}` inside a `run:` shell command. The expression is substituted by the Actions runner before the shell processes it, allowing any special characters in the value to be interpreted by the shell. The offending line is: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. Fix: assign to an env var and reference it as `"$GITHUB_REPOSITORY"` (the pre-set env var) instead.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`

### script-injection (severity: high)

Sub-rule (a): mcp-security-index.yml directly interpolates `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` inside a `run:` shell command. Both expressions are substituted by the Actions runner before the shell processes them. The offending line is: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Fix: use the pre-set environment variables `$GITHUB_TOKEN` and `$GITHUB_REPOSITORY` instead of inline expressions.

Locations:

- `.github/workflows/mcp-security-index.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all 5 findings across 8 workflow files:

1. unpinned-uses: Pinned all action references to full SHA hashes in cve-watcher.yml (actions/checkout, actions/setup-python, actions/cache, actions/github-script), docker-nightly.yml (actions/checkout, docker/setup-buildx-action, docker/login-action, docker/build-push-action, aquasecurity/trivy-action, github/codeql-action/upload-sarif, actions/github-script), link-check.yml (actions/checkout, lycheeverse/lychee-action), mcp-security-index.yml (actions/checkout, actions/setup-python, actions/github-script), release.yml (all 14+ action references across 6 jobs), and sync-rule-count.yml (actions/checkout, actions/setup-python).

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml (job-level already has specific scopes: security-events: write, id-token: write, contents: read).

4. script-injection (sync-repo-metadata.yml line 31): Replaced `${{ github.repository }}` with the pre-set `$GITHUB_REPOSITORY` env var.

5. script-injection (mcp-security-index.yml line 89): Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into the step's env: block as GH_TOKEN and GH_REPOSITORY, referenced as shell variables in the run: script.


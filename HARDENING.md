<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.62

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.62** was hardened automatically. 5 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of pinned 40-character SHA digests, making them vulnerable to supply-chain attacks.

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v6, actions/github-script@v9

docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

release.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:18`
- `.github/workflows/docker-nightly.yml:17`
- `.github/workflows/mcp-security-index.yml:19`
- `.github/workflows/release.yml:42`
- `.github/workflows/sync-rule-count.yml:22`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and its only job (`test`) also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the repository default (typically read/write for all scopes), violating the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all scopes and should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`, `id-token: write`).

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Sub-rule (a): A `${{ github.repository }}` expression is interpolated directly inside a `run:` shell command. Before the shell executes, GitHub Actions substitutes the expression value into the script text, allowing a repository name containing shell metacharacters to alter the command. Offending line: `gh repo edit "${{ github.repository }}" --description "$desc" || true`

Locations:

- `.github/workflows/sync-repo-metadata.yml:22`

### script-injection (severity: high)

Sub-rule (a): Both `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are interpolated directly inside a `run:` shell command. GitHub Actions substitutes these expressions into the script text before the shell sees it. Offending line: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`

Locations:

- `.github/workflows/mcp-security-index.yml:75`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all 5 findings across 7 workflow files:

1. unpinned-uses: Pinned all action references to full 40-char SHAs in cve-watcher.yml (checkout, setup-python, cache, github-script), docker-nightly.yml (checkout, setup-buildx-action, login-action, build-push-action, trivy-action, codeql-action/upload-sarif), mcp-security-index.yml (checkout, setup-python), release.yml (checkout x4, setup-python x2, pypi-publish, setup-buildx-action, login-action, build-push-action x2, trivy-action, attest-build-provenance, gh-action-sigstore-python, upload-artifact, download-artifact, action-gh-release), and sync-rule-count.yml (checkout, setup-python).

2. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions (contents: read, security-events: write, id-token: write).

4. script-injection (sync-repo-metadata.yml line 22): Moved `${{ github.repository }}` into env block as GH_REPOSITORY, referenced as $GH_REPOSITORY in shell.

5. script-injection (mcp-security-index.yml line 75): Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env block as GH_TOKEN and GH_REPOSITORY, referenced as ${GH_TOKEN} and ${GH_REPOSITORY} in shell.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Fixed the 'Extract version from tag' step in the docker job of .github/workflows/release.yml. The `github.ref_name` value is now placed in an env var (`REF_NAME`) and sanitized with `printf '%s' "${REF_NAME#v}" | tr -d '\n\r'` before being written to `$GITHUB_OUTPUT`, preventing potential newline injection attacks.


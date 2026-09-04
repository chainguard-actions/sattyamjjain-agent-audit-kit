<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.94

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.94** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

The 'Publish to gh-pages' step in mcp-security-index.yml directly interpolates `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` inside a `run:` shell command string: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any `${{ ... }}` expression interpolated directly in a run: block is a script-injection risk — the value is substituted by the YAML template engine before the shell ever sees it, bypassing shell quoting. Sub-rule (a) violation.

Locations:

- `.github/workflows/mcp-security-index.yml:121`

### unpinned-uses (severity: high)

Multiple workflow files reference actions by mutable tags or version strings instead of full 40-character commit SHA pins, making them vulnerable to supply-chain attacks. Unpinned references found:

- ci.yml: `actions/setup-python@v7`
- cve-deferral-date.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`
- cve-watcher.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/cache@v6`, `actions/github-script@v9`
- docker-nightly.yml: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`, `actions/github-script@v9`
- link-check.yml: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`, `actions/setup-python@v7`
- mcp-security-index.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `actions/github-script@v9`
- release.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`, `pypa/gh-action-pypi-publish@v1.14.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`
- sync-rule-count.yml: `actions/checkout@v7.0.1`, `actions/setup-python@v7`

Locations:

- `.github/workflows/ci.yml:57`
- `.github/workflows/cve-deferral-date.yml:30`
- `.github/workflows/cve-watcher.yml:21`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/link-check.yml:33`
- `.github/workflows/mcp-security-index.yml:28`
- `.github/workflows/release.yml:62`
- `.github/workflows/sync-rule-count.yml:24`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and neither of its jobs (`test`, `counts`) defines a job-level `permissions:` block. Without explicit permissions, the workflow runs with the default token permissions (which may include write access to contents and other scopes), violating the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level, granting overly broad read access across all scopes. This should be replaced with specific minimal permissions (e.g., `contents: read`, `security-events: write`, `id-token: write`) matching only what each job actually needs.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 4 findings:

1. script-injection (mcp-security-index.yml): Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` from the 'Publish to gh-pages' run: shell string into the step's env: block as GH_TOKEN and GH_REPOSITORY, then referenced them as plain shell variables.

2. unpinned-uses: Pinned all 16 distinct action references across 8 workflow files (ci.yml, cve-deferral-date.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml) to full 40-character commit SHAs using lookup_action_sha.

3. missing-permissions (ci.yml): Added top-level `permissions: contents: read` block.

4. broad-permissions (scorecard.yml): Replaced `permissions: read-all` with specific minimal permissions `contents: read` and `actions: read` at the top level (the job already had specific job-level permissions).


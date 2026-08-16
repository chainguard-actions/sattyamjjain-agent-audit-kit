<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.80

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.80** was hardened automatically. 10 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violation: `${{ github.repository }}` is directly interpolated inside a `run:` shell command. The offending line is: `gh repo edit "${{ github.repository }}" --description "$desc" || true`. Any `${{ ... }}` expression inside a run: block is a script-injection risk because the value is substituted by the YAML template engine before the shell ever sees it.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`

### script-injection (severity: high)

Rule (a) violation: `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` are directly interpolated inside a `run:` shell command. The offending line is: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any `${{ ... }}` expression inside a run: block is a script-injection risk because the value is substituted by the YAML template engine before the shell ever sees it.

Locations:

- `.github/workflows/mcp-security-index.yml:68`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and the single job (`test`) also has no `permissions:` key. Without explicit permissions the workflow inherits the repository default (typically write-all for private repos), granting broader access than necessary.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all scopes rather than the minimal specific scopes needed, violating the principle of least privilege.

Locations:

- `.github/workflows/scorecard.yml:11`

### unpinned-uses (severity: high)

Multiple actions are referenced by mutable tag or branch refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `actions/cache@v6`, `actions/github-script@v9`.

Locations:

- `.github/workflows/cve-watcher.yml:20`

### unpinned-uses (severity: high)

Multiple actions are referenced by mutable tag or branch refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`.

Locations:

- `.github/workflows/docker-nightly.yml:20`

### unpinned-uses (severity: high)

Multiple actions are referenced by mutable tag or branch refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `lycheeverse/lychee-action@v2`.

Locations:

- `.github/workflows/link-check.yml:28`

### unpinned-uses (severity: high)

Multiple actions are referenced by mutable tag or branch refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/mcp-security-index.yml:23`

### unpinned-uses (severity: high)

Multiple actions are referenced by mutable tag or branch refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`, `pypa/gh-action-pypi-publish@v1.14.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.5.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`.

Locations:

- `.github/workflows/release.yml:37`

### unpinned-uses (severity: high)

Multiple actions are referenced by mutable tag or branch refs instead of immutable 40-character SHA digests. Failing references: `actions/checkout@v7.0.1`, `actions/setup-python@v7.0.0`.

Locations:

- `.github/workflows/sync-rule-count.yml:28`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, missing-permissions, broad-permissions, unpinned-uses

**Notes:**

Fixed all 10 findings across 7 workflow files:

1. script-injection (sync-repo-metadata.yml): Moved ${{ github.repository }} into env block as REPO, referenced as $REPO in shell.

2. script-injection (mcp-security-index.yml): Moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} into env block as GH_TOKEN and REPO, referenced as ${GH_TOKEN} and ${REPO} in shell.

3. missing-permissions (ci.yml): Added top-level `permissions: contents: read`.

4. broad-permissions (scorecard.yml): Replaced `permissions: read-all` with `contents: read` and `actions: read`.

5. unpinned-uses (cve-watcher.yml): Pinned checkout@3d3c42e5, setup-python@5fda3b95, cache@55cc8345, github-script@3a2844b7.

6. unpinned-uses (docker-nightly.yml): Pinned checkout@3d3c42e5, setup-buildx-action@bb05f3f5, login-action@dbcb8138, build-push-action@53b7df96, trivy-action@d2a0b607, upload-sarif@ff2f1c62.

7. unpinned-uses (link-check.yml): Pinned checkout@3d3c42e5, lychee-action@e7477775.

8. unpinned-uses (mcp-security-index.yml): Pinned checkout@3d3c42e5, setup-python@5fda3b95.

9. unpinned-uses (release.yml): Pinned all 12 unpinned actions across 6 jobs including checkout, setup-python, pypi-publish, docker actions, trivy, attest-build-provenance, sigstore-python, upload-artifact, download-artifact, action-gh-release.

10. unpinned-uses (sync-rule-count.yml): Pinned checkout@3d3c42e5, setup-python@5fda3b95.


<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit--/v0.3.46

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **sattyamjjain--agent-audit-kit--/v0.3.46** was hardened automatically. 4 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use action references pinned to mutable version tags (e.g. @v7.0.0, @v4, @master) instead of immutable 40-character commit SHAs. This exposes the workflow to supply-chain attacks if the tag is moved. Affected references include: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, pypa/gh-action-pypi-publish@v1.14.0, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

Locations:

- `.github/workflows/cve-watcher.yml:18`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:47`
- `.github/workflows/sync-rule-count.yml:26`

### missing-permissions (severity: medium)

The workflow file ci.yml has no top-level 'permissions:' key and the single job 'test' also has no job-level 'permissions:' key. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow file scorecard.yml sets top-level 'permissions: read-all', which grants overly broad read access to all scopes. It should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

Rule (a): GitHub Actions expressions are interpolated directly inside run: shell command strings. In sync-repo-metadata.yml, '${{ github.repository }}' is embedded directly in a shell command: `gh repo edit "${{ github.repository }}" --description "$desc"`. In mcp-security-index.yml, '${{ secrets.GITHUB_TOKEN }}' and '${{ github.repository }}' are embedded directly in a shell command: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. Any ${{ ... }} expression inside a run: block is substituted by the YAML template engine before the shell sees it, bypassing shell quoting and enabling injection.

Locations:

- `.github/workflows/sync-repo-metadata.yml:27`
- `.github/workflows/mcp-security-index.yml:72`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four finding types across multiple workflow files:

1. unpinned-uses: Pinned all mutable action references to full 40-char commit SHAs in cve-watcher.yml (checkout@9c091bb, setup-python@ece7cb0, cache@caa2961, github-script@3a2844b), docker-nightly.yml (checkout@9c091bb, setup-buildx-action@bb05f3f, login-action@af1e73f, build-push-action@53b7df9, trivy-action@c07df6f, codeql-action/upload-sarif@54f647b), mcp-security-index.yml (checkout@9c091bb, setup-python@ece7cb0), release.yml (checkout@9c091bb x4, setup-python@ece7cb0 x2, pypi-publish@cef2210, setup-buildx-action@bb05f3f, login-action@af1e73f, build-push-action@53b7df9 x2, trivy-action@c07df6f, attest-build-provenance@0f67c3f, sigstore-python@5b79a39, upload-artifact@043fb46, download-artifact@3e5f45b, action-gh-release@718ea10), and sync-rule-count.yml (checkout@9c091bb, setup-python@ece7cb0).

2. missing-permissions: Added 'permissions: contents: read' top-level block to ci.yml.

3. broad-permissions: Replaced 'permissions: read-all' with 'permissions: contents: read' in scorecard.yml (job-level permissions already had specific minimal scopes).

4. script-injection: In sync-repo-metadata.yml, moved ${{ github.repository }} to env block as GH_REPOSITORY and replaced inline expression with $GH_REPOSITORY. In mcp-security-index.yml, moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} to env block as GH_TOKEN and GH_REPOSITORY and replaced inline expressions with ${GH_TOKEN} and ${GH_REPOSITORY}.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Fixed the github-env-injection finding in hardened/action/.github/workflows/release.yml at line 107. The 'Extract version from tag' step now sanitizes GITHUB_REF_NAME before writing to $GITHUB_OUTPUT. Changed from a single-line `echo "version=${GITHUB_REF_NAME#v}" >> "$GITHUB_OUTPUT"` to a multi-line run block that first strips newlines via `safe=$(printf '%s' "${GITHUB_REF_NAME#v}" | tr -d '\n\r')` and then writes the sanitized value: `echo "version=$safe" >> "$GITHUB_OUTPUT"`.


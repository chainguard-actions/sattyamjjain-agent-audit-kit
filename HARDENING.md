<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.64

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.64** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files use `uses:` references pinned to mutable version tags or branch names instead of immutable 40-character commit SHAs, making them vulnerable to supply-chain attacks. Failing references include: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v6, actions/github-script@v9, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4, pypa/gh-action-pypi-publish@v1.14.0, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3.

Locations:

- `.github/workflows/cve-watcher.yml:19`
- `.github/workflows/cve-watcher.yml:23`
- `.github/workflows/cve-watcher.yml:28`
- `.github/workflows/cve-watcher.yml:47`
- `.github/workflows/docker-nightly.yml:18`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/docker-nightly.yml:27`
- `.github/workflows/docker-nightly.yml:37`
- `.github/workflows/docker-nightly.yml:57`
- `.github/workflows/docker-nightly.yml:66`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/mcp-security-index.yml:27`
- `.github/workflows/release.yml:43`
- `.github/workflows/release.yml:47`
- `.github/workflows/release.yml:57`
- `.github/workflows/release.yml:67`
- `.github/workflows/release.yml:72`
- `.github/workflows/release.yml:77`
- `.github/workflows/release.yml:88`
- `.github/workflows/release.yml:93`
- `.github/workflows/release.yml:100`
- `.github/workflows/release.yml:115`
- `.github/workflows/release.yml:130`
- `.github/workflows/release.yml:135`
- `.github/workflows/release.yml:148`
- `.github/workflows/release.yml:163`
- `.github/workflows/release.yml:178`
- `.github/workflows/release.yml:183`
- `.github/workflows/release.yml:188`
- `.github/workflows/release.yml:202`
- `.github/workflows/sync-rule-count.yml:24`
- `.github/workflows/sync-rule-count.yml:29`

### missing-permissions (severity: medium)

The CI workflow file has no top-level `permissions:` key and the single job `test` also has no `permissions:` key. Without explicit permissions, the workflow inherits the default repository permissions (which may include write access to contents and other scopes), violating the principle of least privilege.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The Scorecard workflow sets `permissions: read-all` at the top level. This grants read access to all available scopes and should be replaced with specific minimal permissions. The job-level permissions are correctly scoped, but the top-level `read-all` still represents an overly broad grant.

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 3 findings across 6 workflow files:

1. **unpinned-uses** (32 locations): Pinned all mutable tag/branch references to full 40-char commit SHAs with original tag in comment:
   - actions/checkout@v7.0.0 → @9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0
   - actions/setup-python@v6.3.0 → @ece7cb06caefa5fff74198d8649806c4678c61a1
   - actions/cache@v6 → @55cc8345863c7cc4c66a329aec7e433d2d1c52a9
   - actions/github-script@v9 → @3a2844b7e9c422d3c10d287c895573f7108da1b3
   - docker/setup-buildx-action@v4 → @bb05f3f5519dd87d3ba754cc423b652a5edd6d2c
   - docker/login-action@v4 → @dbcb813823bdd20940b903addbd779551569679f
   - docker/build-push-action@v7 → @53b7df96c91f9c12dcc8a07bcb9ccacbed38856a
   - aquasecurity/trivy-action@master → @c07df6fec6fa692e6fd1200d50aaa1fdd66f03c8
   - github/codeql-action/upload-sarif@v4 → @f205ea1c3313d32999d8d6a48b4f6530d4437b38
   - pypa/gh-action-pypi-publish@v1.14.0 → @cef221092ed1bacb1cc03d23a2d87d1d172e277b
   - actions/attest-build-provenance@v4 → @0f67c3f4856b2e3261c31976d6725780e5e4c373
   - sigstore/gh-action-sigstore-python@v3.4.0 → @5b79a39c381910c090341a2c9b0bf022c8b387e1
   - actions/upload-artifact@v7 → @043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
   - actions/download-artifact@v8 → @3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c
   - softprops/action-gh-release@v3 → @3d0d9888cb7fd7b750713d6e236d1fcb99157228

2. **missing-permissions**: Added `permissions: contents: read` top-level block to ci.yml.

3. **broad-permissions**: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml; job-level permissions already correctly specify minimal scopes.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Fixed two script-injection findings:
1. `.github/workflows/mcp-security-index.yml` (Publish to gh-pages step): Moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into the step's `env:` block as `GH_TOKEN` and `GH_REPOSITORY`. The `run:` script now uses `${GH_TOKEN}` and `${GH_REPOSITORY}` as plain shell variables.
2. `.github/workflows/sync-repo-metadata.yml` (Update GitHub repo description step): Moved `${{ github.repository }}` into the step's `env:` block as `GH_REPOSITORY`. The `run:` script now uses `"$GH_REPOSITORY"` as a plain, double-quoted shell variable.


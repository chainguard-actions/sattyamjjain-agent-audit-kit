<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.58

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.58** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable version tags or branch names instead of full 40-character commit SHAs, making them vulnerable to supply-chain attacks.

cve-watcher.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0, actions/cache@v5, actions/github-script@v9

docker-nightly.yml: actions/checkout@v7.0.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master, github/codeql-action/upload-sarif@v4

mcp-security-index.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

release.yml: actions/checkout@v7.0.0 (×3), actions/setup-python@v6.3.0 (×2), pypa/gh-action-pypi-publish@v1.14.0, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (×2), aquasecurity/trivy-action@master, actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.4.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3

sync-rule-count.yml: actions/checkout@v7.0.0, actions/setup-python@v6.3.0

Locations:

- `.github/workflows/cve-watcher.yml:21`
- `.github/workflows/cve-watcher.yml:24`
- `.github/workflows/cve-watcher.yml:28`
- `.github/workflows/cve-watcher.yml:34`
- `.github/workflows/docker-nightly.yml:17`
- `.github/workflows/docker-nightly.yml:20`
- `.github/workflows/docker-nightly.yml:23`
- `.github/workflows/docker-nightly.yml:33`
- `.github/workflows/docker-nightly.yml:57`
- `.github/workflows/docker-nightly.yml:62`
- `.github/workflows/mcp-security-index.yml:24`
- `.github/workflows/mcp-security-index.yml:30`
- `.github/workflows/release.yml:44`
- `.github/workflows/release.yml:48`
- `.github/workflows/release.yml:62`
- `.github/workflows/release.yml:73`
- `.github/workflows/release.yml:77`
- `.github/workflows/release.yml:81`
- `.github/workflows/release.yml:90`
- `.github/workflows/release.yml:97`
- `.github/workflows/release.yml:107`
- `.github/workflows/release.yml:117`
- `.github/workflows/release.yml:131`
- `.github/workflows/release.yml:135`
- `.github/workflows/release.yml:148`
- `.github/workflows/release.yml:157`
- `.github/workflows/release.yml:163`
- `.github/workflows/release.yml:170`
- `.github/workflows/release.yml:185`
- `.github/workflows/sync-rule-count.yml:27`
- `.github/workflows/sync-rule-count.yml:33`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and its only job (`test`) also has no job-level `permissions:` key. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents by default on many repositories).

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is overly broad. It should be replaced with specific minimal permissions (e.g., `security-events: write`, `contents: read`, `id-token: write`).

Locations:

- `.github/workflows/scorecard.yml:11`

### script-injection (severity: high)

Two workflow run: blocks directly interpolate ${{ ... }} expressions into shell command strings (sub-rule a), allowing template substitution to inject arbitrary shell metacharacters before the shell parses the command.

(1) .github/workflows/sync-repo-metadata.yml: `gh repo edit "${{ github.repository }}" --description "$desc"` — the `github.repository` context value is interpolated directly into the shell command string.

(2) .github/workflows/mcp-security-index.yml: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"` — both `secrets.GITHUB_TOKEN` and `github.repository` are interpolated directly into the shell command string.

Fix: move the values into `env:` variables and reference them as `$VAR` in the shell script.

Locations:

- `.github/workflows/sync-repo-metadata.yml:31`
- `.github/workflows/mcp-security-index.yml:86`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. **unpinned-uses**: Pinned all mutable action references to full 40-char SHAs across 5 workflow files:
   - actions/checkout@v7.0.0 → @9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0
   - actions/setup-python@v6.3.0 → @ece7cb06caefa5fff74198d8649806c4678c61a1
   - actions/cache@v5 → @caa296126883cff596d87d8935842f9db880ef25
   - actions/github-script@v9 → @3a2844b7e9c422d3c10d287c895573f7108da1b3
   - docker/setup-buildx-action@v4 → @bb05f3f5519dd87d3ba754cc423b652a5edd6d2c
   - docker/login-action@v4 → @06fb636fac595d6fb4b28a5dfcb21a6f5091859c
   - docker/build-push-action@v7 → @53b7df96c91f9c12dcc8a07bcb9ccacbed38856a
   - aquasecurity/trivy-action@master → @c07df6fec6fa692e6fd1200d50aaa1fdd66f03c8
   - github/codeql-action/upload-sarif@v4 → @e4fba868fa4b1b91e1fdab776edc8cfbe6e9fb81
   - pypa/gh-action-pypi-publish@v1.14.0 → @cef221092ed1bacb1cc03d23a2d87d1d172e277b
   - actions/attest-build-provenance@v4 → @0f67c3f4856b2e3261c31976d6725780e5e4c373
   - sigstore/gh-action-sigstore-python@v3.4.0 → @5b79a39c381910c090341a2c9b0bf022c8b387e1
   - actions/upload-artifact@v7 → @043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
   - actions/download-artifact@v8 → @3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c
   - softprops/action-gh-release@v3 → @3d0d9888cb7fd7b750713d6e236d1fcb99157228

2. **missing-permissions**: Added `permissions: contents: read` to ci.yml.

3. **broad-permissions**: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: `contents: read`, `security-events: write`, `id-token: write`.

4. **script-injection**: Fixed two instances:
   - sync-repo-metadata.yml: moved `${{ github.repository }}` into env var `REPOSITORY`
   - mcp-security-index.yml: moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` into env vars `GITHUB_TOKEN` and `REPOSITORY`


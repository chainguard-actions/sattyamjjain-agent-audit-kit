<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.25

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.25** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): GitHub Actions expressions are interpolated directly inside `run:` shell command strings. In mcp-security-index.yml, the 'Publish to gh-pages' step embeds `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` directly in a shell command: `git remote add origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git"`. In sync-repo-metadata.yml, the 'Update GitHub repo description' step embeds `${{ github.repository }}` directly in a shell command: `gh repo edit "${{ github.repository }}" --description "$desc"`. Any `${{ ... }}` expression inside a `run:` block is a script-injection risk because YAML template substitution occurs before the shell ever sees the string.

Locations:

- `.github/workflows/mcp-security-index.yml:72`
- `.github/workflows/sync-repo-metadata.yml:24`

### unpinned-uses (severity: high)

Multiple workflow files reference actions by mutable tag or version strings instead of full 40-character commit SHAs. Unpinned references are vulnerable to supply-chain attacks if the upstream tag is moved or the repository is compromised.

cve-watcher.yml: `actions/checkout@v6.0.2`, `actions/setup-python@v6.2.0`, `actions/cache@v5`, `actions/github-script@v9`

docker-nightly.yml: `actions/checkout@v6.0.2`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `github/codeql-action/upload-sarif@v4`

mcp-security-index.yml: `actions/checkout@v6.0.2`, `actions/setup-python@v6.2.0`

release.yml: `actions/checkout@v6.0.2`, `actions/setup-python@v6.2.0`, `pypa/gh-action-pypi-publish@v1.14.0`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`, `docker/build-push-action@v7`, `aquasecurity/trivy-action@master`, `actions/attest-build-provenance@v4`, `sigstore/gh-action-sigstore-python@v3.3.0`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`, `softprops/action-gh-release@v3`

sync-rule-count.yml: `actions/checkout@v6.0.2`, `actions/setup-python@v6.2.0`

Locations:

- `.github/workflows/cve-watcher.yml:20`
- `.github/workflows/docker-nightly.yml:19`
- `.github/workflows/mcp-security-index.yml:22`
- `.github/workflows/release.yml:46`
- `.github/workflows/sync-rule-count.yml:36`

### missing-permissions (severity: medium)

The workflow file ci.yml has no top-level `permissions:` key and no job-level `permissions:` key on any of its jobs. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad (write access to contents, packages, etc.). A minimal permissions block should be added.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

The workflow file scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and is considered overly broad. It should be replaced with a specific minimal set of permissions required by the workflow (e.g., `security-events: write`, `contents: read`).

Locations:

- `.github/workflows/scorecard.yml:9`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, unpinned-uses, missing-permissions, broad-permissions

**Notes:**

Fixed all 4 findings:

1. script-injection: In mcp-security-index.yml, moved ${{ secrets.GITHUB_TOKEN }} and ${{ github.repository }} from the 'Publish to gh-pages' run: shell string into an env: block (as GH_TOKEN and GH_REPOSITORY), then referenced them as plain shell variables. In sync-repo-metadata.yml, moved ${{ github.repository }} from the 'Update GitHub repo description' run: shell string into the existing env: block (as GH_REPOSITORY).

2. unpinned-uses: Pinned all unpinned action references to full 40-char commit SHAs:
- actions/checkout@v6.0.2 → @de0fac2e4500dabe0009e67214ff5f5447ce83dd
- actions/setup-python@v6.2.0 → @a309ff8b426b58ec0e2a45f0f869d46889d02405
- actions/cache@v5 → @caa296126883cff596d87d8935842f9db880ef25
- actions/github-script@v9 → @3a2844b7e9c422d3c10d287c895573f7108da1b3
- docker/setup-buildx-action@v4 → @bb05f3f5519dd87d3ba754cc423b652a5edd6d2c
- docker/login-action@v4 → @af1e73f918a031802d376d3c8bbc3fe56130a9b0
- docker/build-push-action@v7 → @53b7df96c91f9c12dcc8a07bcb9ccacbed38856a
- aquasecurity/trivy-action@master → @c07df6fec6fa692e6fd1200d50aaa1fdd66f03c8
- github/codeql-action/upload-sarif@v4 → @7188fc363630916deb702c7fdcf4e481b751f97a
- pypa/gh-action-pypi-publish@v1.14.0 → @cef221092ed1bacb1cc03d23a2d87d1d172e277b
- actions/attest-build-provenance@v4 → @0f67c3f4856b2e3261c31976d6725780e5e4c373
- sigstore/gh-action-sigstore-python@v3.3.0 → @04cffa1d795717b140764e8b640de88853c92acc
- actions/upload-artifact@v7 → @043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
- actions/download-artifact@v8 → @3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c
- softprops/action-gh-release@v3 → @3d0d9888cb7fd7b750713d6e236d1fcb99157228

3. missing-permissions: Added `permissions: contents: read` top-level block to ci.yml.

4. broad-permissions: Replaced `permissions: read-all` in scorecard.yml with specific minimal permissions: contents: read, security-events: write, id-token: write.


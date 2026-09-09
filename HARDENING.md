<!-- markdownlint-disable -->

# Hardening Report: sattyamjjain--agent-audit-kit/v0.3.92

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **sattyamjjain--agent-audit-kit/v0.3.92** was hardened automatically. 4 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple workflow files reference GitHub Actions using mutable tags or branch names instead of full 40-character commit SHAs. This allows supply-chain attacks if the referenced action is compromised or the tag is moved. Affected references include: ci.yml: actions/setup-python@v7; cve-watcher.yml: actions/checkout@v7.0.1, actions/setup-python@v7, actions/cache@v6, actions/github-script@v9; docker-nightly.yml: actions/checkout@v7.0.1, docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7, aquasecurity/trivy-action@master (branch ref), github/codeql-action/upload-sarif@v4, actions/github-script@v9; link-check.yml: actions/checkout@v7.0.1, lycheeverse/lychee-action@v2, actions/setup-python@v7; mcp-security-index.yml: actions/checkout@v7.0.1, actions/setup-python@v7, actions/github-script@v9; release.yml: actions/checkout@v7.0.1 (multiple jobs), actions/setup-python@v7 (multiple jobs), docker/setup-buildx-action@v4, docker/login-action@v4, docker/build-push-action@v7 (multiple), aquasecurity/trivy-action@master (branch ref), actions/attest-build-provenance@v4, sigstore/gh-action-sigstore-python@v3.5.0, actions/upload-artifact@v7, actions/download-artifact@v8, softprops/action-gh-release@v3; sync-rule-count.yml: actions/checkout@v7.0.1, actions/setup-python@v7.

Locations:

- `.github/workflows/ci.yml:57`
- `.github/workflows/cve-watcher.yml:22`
- `.github/workflows/cve-watcher.yml:26`
- `.github/workflows/cve-watcher.yml:29`
- `.github/workflows/cve-watcher.yml:57`
- `.github/workflows/docker-nightly.yml:22`
- `.github/workflows/docker-nightly.yml:25`
- `.github/workflows/docker-nightly.yml:28`
- `.github/workflows/docker-nightly.yml:36`
- `.github/workflows/docker-nightly.yml:53`
- `.github/workflows/docker-nightly.yml:60`
- `.github/workflows/docker-nightly.yml:73`
- `.github/workflows/link-check.yml:37`
- `.github/workflows/link-check.yml:39`
- `.github/workflows/link-check.yml:72`
- `.github/workflows/link-check.yml:73`
- `.github/workflows/mcp-security-index.yml:27`
- `.github/workflows/mcp-security-index.yml:30`
- `.github/workflows/mcp-security-index.yml:108`
- `.github/workflows/release.yml:56`
- `.github/workflows/release.yml:60`
- `.github/workflows/release.yml:130`
- `.github/workflows/release.yml:133`
- `.github/workflows/release.yml:163`
- `.github/workflows/release.yml:166`
- `.github/workflows/release.yml:186`
- `.github/workflows/release.yml:189`
- `.github/workflows/release.yml:210`
- `.github/workflows/release.yml:213`
- `.github/workflows/release.yml:218`
- `.github/workflows/release.yml:228`
- `.github/workflows/release.yml:231`
- `.github/workflows/release.yml:234`
- `.github/workflows/release.yml:241`
- `.github/workflows/release.yml:248`
- `.github/workflows/release.yml:261`
- `.github/workflows/release.yml:270`
- `.github/workflows/release.yml:276`
- `.github/workflows/release.yml:290`
- `.github/workflows/release.yml:338`
- `.github/workflows/sync-rule-count.yml:22`
- `.github/workflows/sync-rule-count.yml:27`

### missing-permissions (severity: medium)

ci.yml has no top-level `permissions:` key and neither of its two jobs (`test` and `counts`) defines a job-level `permissions:` block. This means the workflow runs with GitHub's default permissions (contents: write for most events), granting broader access than necessary.

Locations:

- `.github/workflows/ci.yml:1`

### broad-permissions (severity: medium)

scorecard.yml sets `permissions: read-all` at the top level. This grants read access to all repository scopes and should be replaced with specific minimal permissions.

Locations:

- `.github/workflows/scorecard.yml:9`

### script-injection (severity: high)

mcp-security-index.yml interpolates `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` directly inside a `run:` shell command string (the `git remote add origin` line in the 'Publish to gh-pages' step). Per rule (a), ANY `${{ ... }}` expression directly in a `run:` block is a script-injection risk — the YAML template substitution occurs before the shell ever sees the string, so shell metacharacters in the substituted value are parsed by the shell. The `github.repository` value in particular could contain characters that alter the shell command if the repository name is attacker-influenced.

Locations:

- `.github/workflows/mcp-security-index.yml:98`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions, broad-permissions, script-injection

**Notes:**

Fixed all four findings:

1. unpinned-uses: Pinned all unpinned action references across 7 workflow files (ci.yml, cve-watcher.yml, docker-nightly.yml, link-check.yml, mcp-security-index.yml, release.yml, sync-rule-count.yml) to full 40-char commit SHAs. Actions pinned: actions/checkout@v7.0.1→3d3c42e5, actions/setup-python@v7→5fda3b95, actions/cache@v6→55cc8345, actions/github-script@v9→3a2844b7, docker/setup-buildx-action@v4→37fe6310, docker/login-action@v4→dbcb8138, docker/build-push-action@v7→53b7df96, aquasecurity/trivy-action@master→d2a0b607, github/codeql-action/upload-sarif@v4→cdf488f5, lycheeverse/lychee-action@v2→e7477775, actions/attest-build-provenance@v4→4d101475, sigstore/gh-action-sigstore-python@v3.5.0→790bc6be, actions/upload-artifact@v7→043fb46d, actions/download-artifact@v8→3e5f45b2, softprops/action-gh-release@v3→efb35369.

2. missing-permissions: Added top-level `permissions: contents: read` to ci.yml.

3. broad-permissions: Replaced `permissions: read-all` with `permissions: contents: read` in scorecard.yml (job-level permissions already specify the minimal required scopes).

4. script-injection: In mcp-security-index.yml, moved `${{ secrets.GITHUB_TOKEN }}` and `${{ github.repository }}` from the `git remote add origin` run command into an `env:` block as GH_TOKEN and GH_REPOSITORY, then referenced them as shell variables `${GH_TOKEN}` and `${GH_REPOSITORY}`.

### Iteration 2

**Fixes applied:** unpinned-uses

**Notes:**

Pinned `pypa/gh-action-pypi-publish@v1.14.2` to its full commit SHA `dc37677b2e1c63e2034f94d8a5b11f265b73ba33` in `.github/workflows/release.yml` line 208. The tag is preserved as a comment for readability: `pypa/gh-action-pypi-publish@dc37677b2e1c63e2034f94d8a5b11f265b73ba33 # v1.14.2`.


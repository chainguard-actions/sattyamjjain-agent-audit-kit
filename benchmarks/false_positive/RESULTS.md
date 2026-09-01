# Benign-slice HIGH/CRITICAL false-positive rate — AgentAuditKit

> Generated from `benchmarks/false_positive/run.py` over a benign slice derived
> by `corpus.py`. Run date **2026-08-24**. Offline, deterministic, no LLM.
> Reproduce: `make fp` (or `python benchmarks/false_positive/run.py`).
> The slice itself is committed as [`benign-slice.json`](benign-slice.json), so
> which servers were measured is checkable without running anything.

## Headline

On a **536-config benign slice** of public MCP servers, AgentAuditKit produces
**4 HIGH/CRITICAL findings** (0.8% of the slice). Hand-adjudicated: **2 false
positives, 1 true positive, 1 ambiguous**.

**Benign-slice HIGH/CRITICAL false-positive rate = 2 / 4 = 50.0%** (Wilson 95%
CI **[15.0%, 85.0%]**).

The untuned measurement was **4 / 6 = 66.7%**, published first in its own commit
and kept in [`triage.md`](triage.md) and the history table below. Both remaining
false positives are attributable to the corpus rather than the scanner, and the
section on root causes says which is which.

That is a large regression against the 0.0% published on 2026-07-22, and the
reason is worth stating first: **the 0.0% was never re-measured after the corpus
grew.** The manifest went from 1,374 to 1,641 registry servers and the benign
slice from 368 to 536, and nothing re-ran the benchmark. The published number
described a slice that no longer existed. There is now a drift guard
(`make fp-check`) so that cannot recur silently.

The untuned number was measured, adjudicated, and committed **before** any rule
was changed, so the record shows what the scanner actually did rather than only
what it did after being adjusted. This file reports the post-fix state; the
commit immediately preceding it reports the pre-fix state.

### How to read the badge

The README badge reads `benign-slice 536 configs · HIGH/CRIT FP 2/4`. The two
numbers answer different questions and both are needed:

- **536** is how many benign configs were scanned. This is the sample size of
  the *measurement*.
- **2/4** is how many of the HIGH/CRITICAL findings raised on those 536 configs
  were wrong. The denominator is small because the scanner is quiet on benign
  input — 4 high-severity findings across 536 configs — not because little was
  tested.

That small denominator is also why the ratio moves oddly: the fix removed 2
findings from the numerator *and* the denominator, so the rate fell 66.7% → 50.0%
while the number of wrong findings halved, 4 → 2. The absolute count is the more
informative figure at this scale, which is why the badge carries both.

The previous badge read `0/1 (n=1)`, which reads as "one thing was tested." It
was not: 368 configs were tested and exactly one high-severity finding came out
of them. The badge is now explicit about both figures because that phrasing
misled every reader who did not open this file, which is the point of a badge.

## Method

### Reuse, not reimplementation

The benchmark runs the shipped engine; it contains no scanner or scorer of its
own. It reuses:

- `agent_audit_kit.engine.run_scan` — the scan entrypoint the `scan` CLI drives.
- `agent_audit_kit.rules.builtin.RULES` — rule titles, severities, families.
- the committed corpus manifest
  `research/state-of-mcp-2026/corpus/registry-manifest.json` (1,641 servers,
  fetched 2026-07-26 from `https://registry.modelcontextprotocol.io/v0/servers`).

### Pre-registered benign predicate

A server is in the benign slice iff ALL hold (pre-registered in `corpus.py`, where
the `PREDICATE` string has been byte-identical since its first commit
[`412575c`](https://github.com/sattyamjjain/agent-audit-kit/commit/412575c) / #476 —
so "pre-registered" is a checkable claim about git history, not an assurance):

1. It is an **official MCP Registry** latest-version server.
2. Its registry status is **active**.
3. It **declares an auth mode** — `static-credential`, `header-nonsecret`, or
   `local-stdio` (i.e. not `none`/`unknown`).
4. It is **not in any CVE/advisory feed AAK ships** (`data/vuln_db.json` package
   names + the CVE version-pin package names).

"Benign" is a property of the server's own published metadata. It is **not**
defined as "AAK found nothing" — that would make the measurement circular.

**Resulting n = 536**: 1,641 upstream servers → 603 active with a declared auth
mode → 67 excluded for appearing in a shipped CVE feed → **536**. By auth mode:
400 static-credential, 135 local-stdio, 1 header-nonsecret. By transport: 399
streamable-http, 133 stdio, 4 sse.

The predicate is unchanged from 2026-07-20. It was **not** adjusted in this run —
loosening a pre-registered predicate after seeing the result is the failure mode
the pre-registration exists to prevent.

**Stars substitution (honesty).** The commonly-suggested "repo ≥ N stars"
conjunct is *not* used: neither the MCP Registry API nor the cached raw data
exposes GitHub stars or a repository URL, and fetching stars for hundreds of
repos would require a networked GitHub-API pass — this benchmark is offline by
construction. Predicate (1)+(2) is the offline curation proxy that stands in for
the stars signal.

### Provenance

[`benign-slice.json`](benign-slice.json) carries every server in the slice with
its registry provenance: `name`, `version`, `source_url` (the endpoint the server
publishes), `registry_status`, `published_at`, `auth_mode`, `transport`, and the
`fetched_at` date of the snapshot. Corpus-level provenance — the upstream API URL
and fetch date — is carried at the top of the file. `make fp-check` fails if it
drifts from a fresh derivation.

## Findings profile (n = 536)

1,158 findings total (2.16 per config), almost all low-severity / advisory:

| Severity | Findings |
|----------|---------:|
| critical | 4 |
| high | 0 |
| medium | 665 |
| low | 489 |

### Noisiest rules overall (all severities)

| Rule | Severity | Findings | Note |
|------|:--------:|---------:|------|
| `AAK-MCP-ATTEST-001` | MEDIUM | 536 | Advisory-posture rule — fires on every config (no attestation); excluded from the report headline as advisory. |
| `AAK-OAUTH-008` | LOW | 366 | Expected on static-credential servers (no RFC 9728 discovery). |
| `AAK-MCP-005` | MEDIUM | 123 | `npx`/`uvx` fetch-and-execute — a real supply-chain pattern, MEDIUM. |
| `AAK-MCP-007` | LOW | 123 | Advisory-posture. |
| `AAK-MCP-001` | **CRITICAL** | 4 | The only HIGH/CRITICAL rule that fired — adjudicated below. |

The MEDIUM count is inflated by one advisory rule (`AAK-MCP-ATTEST-001`) that
fires on 100% of configs by design; it is not an exploitable misconfiguration.
Only `AAK-MCP-001` produced HIGH/CRITICAL findings, so it is the whole of the FP
surface here — as it was in both previous runs.

## Adjudication (single rater, 2026-08-24)

Full table in [`triage.md`](triage.md). Summary:

| # | Rule | Config | Verdict | Reason |
|--:|------|--------|:------:|--------|
| 1 | `AAK-MCP-001` | `ai.spala/public-mcp` | TP | Only header is `Accept`; genuinely no auth (server named `public-mcp`). |
| 2 | `AAK-MCP-001` | `co.curie/commerce` | **FP** | Server declares `Authorization` (`isSecret`) on remote 1; only remote 0 was converted. |
| 3 | `AAK-MCP-001` | `co.huggingface/hf-mcp-server` | **FP** | Same: `Authorization` on remote 1; remote 0 is the `?login` OAuth entry point. |
| 4 | `AAK-MCP-001` | `app.thoughtspot/mcp-server` | ambiguous | Snapshot says `static-credential` at v1.0.1; the live registry has moved to v0.5.0, so the July record cannot be re-verified. |

Cleared by the fix in this run, and recorded in [`triage.md`](triage.md):
`ai.velarion/company-intelligence` (`X-Velarion-Agent-Token`) and
`br.com.signdocs/mcp-server` (`X-SignDocs-Client-Id` + `-Client-Secret`).

Findings 4 and 5 were verified against the **live** MCP Registry at the same
version as the snapshot, so the auth they declare is a fact and not an inference.

### Two root causes, and only one of them is the scanner

**A. Scanner gap — FIXED in this run.** [#475](https://github.com/sattyamjjain/agent-audit-kit/issues/475)
extended `AAK-MCP-001` from `Authorization`/`Bearer` to the `X-*-Key` /
`*-API-Key` family. Real vendors also authenticate with `-Token`, `-Secret`, and
client-credential *pairs*. The 2026-07 fix generalised one suffix and stopped —
which is why the same class of false positive came back the moment the slice
grew. The family now covers `-key`/`-token`/`-secret`. Measured across the whole
1,641-config corpus the change silences **exactly the 2 offending configs and
nothing else** (1,046 → 1,044 firing, 0 newly firing), so it did not buy a lower
false-positive rate with false negatives. A bare `client_id` and
`X-CSRF-Token`/`X-XSRF-Token` are deliberately still *not* treated as auth.

**B. Benchmark gap — fixed forward, not retroactively (the 2 remaining FPs).**
`fetch_registry._to_config()` builds the scannable config from `remotes[0]` only.
A server that publishes an anonymous or login entry point first and its
credentialled endpoint second loses its declared auth in conversion. AAK is then
correct about the config it was handed and wrong about the server. This has been
listed under Limitations since 2026-07-20; these are the first findings it has
actually produced. They are counted as false positives rather than excused,
because the finding text makes a claim about the *server* — but the fix belongs
in the corpus builder, not the rule. `_to_config()` now converts the first remote
that *declares headers*; the committed manifest predates that and these clear on
the next `make corpus` refresh. Regenerating 1,641 records inside a precision fix
would move the number for two reasons at once and make the improvement
unauditable, so it is deliberately not bundled here.

## Limitations (stated plainly)

- **"Benign" is a proxy.** A declared-auth, active, non-CVE registry server is a
  reasonable stand-in for "correctly configured," but it is not ground truth —
  some of these servers may be misconfigured in ways not visible in their
  registry metadata, and some flagged issues may be real.
- **Single rater, no inter-rater agreement.** All verdicts are the maintainer's.
  There is no second independent adjudicator, so no agreement statistic is
  reported.
- **Small adjudication denominator → wide interval.** 6 HIGH/CRITICAL findings
  across 536 configs gives a Wilson 95% CI of [30.0%, 90.3%] on the FP rate. The
  point estimate (66.7%) should not be read as precise; the interval is the
  honest summary. The *slice* is large; the number of high-severity findings it
  provokes is small, and that is what bounds the precision of this rate.
- **Config-level + conversion fidelity.** Registry servers are converted to
  `.mcp.json` shape from their `remotes`/`packages` metadata (**first remote
  only**), so a multi-remote server's auth can be under-represented. This is no
  longer hypothetical — see root cause B above.
- **Snapshot vs live drift.** The manifest is a 2026-07-26 snapshot. Servers
  republish, and at least one (`app.thoughtspot/mcp-server`) has changed version
  since, which is why its finding is adjudicated ambiguous rather than guessed at.
- **Scope is HIGH/CRITICAL.** MEDIUM/LOW findings (the bulk of the volume) are not
  adjudicated here; this measures the false-positive rate of the severities that
  drive operational action.

## History

| Run | Slice | HIGH/CRIT | FP / adjudicated | Rate | Note |
|-----|------:|----------:|-----------------:|-----:|------|
| 2026-07-20 | 368 | 4 | 2 / 4 | 50.0% | Custom API-key headers unrecognised. |
| 2026-07-22 | 368 | 1 | 0 / 1 | 0.0% | Post-#475: `X-*-Key` family recognised. |
| 2026-08-24 | 536 | 6 | 4 / 6 | 66.7% | Slice grew 368→536; `-Token`/`-Secret` families unrecognised, plus 2 first-remote conversion artifacts. **Untuned.** |
| 2026-08-24 (post-fix) | 536 | 4 | 2 / 4 | 50.0% | Header family extended to `-token`/`-secret`. Both remaining FPs are corpus conversion artifacts that clear on the next `make corpus`. |

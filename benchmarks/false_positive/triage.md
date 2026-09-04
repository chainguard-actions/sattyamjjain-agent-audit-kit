# Manual adjudication — benign-slice HIGH/CRITICAL findings

This is the human pass that makes the false-positive number credible. Every
HIGH/CRITICAL finding the harness surfaces on the benign slice is adjudicated by
hand: **true positive** (the config really has the issue), **false positive**
(AAK is wrong), or **ambiguous** (defensible either way). Findings are **not**
auto-labelled.

- **Rater:** single rater (the maintainer). No second rater, so there is no
  inter-rater agreement statistic — stated as a limitation in `RESULTS.md`.
- **Scope:** the top 30 HIGH/CRITICAL findings on the benign slice, ranked
  deterministically by severity → rule id → config → evidence. The 2026-07-20
  run produced **4** HIGH/CRITICAL findings total, so all 4 are adjudicated
  (fewer than 30).
- **Verdict rule:** the false-positive *rate* = (false positives) / (all
  adjudicated). Ambiguous verdicts count in the denominator but not as false
  positives (conservative — does not inflate the FP rate).

## Template (copy per finding)

| # | Rule ID | Config | Verdict | One-line reason |
|--:|---------|--------|:-------:|-----------------|
| … | `AAK-…` | `<server name>` | TP / FP / ambiguous | … |

## Adjudication — 2026-07-20 run (n = 4 HIGH/CRITICAL)

| # | Rule ID | Config | Verdict | One-line reason |
|--:|---------|--------|:-------:|-----------------|
| 1 | `AAK-MCP-001` | `ai.nefesh/human-state` | **FALSE POSITIVE** | Server authenticates with a custom `X-Nefesh-Key` API-key header; `AAK-MCP-001` only recognises `Authorization`/`Bearer`, so it wrongly reports "no authentication". |
| 2 | `AAK-MCP-001` | `ai.satoshidata/wallet-intelligence` | **FALSE POSITIVE** | Same gap: `X-WR-API-Key` is an API-key auth header (literally "API-Key"); the rule misses non-`Authorization` credential headers. |
| 3 | `AAK-MCP-001` | `ai.lattiq/x402-trading-signals` | **AMBIGUOUS** | `X-PAYMENT` gates access via the x402 pay-to-access protocol — access control, but not identity authentication; "no auth" is defensible either way. |
| 4 | `AAK-MCP-001` | `ai.spala/public-mcp` | **TRUE POSITIVE** | The only header is `Accept` (content negotiation, not auth); the server is named `public-mcp` and genuinely exposes a remote endpoint with no authentication. |

### Tally

- False positives: **2** (both a single root cause — `AAK-MCP-001` not recognising custom API-key headers).
- True positives: **1**.
- Ambiguous: **1**.
- **Benign-slice HIGH/CRITICAL false-positive rate = 2 / 4 = 50.0%** (Wilson 95% CI [15.0%, 85.0%]; n is small, so the interval is wide).

### Follow-up filed

The two false positives share one fixable gap — `AAK-MCP-001`'s "no auth" check
should recognise common API-key credential headers (`X-*-Key`, `X-API-Key`,
`Api-Key`, and the x402 `X-PAYMENT` case reviewed) as authentication, not just
`Authorization`/`Bearer`. Tracked as
[#475](https://github.com/sattyamjjain/agent-audit-kit/issues/475).

## Adjudication — 2026-07-22 re-run (post-#475, n = 1 HIGH/CRITICAL)

[#475](https://github.com/sattyamjjain/agent-audit-kit/issues/475) shipped:
`AAK-MCP-001` now recognises the `X-*-Key` / `*-API-Key` credential-header family
and the x402 `X-PAYMENT` access gate (value-aware — a hardcoded literal still
fires). Re-running the harness on the same 368-config slice:

| # | Rule ID | Config | Verdict | One-line reason |
|--:|---------|--------|:-------:|-----------------|
| 1 | `AAK-MCP-001` | `ai.spala/public-mcp` | **TRUE POSITIVE** | Sole header is `Accept` (content negotiation, not auth); a genuinely unauthenticated remote endpoint. Correctly flagged. |

### Tally (post-#475)

- False positives: **0** (both prior FPs — `X-Nefesh-Key`, `X-WR-API-Key` — cleared).
- True positives: **1**.
- Ambiguous: **0** (the x402 `X-PAYMENT` case is now recognised as a declared access gate).
- **Benign-slice HIGH/CRITICAL false-positive rate = 0 / 1 = 0.0%** (Wilson 95% CI [0.0%, 79.3%]; n = 1, interval very wide).
- No new HIGH/CRITICAL findings were introduced elsewhere on the corpus (full-corpus AAK-MCP-001 configs 497 → 492, delta −5, 0 newly firing).

## Adjudication — 2026-08-24 re-run (n = 6 HIGH/CRITICAL), UNTUNED

The corpus manifest grew from 1,374 to 1,641 registry servers, and the benign
slice with it: **368 → 536 configs**. Nobody re-ran the benchmark when the
manifest was refreshed, so the published number was measured against a slice
that no longer existed. This run is that re-measurement, and it is published
**before** any rule change, so the untuned number is on the record.

Six HIGH/CRITICAL findings, all `AAK-MCP-001`. Verified against the live MCP
Registry where the record still matches the snapshot version.

| # | Rule ID | Config | Verdict | One-line reason |
|--:|---------|--------|:-------:|-----------------|
| 1 | `AAK-MCP-001` | `ai.spala/public-mcp` | **TRUE POSITIVE** | Sole header is `Accept` (content negotiation, not auth); server is named `public-mcp`. Same verdict as 2026-07-22. |
| 2 | `AAK-MCP-001` | `ai.velarion/company-intelligence` | **FALSE POSITIVE** | Authenticates with `X-Velarion-Agent-Token`. `_CUSTOM_AUTH_HEADER_RE` covers the `-key` family (`x-*-key`, `*-api-key`, `*-api-token`, `*-access-key`) but a vendor token ending plain `-token` matches none of them. |
| 3 | `AAK-MCP-001` | `br.com.signdocs/mcp-server` | **FALSE POSITIVE** | Authenticates with `X-SignDocs-Client-Id` + `X-SignDocs-Client-Secret` — an OAuth client-credentials pair. Neither `-id` nor `-secret` is in the recognised family. |
| 4 | `AAK-MCP-001` | `co.curie/commerce` | **FALSE POSITIVE** | The server *is* authenticated: remote 1 (`/api/mcp/{shop_id}`) declares `Authorization` with `isSecret: true`. Verified live at the same version (1.0.0). The scanned config is remote 0 only — see root cause B. |
| 5 | `AAK-MCP-001` | `co.huggingface/hf-mcp-server` | **FALSE POSITIVE** | Same shape: remote 1 declares `Authorization` (`isSecret: true`); remote 0 is the `?login` OAuth entry point. Verified live at the same version (0.2.33). |
| 6 | `AAK-MCP-001` | `app.thoughtspot/mcp-server` | **AMBIGUOUS** | The snapshot records `auth_mode: static-credential` at v1.0.1, which requires some remote to declare a secret header. The live registry has since moved to v0.5.0, where neither remote declares one, so the July record cannot be re-verified. Not counted as a false positive. |

### Tally

- False positives: **4**.
- True positives: **1**.
- Ambiguous: **1** (counts in the denominator, not as a false positive).
- **Benign-slice HIGH/CRITICAL false-positive rate = 4 / 6 = 66.7%** (Wilson 95% CI **[30.0%, 90.3%]**).

### Two root causes, and only one of them is the scanner

**A. Scanner gap — the `#475` header family, one step out (findings 2, 3).**
`#475` extended `AAK-MCP-001` from `Authorization`/`Bearer` to the `X-*-Key` /
`*-API-Key` family. Real vendors also authenticate with `-Token`, `-Secret`, and
client-credential *pairs* (`-Client-Id` + `-Client-Secret`). The 2026-07 fix
generalised one suffix and stopped. This is AAK's defect and is fixed in the
tuning commit that follows this one.

**B. Benchmark gap — first-remote-only conversion (findings 4, 5, and probably 6).**
`fetch_registry._to_config()` synthesises the scannable config from
`remotes[0]`. When a server publishes an anonymous or login entry point first
and its credentialled endpoint second, the converted config drops the auth the
server actually declares, and AAK is then correct about the config it was handed
and wrong about the server. `RESULTS.md` has listed this under Limitations since
2026-07-20; these are the first findings it has actually produced. The finding
text makes a claim about the *server*, so these count as false positives rather
than being excused — but the fix belongs in the corpus builder, not the rule.

### Follow-up

Root cause A is fixed in the next commit (header family extended, with the
untuned number already published above). Root cause B is fixed in
`fetch_registry._to_config()` so future refreshes carry the credentialled
remote's headers; the committed manifest predates that fix, so findings 4-6
persist until the next `make corpus` refresh. That is stated rather than
smoothed over, because a rate that improves because the corpus was quietly
regenerated is not a rate anyone should trust.

## Adjudication — 2026-08-24 re-run (post-fix, n = 4 HIGH/CRITICAL), TUNED

Root cause A fixed: `AAK-MCP-001`'s credential-header family now covers the
`-token` and `-secret` suffixes as well as `-key`, so a vendor token header
(`X-Velarion-Agent-Token`) and an OAuth client-credentials pair
(`X-SignDocs-Client-Id` + `X-SignDocs-Client-Secret`) read as declared auth.

Measured across the whole 1,641-config corpus, the change silences **exactly
those 2 configs and nothing else** — 1,046 → 1,044 firing, 0 newly firing. A
widening that had silenced anything further would have been trading false
positives for false negatives, which on a CRITICAL rule is the worse trade.

Two negatives keep it honest and are pinned in
`tests/test_mcp_auth_header_family.py`: a bare `X-SignDocs-Client-Id` is still
*not* auth (a `client_id` is a public identifier — the pair is recognised because
of its secret half), and `X-CSRF-Token` / `X-XSRF-Token` are still not auth
despite the `-token` suffix, because they prove request provenance rather than
caller identity.

| # | Rule ID | Config | Verdict | One-line reason |
|--:|---------|--------|:-------:|-----------------|
| 1 | `AAK-MCP-001` | `ai.spala/public-mcp` | **TRUE POSITIVE** | Sole header is `Accept`; genuinely unauthenticated. Unchanged across all four runs. |
| 2 | `AAK-MCP-001` | `co.curie/commerce` | **FALSE POSITIVE** | Root cause B, unfixed in the committed data: `Authorization` (`isSecret`) is on remote 1, and the snapshot converted remote 0. |
| 3 | `AAK-MCP-001` | `co.huggingface/hf-mcp-server` | **FALSE POSITIVE** | Root cause B: `Authorization` on remote 1; remote 0 is the `?login` entry point. |
| 4 | `AAK-MCP-001` | `app.thoughtspot/mcp-server` | **AMBIGUOUS** | Live registry has moved to v0.5.0; the v1.0.1 record in the snapshot cannot be re-verified. |

### Tally (post-fix)

- False positives: **2** (both root cause B — the corpus, not the rule).
- True positives: **1**.
- Ambiguous: **1**.
- **Benign-slice HIGH/CRITICAL false-positive rate = 2 / 4 = 50.0%** (Wilson 95% CI **[15.0%, 85.0%]**).

### Why the rate did not fall further, stated plainly

`fetch_registry._to_config()` is fixed — it now converts the first remote that
*declares headers* rather than `remotes[0]` unconditionally — but the committed
manifest was fetched on 2026-07-26 and predates that fix. Findings 2 and 3 clear
on the next `make corpus` refresh, which is a networked step that also rewrites
all 1,641 server records and would perturb the State of MCP report. Bundling a
corpus regeneration into a precision fix would make the improvement unauditable:
the number would move for two reasons at once and nobody could say which.

Note also what the ratio does here. The scanner fix removed 2 findings from both
the numerator and the denominator, so the *rate* fell only 66.7% → 50.0% while
the absolute count of wrong findings fell 4 → 2. On a denominator this small the
ratio is the less informative of the two figures, which is why the badge now
leads with the slice size and shows the raw counts.

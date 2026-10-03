"""``AAK-MCP-TRANSPORT-SESSION-UNAUTH-001`` — CVE-2026-82456 (argocd-mcp 0.8.0).

The rule is keyed on the conjunction, not on the package name, so the tests are
too: no fixture here mentions argocd except the one that reproduces the
advisory's published snippet verbatim.

The negative fixtures carry the weight. ``test_loopback_bind_is_quiet`` is the
same file as the positive with one argument changed, so a regex that stops
distinguishing a bound host from an unbound one fails here rather than in
somebody's repository.

``test_generic_rule_is_silenced_on_the_cve_shape`` is the reason this rule
exists at all, written as an executable claim. If a later change to
``_AUTH_MARKER_RE`` makes the generic rule see this shape, that test fails and
whoever is holding it gets to decide which rule should own it — instead of
finding two criticals for one defect.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from agent_audit_kit.rules.builtin import RULES
from agent_audit_kit.models import Severity, Category
from agent_audit_kit.scanners.mcp_transport_session_unauth import scan

RULE = "AAK-MCP-TRANSPORT-SESSION-UNAUTH-001"
GENERIC = "AAK-MCP-HTTP-NOAUTH-SERVER-001"
CVE = "CVE-2026-82456"

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER = REPO_ROOT / "CHANGELOG.cves.md"

# The advisory's own snippet (GHSA-rp45-5x3v-48mr, src/server/transport.ts:73-91)
# plus the bind it describes at line 166: `app.listen(port)`, with no host and
# therefore no 0.0.0.0 anywhere in the file.
CVE_SHAPE = """\
import express from "express";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

const app = express();

app.post("/mcp", async (req, res) => {
  const apiToken =
    (req.headers["x-argocd-api-token"] as string) ||
    process.env.ARGOCD_API_TOKEN ||
    "";

  await fetch(`${process.env.ARGOCD_BASE_URL}/api/v1/applications`, {
    headers: { Authorization: `Bearer ${apiToken}` },
  });

  const transport = new StreamableHTTPServerTransport({});
  await server.connect(transport);
});

const port = Number(process.env.PORT ?? 3000);
app.listen(port);
"""

# Identical but for the bind. This is the file the rule must stay quiet on.
LOOPBACK_SHAPE = CVE_SHAPE.replace("app.listen(port);", 'app.listen(port, "127.0.0.1");')

# Python: an outbound credential written the idiomatic requests/httpx way, on a
# transport explicitly bound to every interface.
PY_SHAPE = """\
import os
import httpx
import uvicorn
from fastapi import FastAPI

app = FastAPI()
session = httpx.Client()
session.headers.update(Authorization=f"Bearer {os.environ['UPSTREAM_API_TOKEN']}")


@app.post("/mcp")
async def mcp_endpoint(payload: dict) -> dict:
    return session.get(f"{os.environ['UPSTREAM_BASE_URL']}/v1/things").json()


uvicorn.run(app, host="0.0.0.0", port=8080)
"""

PY_LOOPBACK_SHAPE = PY_SHAPE.replace('host="0.0.0.0"', 'host="127.0.0.1"')


def _ids(tmp_path: Path, name: str, content: str) -> set[str]:
    target = tmp_path / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {f.rule_id for f in scan(tmp_path)[0]}


def _engine_ids(tmp_path: Path, name: str, content: str) -> set[str]:
    """Every rule the full engine reports — used for the no-double-fire checks."""
    from agent_audit_kit.engine import run_scan

    target = tmp_path / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {f.rule_id for f in run_scan(tmp_path).findings}


# ---------------------------------------------------------------------------
# Positive
# ---------------------------------------------------------------------------


def test_published_cve_shape_fires(tmp_path: Path) -> None:
    assert RULE in _ids(tmp_path, "src/transport.ts", CVE_SHAPE)


def test_the_finding_names_the_implicit_bind(tmp_path: Path) -> None:
    """A finding that says "binds 0.0.0.0" on a file containing no such literal
    would send the reader looking for a string that is not there."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "transport.ts").write_text(CVE_SHAPE, encoding="utf-8")
    finding = next(f for f in scan(tmp_path)[0] if f.rule_id == RULE)
    assert "0.0.0.0" not in CVE_SHAPE
    assert ".listen(port) with no host" in finding.evidence


def test_explicit_bind_all_also_fires(tmp_path: Path) -> None:
    assert RULE in _ids(tmp_path, "server.py", PY_SHAPE)


# ---------------------------------------------------------------------------
# Negative — the fixtures that keep the rule honest
# ---------------------------------------------------------------------------


def test_loopback_bind_is_quiet(tmp_path: Path) -> None:
    """Same server, same environment token, one argument different."""
    assert RULE not in _ids(tmp_path, "src/transport.ts", LOOPBACK_SHAPE)


def test_python_loopback_bind_is_quiet(tmp_path: Path) -> None:
    assert RULE not in _ids(tmp_path, "server.py", PY_LOOPBACK_SHAPE)


def test_loopback_fixture_is_otherwise_identical() -> None:
    """Guards the guard: if the two fixtures ever drift apart by more than the
    bind, the negative stops testing the thing it claims to test."""
    assert LOOPBACK_SHAPE.replace('app.listen(port, "127.0.0.1");', "app.listen(port);") == CVE_SHAPE
    assert PY_LOOPBACK_SHAPE.replace('host="127.0.0.1"', 'host="0.0.0.0"') == PY_SHAPE


def test_inbound_auth_is_quiet(tmp_path: Path) -> None:
    """A real per-caller check clears it, even bound to every interface."""
    authed = CVE_SHAPE.replace(
        "const app = express();",
        'const app = express();\napp.use(requireAuth({ audience: "mcp" }));',
    ).replace(
        '    (req.headers["x-argocd-api-token"] as string) ||\n'
        "    process.env.ARGOCD_API_TOKEN ||\n"
        '    "";',
        "    process.env.UPSTREAM_API_TOKEN!;",
    )
    assert RULE not in _ids(tmp_path, "src/authed.ts", authed)


def test_no_credential_at_all_is_left_to_the_generic_rule(tmp_path: Path) -> None:
    """One defect, one rule id. A bind-all server with no credential material is
    what ``AAK-MCP-HTTP-NOAUTH-SERVER-001`` was written for."""
    plain = """\
import express from "express";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
const app = express();
app.get("/mcp", (req, res) => { new SSEServerTransport("/messages", res); });
app.listen(3000, "0.0.0.0");
"""
    ids = _engine_ids(tmp_path, "src/plain.ts", plain)
    assert RULE not in ids
    assert GENERIC in ids


def test_a_non_mcp_http_server_is_quiet(tmp_path: Path) -> None:
    """The MCP context gate: an ordinary API proxy with an upstream token is not
    this rule's business, however it binds."""
    plain = """\
import express from "express";
const app = express();
app.get("/v1/things", async (req, res) => {
  const r = await fetch("https://upstream.example/things", {
    headers: { Authorization: `Bearer ${process.env.UPSTREAM_API_TOKEN}` },
  });
  res.json(await r.json());
});
app.listen(3000);
"""
    assert RULE not in _ids(tmp_path, "src/proxy.ts", plain)


def test_python_missing_host_is_not_inferred_as_bind_all(tmp_path: Path) -> None:
    """Node's listen() defaults to every interface; uvicorn and Flask default to
    loopback. Inferring the JS semantic in Python would invent a finding."""
    py = PY_SHAPE.replace('uvicorn.run(app, host="0.0.0.0", port=8080)', "uvicorn.run(app, port=8080)")
    assert "0.0.0.0" not in py
    assert RULE not in _ids(tmp_path, "server.py", py)


def test_a_log_string_is_not_mistaken_for_a_host(tmp_path: Path) -> None:
    """`app.listen(port, () => log("..."))` still has no host argument."""
    with_cb = CVE_SHAPE.replace(
        "app.listen(port);",
        'app.listen(port, () => console.log("mcp server listening"));',
    )
    assert RULE in _ids(tmp_path, "src/transport.ts", with_cb)


# ---------------------------------------------------------------------------
# The reason the rule exists, as an executable claim
# ---------------------------------------------------------------------------


def test_generic_rule_is_silenced_on_the_cve_shape() -> None:
    """``_AUTH_MARKER_RE`` matches a bare ``Authorization:``, which the *outbound*
    header satisfies — so the generic rule reads this server as authenticated.
    That, plus a bind regex that needs a literal 0.0.0.0, is the whole gap."""
    from agent_audit_kit.scanners.mcp_server_auth import _AUTH_MARKER_RE
    from agent_audit_kit.scanners.mcp_http_noauth_server import _BIND_ALL_RE

    assert _AUTH_MARKER_RE.search(CVE_SHAPE), "gap closed upstream — re-home this rule"
    assert not _BIND_ALL_RE.search(CVE_SHAPE), "gap closed upstream — re-home this rule"


def test_the_cve_shape_is_not_reported_twice(tmp_path: Path) -> None:
    ids = _engine_ids(tmp_path, "src/transport.ts", CVE_SHAPE)
    assert RULE in ids
    assert GENERIC not in ids


def test_dns_rebinding_is_a_separate_finding(tmp_path: Path) -> None:
    """``AAK-DNS-REBIND-001`` fires alongside and should: a missing Host
    allow-list and a missing inbound credential are different defects with
    different fixes, and the advisory lists both separately."""
    ids = _engine_ids(tmp_path, "src/transport.ts", CVE_SHAPE)
    assert {RULE, "AAK-DNS-REBIND-001"} <= ids


# ---------------------------------------------------------------------------
# Rule metadata + ledger
# ---------------------------------------------------------------------------


def test_rule_is_registered_with_the_cve_as_its_anchor() -> None:
    rule = RULES[RULE]
    assert rule.severity is Severity.CRITICAL
    assert rule.category is Category.TRANSPORT_SECURITY
    assert rule.cve_references == [CVE]
    assert rule.limitations, "a single-file scanner must state its blind spot"


def test_the_rule_is_a_family_rule_not_a_package_signature() -> None:
    """No package name anywhere in the rule text: the detectable thing is the
    conjunction, so the next server of this shape needs no new rule."""
    rule = RULES[RULE]
    text = f"{rule.title} {rule.description} {rule.remediation}".lower()
    assert "argocd" not in text


@pytest.mark.parametrize("field", ["owasp_mcp_references", "owasp_agentic_references"])
def test_framework_mappings_are_present(field: str) -> None:
    assert getattr(RULES[RULE], field), f"{field} must not be empty"


def test_cve_is_recorded_in_the_ledger() -> None:
    assert CVE in LEDGER.read_text(encoding="utf-8")

#!/usr/bin/env python3
"""Generate ``remediation-key-corpus.json`` — the set of config keys a remediation
string is allowed to tell a user to set.

Why this exists
---------------
v0.3.78 corrected two rules whose remediation told users to set
``"deny_stdio_transport": true`` / ``"allowed_transports": ["sse"]`` "so a MITM
cannot flip the transport mid-session". Those are AgentAuditKit conventions, not
MCP specification fields: they appear in 0 of the 748 public configs in
``benchmarks/data``. A user who followed that advice added a key their MCP client
ignores, silenced the rule, and believed they were protected — strictly worse than
no advice, because it converted an open finding into false confidence.

That was fixed rule-by-rule. This corpus makes the class checkable: every key a
remediation asks for must be a key something actually reads. The assertion lives in
``tests/test_remediation_keys_are_real.py``.

Two sources, both already in the repo, so the check is offline and deterministic —
matching the no-network default scan path:

1. Every distinct JSON key in any config under ``benchmarks/data`` — the corpus the
   v0.3.78 changelog cites. This is deliberately permissive: a key that real MCP
   configs in the wild use is a key some client reads, whatever the spec says.
2. ``MCP_SPEC_FIELDS`` below — specification field and header names that are correct
   to recommend even though the sampled configs never happened to contain them
   (a config only shows what deployments *do*, not what the spec *defines*). Each
   entry cites the spec that defines it and where this repo already encodes it, so
   the list is reviewable rather than asserted.

Determinism: output keys are sorted and the file carries **no timestamp**. A
generated artifact with a clock in it churns on every run and trains reviewers to
ignore its diff (this repo already has that problem with
``public/owasp-agentic-coverage.json``). Byte-stability is what makes the staleness
check in the test meaningful.

Usage:
    python scripts/gen_remediation_key_corpus.py            # write the corpus
    python scripts/gen_remediation_key_corpus.py --check     # exit 1 if stale
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = REPO_ROOT / "benchmarks" / "data"
OUT_PATH = REPO_ROOT / "remediation-key-corpus.json"

SCHEMA_VERSION = "1"

# Specification field / header names that are legitimate to recommend even when the
# sampled configs do not contain them. Value = why it is real, and where this repo
# already encodes it — so a reviewer can check each claim without leaving the repo.
MCP_SPEC_FIELDS: dict[str, str] = {
    # --- MCP HTTP transport headers ---
    "Mcp-Method": (
        "MCP HTTP transport request header; encoded in "
        "agent_audit_kit/scanners/mcp_routing_desync.py"
    ),
    "Mcp-Session-Id": (
        "MCP streamable-HTTP session header; encoded in "
        "agent_audit_kit/scanners/mcp_stateless_migration.py"
    ),
    "Mcp-Name": "MCP server-identity header used by the registry/naming checks",
    "Last-Event-ID": "SSE resumption header referenced by the MCP HTTP transport",
    # --- Generic HTTP headers the MCP auth flow depends on ---
    "Authorization": (
        "HTTP auth header (RFC 9110); read by "
        "agent_audit_kit/scanners/oauth_misconfig.py"
    ),
    "WWW-Authenticate": (
        "RFC 9728 discovery is advertised through this challenge header"
    ),
    "Content-Type": "HTTP representation header (RFC 9110)",
    "Content-Length": "HTTP framing header (RFC 9110)",
    # --- RFC 9728 Protected Resource Metadata (AAK-OAUTH-008) ---
    "resource_metadata": (
        "RFC 9728 Protected Resource Metadata pointer; named in "
        "agent_audit_kit/rules/builtin.py"
    ),
    "authorization_servers": (
        "RFC 9728 metadata field; named in agent_audit_kit/rules/builtin.py"
    ),
    "scopes_supported": "RFC 9728 metadata field",
    "bearer_methods_supported": "RFC 9728 metadata field",
    "resource_documentation": "RFC 9728 metadata field",
    # --- OAuth params the auth-profile rules require (AAK-OAUTH-006/007) ---
    "iss": "RFC 9207 authorization-response issuer param (AAK-OAUTH-006)",
    "resource": "RFC 8707 resource indicator (AAK-OAUTH-007)",
    # --- JSON Schema keywords used on MCP tool input schemas ---
    "readOnly": (
        "JSON Schema validation keyword; honoured by "
        "agent_audit_kit/scanners/sandbox_self_disable.py"
    ),
    "additionalProperties": "JSON Schema keyword constraining unlisted properties",
}


def _walk_keys(obj: Any, out: set[str]) -> None:
    """Collect every mapping key at any depth."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            out.add(key)
            _walk_keys(value, out)
    elif isinstance(obj, list):
        for value in obj:
            _walk_keys(value, out)


def _config_files() -> list[Path]:
    if not CORPUS_DIR.is_dir():
        return []
    return sorted(p for p in CORPUS_DIR.rglob("*") if p.is_file())


def harvest_corpus_keys() -> tuple[set[str], int, list[str]]:
    """Return (keys, files_read, unparseable_relative_paths).

    Reads with ``utf-8-sig`` so a BOM-prefixed config still parses — one config in
    the corpus carries a UTF-8 BOM, and skipping it would quietly shrink the corpus.
    """
    keys: set[str] = set()
    unparseable: list[str] = []
    files = _config_files()
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            unparseable.append(path.relative_to(REPO_ROOT).as_posix())
            continue
        _walk_keys(data, keys)
    return keys, len(files), sorted(unparseable)


def build() -> dict[str, Any]:
    corpus_keys, n_files, unparseable = harvest_corpus_keys()
    all_keys: Iterable[str] = corpus_keys | set(MCP_SPEC_FIELDS)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": "scripts/gen_remediation_key_corpus.py",
        "purpose": (
            "Config keys a rule remediation may tell a user to set. Asserted by "
            "tests/test_remediation_keys_are_real.py so advice cannot name a key "
            "nothing reads."
        ),
        "sources": {
            "benchmarks_data": {
                "path": "benchmarks/data",
                "configs_read": n_files,
                "unparseable": unparseable,
                "distinct_keys": len(corpus_keys),
            },
            "mcp_spec_fields": {
                "count": len(MCP_SPEC_FIELDS),
                "fields": dict(sorted(MCP_SPEC_FIELDS.items())),
            },
        },
        "keys": sorted(all_keys),
    }


def _serialise(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=False, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if the committed corpus differs from a fresh build",
    )
    args = parser.parse_args()

    fresh = _serialise(build())

    if args.check:
        if not OUT_PATH.is_file():
            sys.stderr.write(
                f"{OUT_PATH.name} missing — run python "
                "scripts/gen_remediation_key_corpus.py\n"
            )
            return 1
        current = OUT_PATH.read_text(encoding="utf-8")
        if current != fresh:
            sys.stderr.write(
                f"{OUT_PATH.name} is stale vs benchmarks/data — regenerate with "
                "python scripts/gen_remediation_key_corpus.py and commit the result\n"
            )
            return 1
        sys.stdout.write(f"{OUT_PATH.name}: up to date.\n")
        return 0

    OUT_PATH.write_text(fresh, encoding="utf-8")
    payload = json.loads(fresh)
    src = payload["sources"]["benchmarks_data"]
    sys.stdout.write(
        f"wrote {OUT_PATH.name}: {len(payload['keys'])} keys "
        f"({src['distinct_keys']} from {src['configs_read']} configs, "
        f"{len(MCP_SPEC_FIELDS)} spec fields, "
        f"{len(src['unparseable'])} unparseable)\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

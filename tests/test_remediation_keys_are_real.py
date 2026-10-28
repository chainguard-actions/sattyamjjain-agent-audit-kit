"""Every config key a remediation tells you to set must be a key something reads.

The defect class
---------------
A remediation says "set ``X``". If ``X`` is not a field any MCP client reads, a user
who follows the advice changes nothing, silences the finding, and now believes they
are covered. That is worse than no advice: it converts an open finding into false
confidence.

v0.3.78 fixed two instances by hand — ``AAK-DOCSGPT-MCP-STDIO-MITM-001`` and
``AAK-GPTRESEARCHER-MCP-STDIO-MITM-001`` both told users to set
``"deny_stdio_transport": true`` / ``"allowed_transports": ["sse"]``, keys that appear
in 0 of the 748 public configs in ``benchmarks/data``.
``tests/test_transport_flip_remediation.py`` keeps those two rules honest by name.

This module generalises it to the whole registry, so the next invented key fails in
CI instead of shipping. The known-key corpus is committed
(``remediation-key-corpus.json``, built by ``scripts/gen_remediation_key_corpus.py``)
so the check is offline and deterministic, matching the no-network default scan path.

Direction of the allow-list
---------------------------
``AAK_OWN_CONVENTIONS`` enumerates **exemptions, not obligations**. A new rule with a
new invented key is not on it, so it fails closed. Each entry carries a one-line
reason, and ``test_every_exemption_is_actually_read_by_a_scanner`` proves the reason
is true by finding the key in the scanner source — so the allow-list cannot become a
parking spot for advice that still does nothing.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from agent_audit_kit.rules.builtin import RULES

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = REPO_ROOT / "remediation-key-corpus.json"
SCANNERS_DIR = REPO_ROOT / "agent_audit_kit" / "scanners"

# --- extraction -------------------------------------------------------------
# (a) a double-quoted identifier immediately followed by a colon: "key": value
#     This is the form that means "put this in your config file", which is exactly
#     the shape the v0.3.78 defect took.
QUOTED_KEY_RE = re.compile(r'"([A-Za-z_][A-Za-z0-9_.\-]*)"\s*:')
# (b) anything assigned inside a fenced block: key = value / key: value
FENCE_RE = re.compile(r"```[^\n]*\n(.*?)```", re.S)
FENCED_ASSIGN_RE = re.compile(
    r"^\s*[\"']?([A-Za-z_][A-Za-z0-9_.\-]*)[\"']?\s*(?::|=)\s*\S", re.M
)

# Deliberately NOT extracted: a bare backticked identifier. Measured across the
# registry, that form yields 112 distinct tokens of which ~109 are package names
# (`mcp-atlassian`), functions (`shlex.quote`), GitHub Actions triggers
# (`workflow_run`), iframe sandbox tokens (`allow-scripts`) and filenames — naming a
# thing is not the same as telling someone to configure it. Widening to backticks
# would require allow-listing ~109 non-keys, which is the blanket exemption this
# guard exists to prevent.

# --- exemptions -------------------------------------------------------------
# AAK's own annotations. Legitimate to recommend even though no MCP client reads
# them, because their stated purpose is to record a decision *for AgentAuditKit* and
# suppress a finding — not to configure a client. That is the opposite of the
# transport-flip defect, where an AAK-only key was presented as a security control.
#
# NOTE: the transport-flip keys (deny_stdio_transport, allowed_transports) are
# deliberately absent. Recommending those IS the defect; if a remediation ever
# proposes them again in config form, this test must fail.
AAK_OWN_CONVENTIONS: dict[str, str] = {
    "x-aak-shared-authz": (
        "AAK suppression annotation: records that a shared resource is "
        "intentionally global; read by scanners/shared_resource_authz.py"
    ),
    "x-aak-sandbox-control": (
        "AAK suppression annotation: records that a sandbox flag is host-set, "
        "not model-set; read by scanners/sandbox_self_disable.py"
    ),
}


def _load_corpus() -> set[str]:
    assert CORPUS_PATH.is_file(), (
        f"{CORPUS_PATH.name} missing — run "
        "`python scripts/gen_remediation_key_corpus.py` and commit the result"
    )
    payload = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    keys = payload.get("keys")
    assert isinstance(keys, list) and keys, f"{CORPUS_PATH.name} has no keys"
    return set(keys)


def extract_config_keys(text: str) -> set[str]:
    """Config-key-shaped tokens a remediation is asking the reader to set."""
    keys: set[str] = set(QUOTED_KEY_RE.findall(text))
    for block in FENCE_RE.findall(text):
        keys.update(FENCED_ASSIGN_RE.findall(block))
    return keys


def _sentence_containing(text: str, key: str) -> str:
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if key in sentence:
            return " ".join(sentence.split())
    return " ".join(text.split())[:200]


def test_every_remediation_key_is_real() -> None:
    """No remediation may tell a user to set a key nothing reads."""
    corpus = _load_corpus()
    allowed = corpus | set(AAK_OWN_CONVENTIONS)

    failures: list[str] = []
    for rule_id, rule in sorted(RULES.items()):
        text = getattr(rule, "remediation", "") or ""
        if not text:
            continue
        for key in sorted(extract_config_keys(text)):
            if key in allowed:
                continue
            failures.append(
                f"{rule_id}: remediation names config key {key!r}, which is not in "
                f"{CORPUS_PATH.name} and not an AAK_OWN_CONVENTIONS exemption.\n"
                f"    sentence: {_sentence_containing(text, key)}"
            )

    assert not failures, (
        f"{len(failures)} remediation(s) name a config key nothing reads. Either "
        "rewrite the remediation to name a control that works, or — if the key is an "
        "AAK annotation AAK itself reads — add it to AAK_OWN_CONVENTIONS with a "
        "one-line reason. Do not add a blanket exemption.\n\n" + "\n".join(failures)
    )


def test_exemptions_are_not_already_in_the_corpus() -> None:
    """A key that real configs use needs no exemption; a dead entry hides drift."""
    corpus = _load_corpus()
    redundant = sorted(set(AAK_OWN_CONVENTIONS) & corpus)
    assert not redundant, (
        f"AAK_OWN_CONVENTIONS entries are already in {CORPUS_PATH.name} and should be "
        f"removed: {redundant}"
    )


def test_every_exemption_is_actually_read_by_a_scanner() -> None:
    """The reason on each exemption has to be true.

    An exemption is only defensible if AAK really honours the key — otherwise the
    advice is the same defect wearing a different hat, and the allow-list has become
    the place bad advice goes to survive.
    """
    if not SCANNERS_DIR.is_dir():
        pytest.skip("scanners package not present in this checkout")
    sources = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in sorted(SCANNERS_DIR.glob("*.py"))
    )
    unread = [key for key in sorted(AAK_OWN_CONVENTIONS) if key not in sources]
    assert not unread, (
        "exempted key(s) are not read by any scanner, so recommending them does "
        f"nothing: {unread}. Remove the exemption and fix the remediation."
    )


def test_every_exemption_carries_a_reason() -> None:
    for key, reason in AAK_OWN_CONVENTIONS.items():
        assert reason and len(reason.split()) >= 5, (
            f"exemption {key!r} needs a one-line reason explaining why recommending "
            "it is legitimate"
        )


def test_extractor_catches_the_historical_defect() -> None:
    """Guard the guard.

    An extractor that finds nothing passes this module trivially. Feed it the
    remediation text v0.3.78 removed and assert both invented keys are caught, so a
    future refactor cannot quietly narrow the pattern into uselessness.
    """
    original = (
        'Set `"deny_stdio_transport": true` or '
        '`"allowed_transports": ["sse"]` in your MCP client config so a MITM '
        "cannot flip the transport mid-session."
    )
    found = extract_config_keys(original)
    assert "deny_stdio_transport" in found, "extractor no longer catches the 0.3.78 defect"
    assert "allowed_transports" in found, "extractor no longer catches the 0.3.78 defect"

    corpus = _load_corpus()
    allowed = corpus | set(AAK_OWN_CONVENTIONS)
    assert not (found & allowed), (
        "the keys v0.3.78 removed are now considered acceptable — if a real MCP "
        "client adopted them, revisit the remediation note; otherwise this is a "
        "corpus or allow-list regression"
    )


def test_extractor_reads_fenced_assignments() -> None:
    """The fenced-block branch currently matches nothing in the registry (no rule
    uses a code fence). Cover it directly so the branch is not dead code that
    silently stops working before the first author needs it."""
    fenced = 'Configure it:\n\n```json\n{\n  "made_up_key": true\n}\n```\n'
    assert "made_up_key" in extract_config_keys(fenced)
    toml_style = "Set it:\n\n```toml\nmade_up_toml = 1\n```\n"
    assert "made_up_toml" in extract_config_keys(toml_style)


def test_corpus_is_not_stale() -> None:
    """The committed corpus must match a fresh build from benchmarks/data.

    Same drift-guard shape as report-check / cve-latency-check: a generated artifact
    that nothing re-derives goes stale silently.
    """
    import importlib.util

    script = REPO_ROOT / "scripts" / "gen_remediation_key_corpus.py"
    assert script.is_file(), "scripts/gen_remediation_key_corpus.py missing"
    spec = importlib.util.spec_from_file_location("gen_remediation_key_corpus", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not module.CORPUS_DIR.is_dir():
        pytest.skip("benchmarks/data not present in this checkout")

    fresh = module.build()
    committed = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    assert committed["keys"] == fresh["keys"], (
        "remediation-key-corpus.json is stale vs benchmarks/data — run "
        "`python scripts/gen_remediation_key_corpus.py` and commit the result"
    )

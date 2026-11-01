"""public/owasp-agentic-coverage.json — schema + density + regen guard."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "gen_owasp_coverage.py"
JSON_PATH = REPO_ROOT / "public" / "owasp-agentic-coverage.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("gen_owasp_coverage", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["gen_owasp_coverage"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def regenerated(tmp_path_factory) -> dict:
    """Generate into a temp path and return the payload.

    It used to regenerate into the canonical repo path, autouse, so merely
    running pytest rewrote a tracked file and left the working tree dirty --
    every session, for a timestamp nobody changed. A test that mutates tracked
    state is a test you have to remember to undo, and this one was quietly
    undone by hand many times.
    """
    module = _load_module()
    out = tmp_path_factory.mktemp("owasp") / "coverage.json"
    rc = module.main(["--json", str(out)])
    assert rc == 0, "gen_owasp_coverage.py failed (coverage gap?)"
    return json.loads(out.read_text(encoding="utf-8"))


def _without_timestamp(payload: dict) -> dict:
    """Everything the generator derives, minus the one field that always differs."""
    return {k: v for k, v in payload.items() if k != "last_updated"}


def test_committed_json_matches_a_fresh_generation(regenerated: dict) -> None:
    """The staleness check the autouse fixture was papering over.

    Regenerating into the canonical path made every run pass by construction:
    the assertions then read the file the fixture had just written. Comparing a
    temp generation against the committed copy is what actually catches drift,
    and ignoring `last_updated` is what stops a wall-clock field reporting drift
    that is not there.
    """
    committed = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert _without_timestamp(committed) == _without_timestamp(regenerated), (
        "public/owasp-agentic-coverage.json is stale -- run "
        "`python scripts/gen_owasp_coverage.py` and commit the result."
    )


def test_json_file_exists() -> None:
    assert JSON_PATH.is_file(), (
        f"{JSON_PATH} missing. Run `python scripts/gen_owasp_coverage.py`."
    )


def test_schema_shape() -> None:
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1"
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", payload["last_updated"])
    assert isinstance(payload["aak_version"], str)
    assert isinstance(payload["rule_count"], int)
    assert isinstance(payload["coverage"], list)


def test_all_ten_slots_present() -> None:
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    ids = [row["asi_id"] for row in payload["coverage"]]
    assert ids == [f"ASI{i:02d}" for i in range(1, 11)]


def test_density_floor_three_per_slot() -> None:
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    for row in payload["coverage"]:
        assert row["rule_density"] >= 3, (
            f"{row['asi_id']} has density {row['rule_density']} < 3"
        )
        assert len(row["rules"]) == row["rule_density"]


def test_rule_entries_have_required_keys() -> None:
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    required = {"id", "severity", "cve_references", "aicm_references"}
    for row in payload["coverage"]:
        for rule in row["rules"]:
            assert required.issubset(rule.keys())
            assert isinstance(rule["cve_references"], list)
            assert isinstance(rule["aicm_references"], list)
            assert rule["severity"] in {"critical", "high", "medium", "low", "info"}

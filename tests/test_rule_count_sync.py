"""Single-source-of-truth test for rule count.

README / action.yml / __init__.RULE_COUNT / rules.json must all agree.
This test is the regression fence that catches human drift before it
reaches main. The sync tool (`scripts/sync_rule_count.py`) is the
enforcer; this test is the shape check.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Docs the sync script drives. Imported rather than mirrored: the mirror existed
# to catch a surface being dropped from the script, but it also meant every list
# change needed two edits, and it broke the moment two comparison pages were
# consolidated in v0.3.86. `test_every_doc_with_an_anchor_is_driven` covers the
# original intent from the other direction and needs no maintenance.
def _doc_total_anchor_files() -> tuple[str, ...]:
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from sync_rule_count import _TOTAL_ANCHOR_DOCS

    return tuple(_TOTAL_ANCHOR_DOCS)
_DOCS_RULES_MD = "docs/rules.md"


def _actual_rule_count() -> int:
    from agent_audit_kit.rules.builtin import RULES

    return len(RULES)


def _load_sync_module():
    """Import scripts/sync_rule_count.py as a module (it lives outside the package)."""
    script = REPO_ROOT / "scripts" / "sync_rule_count.py"
    assert script.is_file(), "scripts/sync_rule_count.py missing"
    spec = importlib.util.spec_from_file_location("sync_rule_count", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["sync_rule_count"] = module
    spec.loader.exec_module(module)
    return module


def test_bundle_count_matches_code() -> None:
    bundle = REPO_ROOT / "rules.json"
    assert bundle.is_file(), (
        "rules.json missing. Run `python scripts/sync_rule_count.py --regenerate`."
    )
    data = json.loads(bundle.read_text(encoding="utf-8"))
    assert isinstance(data.get("rules"), list)
    assert len(data["rules"]) == _actual_rule_count()


def test_readme_badge_matches() -> None:
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(r"img\.shields\.io/badge/rules-(\d+)-[a-z]+\.svg", text)
    assert m, "rules badge missing from README.md"
    assert int(m.group(1)) == _actual_rule_count()


def test_readme_anchors_all_match() -> None:
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    anchors = re.findall(
        r"<!--\s*rule-count:total\s*-->(\d+)<!--\s*/rule-count\s*-->",
        text,
    )
    assert anchors, "no rule-count anchors in README — sync script won't drive any section"
    for value in anchors:
        assert int(value) == _actual_rule_count()


def test_action_yml_description_matches() -> None:
    text = (REPO_ROOT / "action.yml").read_text(encoding="utf-8")
    m = re.search(r"description:.*?(\d+)\s+rules", text)
    assert m, "action.yml description missing the 'N rules' phrase"
    assert int(m.group(1)) == _actual_rule_count()


def test_init_rule_count_matches() -> None:
    from agent_audit_kit import RULE_COUNT

    assert RULE_COUNT == _actual_rule_count()


def test_sync_script_check_mode_is_clean() -> None:
    """Running the sync tool in --check mode should exit 0 on a clean tree.

    This is the broad fence: --check now covers README + action.yml +
    __init__.py + docs/rules.md summary + the comparison-page anchors.
    """
    module = _load_sync_module()

    old_argv = sys.argv[:]
    sys.argv = ["sync_rule_count", "--check"]
    try:
        rc = module.main()
    finally:
        sys.argv = old_argv
    assert rc == 0, "sync_rule_count --check reported drift; run the script and commit the result"


def test_docs_rules_summary_is_generated_from_registry() -> None:
    """docs/rules.md's Summary table must be the exact block the sync script
    renders from the live registry — so a new/renamed category or a count
    change can never leave the doc stale (the 221-vs-246 + missing-12th-category
    drift that motivated v0.3.49)."""
    module = _load_sync_module()
    count = _actual_rule_count()
    expected_block = module._render_rules_summary(count)
    text = (REPO_ROOT / _DOCS_RULES_MD).read_text(encoding="utf-8")
    assert expected_block in text, (
        f"{_DOCS_RULES_MD} summary table is not the registry-generated block; "
        "run scripts/sync_rule_count.py and commit the result."
    )
    # Every live category must be represented (guards against a dropped row).
    from agent_audit_kit.rules.builtin import RULES

    live_categories = {r.category.name for r in RULES.values()}
    for name in live_categories:
        assert name in module._CATEGORY_DISPLAY, (
            f"Category {name} has no display name in sync_rule_count._CATEGORY_DISPLAY"
        )


def test_docs_comparison_anchors_match_registry() -> None:
    """Every `<!-- rule-count:total -->N<!-- /rule-count -->` anchor in the
    comparison docs must equal len(RULES)."""
    count = _actual_rule_count()
    anchor_re = re.compile(
        r"<!--\s*rule-count:total\s*-->(\d+)<!--\s*/rule-count\s*-->"
    )
    for rel in _doc_total_anchor_files():
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        anchors = anchor_re.findall(text)
        assert anchors, f"{rel} has no rule-count anchor — sync can't drive it"
        for value in anchors:
            assert int(value) == count, (
                f"{rel} claims {value} rules; canonical is {count}. "
                "Run scripts/sync_rule_count.py."
            )


def _load_check_counts():
    """Import scripts/check_counts.py — the single source for the repo-wide count
    guard, shared by this test, the release CI gate, and `make count-check`. The
    prose patterns, canonical-count logic, and dated/frozen exclusion list all live
    there now, so they cannot drift from a second copy here."""
    script = REPO_ROOT / "scripts" / "check_counts.py"
    assert script.is_file(), "scripts/check_counts.py missing"
    spec = importlib.util.spec_from_file_location("check_counts", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_counts"] = module
    spec.loader.exec_module(module)
    return module


def test_no_stale_hardcoded_counts_in_prose() -> None:
    """No stale current-state count in any tracked markdown, repo-wide.

    Widened (v0.3.72) from the README / CLAUDE / docs / launch fence to the whole
    repo via scripts/check_counts.py — counts drifted exactly where nothing looked
    (DEEP_ANALYSIS.md, ROADMAP_2026.md, CLAUDE_PROMPT.md, research/**, owasp-outreach).
    The changelogs and a small set of dated / frozen artifacts (each carrying an
    in-file dated note or version label) are excluded in that module's
    EXCLUDE_EXACT / EXCLUDE_PREFIX; per-category and singular phrasings are excluded
    by construction of the patterns.
    """
    failures = _load_check_counts().find_stale_counts()
    assert not failures, (
        "stale count(s) in prose — reconcile to the registry, or add a dated note "
        "and exclude the file in scripts/check_counts.py:\n  " + "\n  ".join(failures)
    )


def test_historical_snapshot_files_carry_banner() -> None:
    """DEEP_ANALYSIS.md and ROADMAP_2026.md are exempt from the count guard by their
    dated historical-snapshot banner (v0.3.74), NOT a hard-coded name list. Assert the
    banner is actually present, so if either drops it, this test fails AND the guard
    starts checking the file's frozen v0.2.0 counts — a stale count can't hide behind a
    silently-removed banner (the exact way CLAUDE_PROMPT.md drifted)."""
    cc = _load_check_counts()
    for rel in ("DEEP_ANALYSIS.md", "ROADMAP_2026.md"):
        assert cc.has_historical_banner(REPO_ROOT / rel), (
            f"{rel} lost its dated historical-snapshot banner. Restore it, or update "
            "its counts to the canonical value — the guard now checks any banner-less file."
        )


def test_report_framework_choices_match_titles() -> None:
    """`len(_FRAMEWORK_TITLES)` is only a legitimate canonical number if it is the
    exact set of `report --framework` targets. Read the Click choices off the live
    command object (never re-listed by hand) and assert they equal the title keys
    once the single non-framework value `standards-crosswalk` is removed. If these
    drift, the "N frameworks" prose fence is measuring the wrong thing."""
    import click

    from agent_audit_kit.cli import cli
    from agent_audit_kit.output import pdf_report

    report_cmd = cli.commands["report"]
    framework_param = next(p for p in report_cmd.params if p.name == "framework")
    param_type = framework_param.type
    assert isinstance(param_type, click.Choice), "--framework is no longer a Click Choice"
    choices = set(param_type.choices)
    choices.discard("standards-crosswalk")

    titles = set(pdf_report._FRAMEWORK_TITLES)
    assert choices == titles, (
        "report --framework choices (minus standards-crosswalk) diverged from "
        f"pdf_report._FRAMEWORK_TITLES: only-in-choices={sorted(choices - titles)}, "
        f"only-in-titles={sorted(titles - choices)}"
    )


def test_rule_count_is_canonical() -> None:
    """One canonical number, computed from len(RULES), shown everywhere it is
    claimed as current state. Fails if any authoritative surface — README badge,
    README total-anchors, action.yml description, __init__.RULE_COUNT, the signed
    rules.json bundle — or the present-tense launch copy diverges from the
    registry. Historical/version-stamped/category counts (CHANGELOG, ROADMAP
    starting point, per-OWASP-category tables, "(v0.3.5)" snapshots) are NOT
    current-state claims and are intentionally out of scope.
    """
    count = _actual_rule_count()

    # 1. Authoritative current-state surfaces must all equal len(RULES).
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    badge = re.search(r"img\.shields\.io/badge/rules-(\d+)-[a-z]+\.svg", readme)
    assert badge and int(badge.group(1)) == count, "README badge != len(RULES)"
    anchors = re.findall(
        r"<!--\s*rule-count:total\s*-->(\d+)<!--\s*/rule-count\s*-->", readme
    )
    assert anchors and all(int(a) == count for a in anchors), "README anchor drift"

    action = (REPO_ROOT / "action.yml").read_text(encoding="utf-8")
    am = re.search(r"description:.*?(\d+)\s+rules", action)
    assert am and int(am.group(1)) == count, "action.yml description != len(RULES)"

    from agent_audit_kit import RULE_COUNT

    assert RULE_COUNT == count, "__init__.RULE_COUNT != len(RULES)"

    bundle = json.loads((REPO_ROOT / "rules.json").read_text(encoding="utf-8"))
    assert len(bundle["rules"]) == count, "rules.json bundle != len(RULES)"

    # 2. The package meta must not carry a divergent hard-coded count.
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    desc = re.search(r'^description\s*=\s*"([^"]*)"', pyproject, re.MULTILINE)
    assert desc, "pyproject description missing"
    bad = re.search(r"(\d+)\s+rules", desc.group(1))
    assert not bad or int(bad.group(1)) == count, (
        "pyproject description hard-codes a divergent rule count"
    )

    # 3. Present-tense launch copy (marketing claims) must match the registry.
    for rel in (
        "docs/launch/hn.md",
        "docs/launch/reddit.md",
        "docs/launch/x-thread.md",
    ):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        for claimed in re.findall(r"(\d+)\s+(?:deterministic\s+)?rules?\b", text):
            assert int(claimed) == count, (
                f"{rel} claims {claimed} rules; canonical is {count}. "
                "Update launch copy or run scripts/sync_rule_count.py."
            )

    # 4. Docs pages the sync script drives — the rules-reference summary total
    #    and the competitor-comparison rule-count cells (v0.3.49).
    anchor_re = re.compile(r"<!--\s*rule-count:total\s*-->(\d+)<!--\s*/rule-count\s*-->")
    rules_md = (REPO_ROOT / "docs/rules.md").read_text(encoding="utf-8")
    total_row = re.search(r"\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|", rules_md)
    assert total_row and int(total_row.group(1)) == count, "docs/rules.md Total != len(RULES)"
    for rel in _doc_total_anchor_files():
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        anchors = anchor_re.findall(text)
        assert anchors and all(int(a) == count for a in anchors), f"{rel} rule-count anchor drift"


def test_readme_test_count_marker_matches_the_tests_on_disk() -> None:
    """The README's test count is generated, not hand-written.

    It said "1,100+ tests" while the suite held 1,868 test functions -- roughly
    60% of the real number, and stale in the direction that undersells. A
    hand-written number next to a command is exactly the shape this repo keeps
    getting wrong, so it is now a marker with an owner.
    """
    import re
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from sync_rule_count import _test_function_count

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(r"<!--\s*test-count:total\s*-->([\d,]+)<!--\s*/test-count\s*-->", readme)
    assert m, "README lost its test-count marker; run scripts/sync_rule_count.py"
    claimed = int(m.group(1).replace(",", ""))
    actual = _test_function_count()
    assert claimed == actual, (
        f"README claims {claimed} test functions; the tree has {actual}. "
        "Run `python scripts/sync_rule_count.py`."
    )


def test_test_count_is_deterministic_and_offline() -> None:
    """Counted from the AST, not from pytest collection.

    Collection varies with parametrisation, skips and plugins, so a number taken
    from it would differ between machines and drift again. Two calls must agree,
    and the number must be large enough that a silent parse failure returning
    almost nothing would fail here.
    """
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from sync_rule_count import _test_function_count

    first = _test_function_count()
    assert first == _test_function_count()
    assert first > 1000, f"only {first} test functions found; parsing likely broke"


def test_scanner_manifest_arithmetic_reconciles_with_disk() -> None:
    """94 registered + 2 shims == 96 files, asserted rather than merely defensible.

    Anyone who counts files in agent_audit_kit/scanners/ gets 96 while the
    manifest advertises 94. That gap is legitimate -- two files are back-compat
    re-exports -- but until it was written down and checked, the only way to
    learn it was to read the generator's docstring.
    """
    import json
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from sync_scanner_count import scanner_module_files, unregistered_shims

    data = json.loads((REPO_ROOT / "scanners.json").read_text(encoding="utf-8"))
    assert "unregistered_shims" in data
    assert "_comment" in data, "the manifest must explain its own arithmetic"
    assert sorted(data["unregistered_shims"]) == sorted(unregistered_shims())
    assert data["count"] + len(data["unregistered_shims"]) == len(scanner_module_files())


def test_every_doc_with_an_anchor_is_driven_by_the_sync_script() -> None:
    """Both directions, so neither list can rot.

    Replaces a hand-mirrored copy of the script's doc list. A doc carrying a
    `rule-count:total` anchor that the script does not drive would go stale
    silently -- the exact failure the anchors exist to prevent -- and a doc in
    the script's list with no anchor is a dead entry that looks like coverage.
    """
    import re

    driven = set(_doc_total_anchor_files())
    anchor_re = re.compile(r"<!--\s*rule-count:total\s*-->")

    for rel in sorted(driven):
        path = REPO_ROOT / rel
        assert path.is_file(), f"{rel} is listed in _TOTAL_ANCHOR_DOCS but does not exist"
        assert anchor_re.search(path.read_text(encoding="utf-8")), (
            f"{rel} is driven by the sync script but carries no rule-count anchor"
        )

    # Frozen history is exempt through the same machinery check_counts uses, not
    # a second list: docs/changelog/archive/ quotes the marker syntax in prose
    # while describing a past fix, and rewriting a changelog entry to match
    # today's count would falsify the record it exists to keep.
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from check_counts import has_historical_banner, is_excluded

    undriven = []
    for path in sorted((REPO_ROOT / "docs").rglob("*.md")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel in driven or is_excluded(rel) or has_historical_banner(path):
            continue
        if anchor_re.search(path.read_text(encoding="utf-8")):
            undriven.append(rel)
    assert not undriven, (
        f"{undriven} carry a rule-count anchor that no script updates; add them to "
        "_TOTAL_ANCHOR_DOCS in scripts/sync_rule_count.py or remove the anchor."
    )

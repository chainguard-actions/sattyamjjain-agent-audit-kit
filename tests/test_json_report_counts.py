"""The JSON report must explain its own numbers.

`summary.total` and the severity histogram describe every finding the scan produced.
`findings` holds only what cleared `min_severity`, which defaults to LOW — so an INFO
finding is counted in the histogram and in `total`, and then absent from the array.

That is a defensible design, but nothing in the document said so. Scanning the 748-config
corpus produced `"total": 370`, `"info": 1`, and 369 entries in `findings`: a consumer
counting the array silently disagreed with the summary by one, and a histogram claiming
an INFO finding sat beside an array containing none.

`reported` and `minSeverity` close that gap without changing what any existing field
means. These tests hold the invariant in both directions — `reported` must always equal
the array length, and the gap must always be explained by the threshold.
"""

from __future__ import annotations

import json

from agent_audit_kit.models import Category, Finding, ScanResult, Severity
from agent_audit_kit.output.json_report import format_results


def _finding(rule_id: str, severity: Severity) -> Finding:
    return Finding(
        rule_id=rule_id,
        title=f"title for {rule_id}",
        description="d",
        severity=severity,
        category=Category.MCP_CONFIG,
        file_path="x.json",
        line_number=1,
        evidence="e",
        remediation="r",
    )


def _result(*severities: Severity) -> ScanResult:
    findings = [_finding(f"AAK-T-{i:03d}", s) for i, s in enumerate(severities)]
    return ScanResult(
        findings=findings,
        files_scanned=1,
        rules_evaluated=1,
        scan_duration_ms=1.0,
    )


def _report(result: ScanResult, **kw) -> dict:
    return json.loads(format_results(result, **kw))


def test_reported_equals_the_findings_array_length() -> None:
    """The invariant a consumer actually needs."""
    result = _result(Severity.CRITICAL, Severity.MEDIUM, Severity.INFO)
    report = _report(result)
    assert report["summary"]["reported"] == len(report["findings"])


def test_info_finding_is_counted_but_not_listed_at_the_default_threshold() -> None:
    """Reproduces the corpus discrepancy in miniature: total 3, reported 2."""
    report = _report(_result(Severity.HIGH, Severity.LOW, Severity.INFO))
    summary = report["summary"]
    assert summary["total"] == 3
    assert summary["info"] == 1
    assert summary["reported"] == 2
    assert len(report["findings"]) == 2
    assert not [f for f in report["findings"] if f["severity"] == "info"]


def test_min_severity_is_disclosed() -> None:
    """The field that explains the gap must name the threshold actually applied."""
    assert _report(_result(Severity.HIGH))["summary"]["minSeverity"] == "low"
    assert (
        _report(_result(Severity.HIGH), min_severity=Severity.CRITICAL)["summary"][
            "minSeverity"
        ]
        == "critical"
    )


def test_gap_between_total_and_reported_is_always_explained_by_the_threshold() -> None:
    """total - reported must equal exactly the findings below the threshold.

    If that ever stops holding, the two numbers differ for some *other* reason and
    `minSeverity` no longer explains the document.
    """
    order = [
        Severity.CRITICAL,
        Severity.HIGH,
        Severity.MEDIUM,
        Severity.LOW,
        Severity.INFO,
    ]
    result = _result(*order)
    for threshold in order:
        summary = _report(result, min_severity=threshold)["summary"]
        below = sum(1 for s in order if s < threshold)
        assert summary["total"] - summary["reported"] == below, threshold
        assert summary["total"] == len(order)


def test_total_still_counts_every_finding() -> None:
    """`total` keeps its old meaning — existing consumers must not shift."""
    result = _result(Severity.CRITICAL, Severity.INFO, Severity.INFO)
    for threshold in (Severity.INFO, Severity.LOW, Severity.CRITICAL):
        assert _report(result, min_severity=threshold)["summary"]["total"] == 3


def test_no_gap_when_threshold_admits_everything() -> None:
    report = _report(_result(Severity.HIGH, Severity.INFO), min_severity=Severity.INFO)
    summary = report["summary"]
    assert summary["total"] == summary["reported"] == len(report["findings"]) == 2


def test_severity_histogram_sums_to_total_not_to_reported() -> None:
    """The histogram describes the scan, so it must reconcile with `total`."""
    report = _report(_result(Severity.CRITICAL, Severity.LOW, Severity.INFO))
    summary = report["summary"]
    histogram = sum(summary[k] for k in ("critical", "high", "medium", "low", "info"))
    assert histogram == summary["total"]
    assert histogram != summary["reported"]

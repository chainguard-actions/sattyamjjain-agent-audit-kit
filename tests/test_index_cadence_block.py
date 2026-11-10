"""The README's index-cadence claim must stay generated, offline-checkable.

The MCP Security Index schedule failed every Monday from 2026-06-15 to
2026-08-21 and nobody noticed for two months. During that window the README
first said the leaderboard was updated weekly (false), and then said the cadence
was interrupted (true, but only until it wasn't). A sentence a human has to
remember to update is a sentence that is eventually wrong in one direction or
the other.

The fix is to state a fact that decays on its own — the date of the last
published snapshot — and to fail the build when it stops moving. The live half
of that guard is `scripts/index_cadence.py --check`, which runs in the
link-check workflow because only the network can settle it.

These tests are the offline half: the markers exist, the block is generated
rather than hand-written, and no prose has crept back in that promises a
frequency the data cannot support.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "link-check.yml"

START = "<!-- index-cadence -->"
END = "<!-- /index-cadence -->"


def _block() -> str:
    text = README.read_text(encoding="utf-8")
    match = re.search(re.escape(START) + r"(.*?)" + re.escape(END), text, re.S)
    assert match, "README has no index-cadence block"
    return match.group(1)


def test_the_block_exists_and_carries_a_date() -> None:
    assert re.search(r"\d{4}-\d{2}-\d{2}", _block()), (
        "the cadence block must state a snapshot date; a date is what decays "
        "visibly when publishing stops"
    )


def test_the_block_is_what_the_generator_would_write() -> None:
    """Offline shape check — the live comparison is the CI job."""
    from scripts.index_cadence import main  # noqa: PLC0415

    assert main(["--check", "--offline"]) == 0


def test_the_readme_does_not_promise_a_cadence_it_has_not_demonstrated() -> None:
    """One scheduled success is not a weekly cadence.

    The schedule was fixed in v0.3.86 and the 2026-08-24 run is the first
    scheduled one to land since. Saying "weekly" again before consecutive Mondays
    prove it would be repeating the original mistake with a fresher date.
    """
    block = _block().lower()
    for promise in ("weekly", "every week", "each week"):
        assert promise not in block, (
            f"the generated cadence block claims {promise!r}; it may state when the "
            "last snapshot published, not how often the next one will"
        )


def test_the_stale_index_guard_is_wired_into_ci() -> None:
    """A guard nobody runs is the situation this replaced."""
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "scripts/index_cadence.py --check" in workflow
    assert "index-cadence:" in workflow


def test_no_stale_interruption_notice_remains() -> None:
    """The inverse failure: leaving "interrupted" standing after the fix landed."""
    text = README.read_text(encoding="utf-8")
    for stale in ("cadence is currently interrupted", "cadence is not yet weekly"):
        assert stale not in text

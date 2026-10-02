#!/usr/bin/env python3
"""Render the MCP Security Index cadence line in README from the published data.

The README used to carry a hand-written cadence claim, and it was wrong in both
directions at different times: first "updated weekly" while every scheduled run
since 2026-06-15 was dying on an unhandled ``HTTP 429``, then "cadence is
currently interrupted" after the fault was fixed. A sentence a human has to
remember to update is a sentence that is eventually false.

So the README states a **fact that degrades on its own**: the date of the last
published snapshot, rendered from the snapshot history the index site actually
serves. If publishing stops, the date stops moving and says so without anyone
noticing first.

``--check`` is the CI half. It fails when the rendered date disagrees with the
published one, and *also* when the last snapshot is more than ``--max-age-days``
old (default 10). Ten days is deliberate for a Monday schedule: one missed week
(7 days) is tolerated as noise, two consecutive misses (14 days) fail the build.
Waiting for a human to notice is what let two months pass unnoticed before.

Usage::

    python scripts/index_cadence.py                 # rewrite the README line
    python scripts/index_cadence.py --check         # CI guard (network)
    python scripts/index_cadence.py --check --offline   # skip the fetch, verify shape only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

HISTORY_URL = "https://sattyamjjain.github.io/agent-audit-kit/data/history.json"
INDEX_URL = "https://sattyamjjain.github.io/agent-audit-kit/"

START = "<!-- index-cadence -->"
END = "<!-- /index-cadence -->"
_BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)

DEFAULT_MAX_AGE_DAYS = 10
_TIMEOUT = 30


def fetch_history(url: str = HISTORY_URL) -> list[dict]:
    """The published snapshot history. Network; raises on failure."""
    req = urllib.request.Request(url, headers={"User-Agent": "agent-audit-kit-cadence"})
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:  # noqa: S310
        data = json.loads(resp.read().decode("utf-8"))
    if isinstance(data, dict):
        data = data.get("snapshots") or data.get("history") or []
    if not isinstance(data, list):
        raise ValueError(f"unexpected history shape at {url}: {type(data).__name__}")
    return [row for row in data if isinstance(row, dict) and row.get("snapshot")]


def last_snapshot(history: list[dict]) -> datetime:
    stamps = []
    for row in history:
        raw = str(row["snapshot"]).replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(raw)
        except ValueError:
            continue
        stamps.append(parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc))
    if not stamps:
        raise ValueError("published history contains no parseable snapshot timestamps")
    return max(stamps)


def render_line(when: datetime, snapshots: int) -> str:
    """The README sentence. A date and a count, no cadence adjective.

    "Weekly" is a claim about the future that only consecutive runs can support;
    "last published <date>" is a claim about the past that the data settles.
    """
    plural = "snapshot" if snapshots == 1 else "snapshots"
    return (
        f"{START}Last published snapshot: **{when.date().isoformat()}** "
        f"({snapshots} {plural} in [`history.json`]({HISTORY_URL})). "
        f"The build fails if this date falls more than {DEFAULT_MAX_AGE_DAYS} days "
        f"behind, so a stalled index reports itself.{END}"
    )


def _replace(text: str, line: str) -> str:
    return _BLOCK_RE.sub(lambda _: line, text, count=1)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="Verify instead of rewriting.")
    ap.add_argument(
        "--offline",
        action="store_true",
        help="Skip the network fetch; only verify the markers exist and parse.",
    )
    ap.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS)
    args = ap.parse_args(sys.argv[1:] if argv is None else argv)

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print(
            f"README.md has no {START} ... {END} block; the cadence line must be "
            "generated rather than hand-written",
            file=sys.stderr,
        )
        return 1

    if args.offline:
        block = _BLOCK_RE.search(text)
        assert block is not None
        if not re.search(r"\d{4}-\d{2}-\d{2}", block.group(0)):
            print("cadence block carries no ISO date", file=sys.stderr)
            return 1
        print("cadence block present and shaped correctly (offline check)")
        return 0

    try:
        history = fetch_history()
        when = last_snapshot(history)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"could not read the published index history: {exc}", file=sys.stderr)
        return 1

    age = datetime.now(timezone.utc) - when
    want = render_line(when, len(history))

    if args.check:
        failed = False
        if _replace(text, want) != text:
            print(
                "README cadence line is stale - run 'python scripts/index_cadence.py' "
                f"and commit.\n  expected: {want}",
                file=sys.stderr,
            )
            failed = True
        if age > timedelta(days=args.max_age_days):
            print(
                f"MCP Security Index has not published since {when.date().isoformat()} "
                f"({age.days} days ago, limit {args.max_age_days}). The weekly schedule "
                f"has missed at least two runs - check {INDEX_URL} and the "
                "mcp-security-index workflow.",
                file=sys.stderr,
            )
            failed = True
        if failed:
            return 1
        print(
            f"index cadence ok: last snapshot {when.date().isoformat()} "
            f"({age.days}d ago), {len(history)} snapshots"
        )
        return 0

    updated = _replace(text, want)
    if updated != text:
        README.write_text(updated, encoding="utf-8")
        print(f"updated README cadence line (last snapshot {when.date().isoformat()})")
    else:
        print("cadence line already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

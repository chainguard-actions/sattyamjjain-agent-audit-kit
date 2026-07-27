"""Single-source-of-truth fence for the package version.

Three surfaces must never disagree:

1. ``pyproject.toml``'s ``version`` (what PyPI/OIDC publishes).
2. ``agent_audit_kit.__version__`` (what the installed package reports).
3. Every self-referencing ``@vX.Y.Z`` / ``rev: vX.Y.Z`` pin in ``README.md``
   (what we tell users to install) — a pin that points at a tag we never cut
   is exactly the "README says v0.3.60 but that tag doesn't exist" trap this
   test exists to prevent.

If a release can't cut the declared tag, the fix is to repin the README to a
tag that *does* resolve (and change the declared version to match) — not to
leave the surfaces disagreeing.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _pyproject_version() -> str:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    assert m, "pyproject.toml has no top-level version = \"...\""
    return m.group(1)


def _init_version() -> str:
    from agent_audit_kit import __version__

    return __version__


def test_pyproject_matches_dunder_version() -> None:
    assert _pyproject_version() == _init_version(), (
        f'pyproject version {_pyproject_version()!r} != '
        f'agent_audit_kit.__version__ {_init_version()!r}'
    )


def test_readme_self_pins_match_declared_version() -> None:
    """Every agent-audit-kit self-reference pin in README must equal the declared
    version, so the documented install/CI path always points at a real tag."""
    declared = _init_version()
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    # GitHub Action usage: `uses: sattyamjjain/agent-audit-kit@vX.Y.Z`
    action_pins = re.findall(
        r"sattyamjjain/agent-audit-kit@v(\d+\.\d+\.\d+)", readme
    )
    # pre-commit hook: `rev: vX.Y.Z` (README has one repos block — ours)
    precommit_pins = re.findall(r"rev:\s*v(\d+\.\d+\.\d+)", readme)
    # pip pin: `agent-audit-kit==X.Y.Z`
    pip_pins = re.findall(r"agent-audit-kit==(\d+\.\d+\.\d+)", readme)

    pins = action_pins + precommit_pins + pip_pins
    assert pins, (
        "README has no agent-audit-kit version pin to check — the @vX / rev: vX / "
        "==X snippets went missing; this fence would silently pass on nothing."
    )
    mismatched = [p for p in pins if p != declared]
    assert not mismatched, (
        f"README pins {sorted(set(mismatched))} disagree with declared version "
        f"{declared!r}. Repin the README (and re-cut the tag) so the documented "
        f"install path resolves."
    )

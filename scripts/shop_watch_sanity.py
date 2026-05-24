#!/usr/bin/env python3
"""shop_watch_sanity.py — GHA post-step roster/audit sanity check.

Usage:
    python3 scripts/shop_watch_sanity.py <YYYY-MM-DD> [coverage-audit.json path]

Exits 0 on warning, 1 on hard error.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


def parse_date(s: str) -> date | None:
    try:
        return date.fromisoformat(s)
    except Exception:
        return None


def check_roster(target: date) -> int:
    p = Path("ontology/shop-roster.json")
    if not p.exists():
        print("::warning::shop-roster.json missing")
        return 0
    r = json.loads(p.read_text(encoding="utf-8"))
    active = r.get("active_shops", []) or []
    seeds = r.get("manual_seeds", []) or []
    window = r.get("window_days", "?")
    print(
        f"roster OK — active:{len(active)}, manual_seeds:{len(seeds)}, window_days={window}"
    )
    violations = []
    for s in active:
        exp = parse_date(s.get("window_expires_on", ""))
        if exp is not None and target > exp:
            violations.append(f"{s.get('name', '?')} (exp={exp.isoformat()})")
    if violations:
        print(
            "::warning::Strict cap violation — "
            f"{len(violations)} expired active: " + ", ".join(violations)
        )
        return 1
    print("strict cap: OK (no expired active beyond target date)")
    return 0


def check_audit(audit_path: Path) -> int:
    if not audit_path.exists():
        print(f"no coverage-audit.json at {audit_path} (shop-watch may have skipped)")
        return 0
    data = json.loads(audit_path.read_text(encoding="utf-8"))
    summary = data.get("summary", {})
    crit = int(summary.get("critical", 0) or 0)
    warn = int(summary.get("warning", 0) or 0)
    patched = int(summary.get("patches_applied", 0) or 0)
    print(
        f"coverage-audit — CRITICAL:{crit}, WARNING:{warn}, patches_applied:{patched}"
    )
    if crit > 0 and patched < crit:
        print(
            f"::warning::Coverage audit: {crit} CRITICAL but only {patched} patches applied"
        )
        return 1
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: shop_watch_sanity.py <YYYY-MM-DD> [audit-path]", file=sys.stderr)
        return 2
    target = parse_date(argv[1])
    if target is None:
        print(f"invalid date: {argv[1]}", file=sys.stderr)
        return 2
    audit_path = Path(argv[2]) if len(argv) >= 3 else Path("/dev/null")
    rc1 = check_roster(target)
    rc2 = check_audit(audit_path)
    return max(rc1, rc2)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
